import re
from source.util import *
from source.manager.img_manager import ImgIcon
from source.manager.button_manager import Button
from source.common.decorator import cached_property, del_cached_property
from source.common.utils import area_pad, corner2area, crop, extract_white_letters, float2str
from source.ocr.models import OCR_MODEL, TextSystem
from pponnxcr.predict_system import BoxedResult
from source.exceptions.common import ScriptError
from datetime import timedelta


class OcrResultButton(Button):
    pass


class Ocr:
    # Merge results with box distance <= thres
    merge_thres_x = 0
    merge_thres_y = 0

    def __init__(self, lang=None):
        """
        Args:
            button:
            lang: If None, use in-game language
        """
        if lang is None:
            lang = 'zh_CN'

        self.name: str = 'testname1'
        self.lang: str = lang

    @cached_property
    def model(self) -> TextSystem:
        return OCR_MODEL.get_by_lang(self.lang)

    def pre_process(self, image):
        """
        Args:
            image (np.ndarray): Shape (height, width, channel)

        Returns:
            np.ndarray: Shape (width, height)
        """
        return image

    def after_process(self, result):
        """
        Args:
            result (str): '第二行'

        Returns:
            str:
        """
        if result.startswith('UID'):
            result = 'UID'
        return result

    def format_result(self, result):
        """
        Will be overriden.
        """
        return result

    def _log_change(self, attr, func, before):
        after = func(before)
        if after != before:
            logger.debug(f'{self.name} {attr}', f'{before} -> {after}')
        return after

    def ocr_single_line(self, image):
        # pre process
        start_time = time.time()
        # if not direct_ocr:
        #     image = crop(image, self.button.area)
        image = self.pre_process(image)
        # ocr
        result, _ = self.model.ocr_single_line(image)
        # after proces
        result = self._log_change('after', self.after_process, result)
        result = self._log_change('format', self.format_result, result)
        logger.attr(name='%s %ss' % (self.name, float2str(time.time() - start_time)),
                    text=str(result))
        return result

    def ocr_multi_lines(self, image_list):
        # pre process
        start_time = time.time()
        image_list = [self.pre_process(image) for image in image_list]
        # ocr
        result_list = self.model.ocr_lines(image_list)
        result_list = [(result, score) for result, score in result_list]
        # after process
        result_list = [(self.after_process(result), score) for result, score in result_list]
        result_list = [(self.format_result(result), score) for result, score in result_list]
        logger.attr(name="%s %ss" % (self.name, float2str(time.time() - start_time)),
                    text=str([result for result, _ in result_list]))
        return result_list

    def filter_detected(self, result: BoxedResult) -> bool:
        """
        Return False to drop result.
        """
        return True

    def detect_and_ocr(self, image) -> t.List[BoxedResult]:
        """
        Args:
            image:
            direct_ocr: True to ignore `button` attribute and feed the image to OCR model without cropping.

        Returns:

        """
        # pre process
        start_time = time.time()
        image = self.pre_process(image)
        # ocr
        results: t.List[BoxedResult] = self.model.detect_and_ocr(image)
        # after proces
        for result in results:
            result.box = tuple(corner2area(result.box))

        results = [result for result in results if self.filter_detected(result)]
        # results = merge_buttons(results, thres_x=self.merge_thres_x, thres_y=self.merge_thres_y)
        for result in results:
            result.ocr_text = self.after_process(result.ocr_text)

        logger.attr(name='%s %ss' % (self.name, float2str(time.time() - start_time)),
                    text=str([result.ocr_text for result in results]))
        return results

    def _match_result(
            self,
            result: str,
            keyword_classes,
            lang: str = None,
            ignore_punctuation=True,
            ignore_digit=True):
        """
        Args:
            result (str):
            keyword_classes: A list of `Keyword` class or classes inherited `Keyword`

        Returns:
            If matched, return `Keyword` object or objects inherited `Keyword`
            If not match, return None
        """
        if not isinstance(keyword_classes, list):
            keyword_classes = [keyword_classes]

        # Digits will be considered as the index of keyword
        if ignore_digit:
            if result.isdigit():
                return None

        # Try in current lang
        for keyword_class in keyword_classes:
            try:
                matched = keyword_class.find(
                    result,
                    lang=lang,
                    ignore_punctuation=ignore_punctuation
                )
                return matched
            except ScriptError:
                continue

        return None

    def matched_single_line(
            self,
            image,
            keyword_classes,
            lang: str = None,
            ignore_punctuation=True
    ) -> OcrResultButton:
        """
        Args:
            image: Image to detect
            keyword_classes: `Keyword` class or classes inherited `Keyword`, or a list of them.
            lang:
            ignore_punctuation:

        Returns:
            OcrResultButton: Or None if it didn't matched known keywords.
        """
        result = self.ocr_single_line(image)

        result = self._match_result(
            result,
            keyword_classes=keyword_classes,
            lang=lang,
            ignore_punctuation=ignore_punctuation,
        )

        logger.attr(name=f'{self.name} matched',
                    text=result)
        return result

    def matched_multi_lines(
            self,
            image_list,
            keyword_classes,
            lang: str = None,
            ignore_punctuation=True
    ) -> t.List[OcrResultButton]:
        """
        Args:
            image_list:
            keyword_classes: `Keyword` class or classes inherited `Keyword`, or a list of them.
            lang:
            ignore_punctuation:

        Returns:
            List of matched OcrResultButton.
            OCR result which didn't matched known keywords will be dropped.
        """
        results = self.ocr_multi_lines(image_list)

        results = [self._match_result(
            result,
            keyword_classes=keyword_classes,
            lang=lang,
            ignore_punctuation=ignore_punctuation,
        ) for result in results]
        results = [result for result in results if result.is_keyword_matched]

        logger.attr(name=f'{self.name} matched',
                    text=results)
        return results


class Digit(Ocr):
    def __init__(self, button: Button):
        super().__init__(button)

    def format_result(self, result) -> int:
        """
        Returns:
            int:
        """
        result = super().after_process(result)
        logger.attr(name=self.name, text=str(result))

        res = re.search(r'(\d+)', result)
        if res:
            return int(res.group(1))
        else:
            logger.warning(f'No digit found in {result}')
            return 0


class DigitCounter(Ocr):
    def __init__(self, button: Button):
        super().__init__(button)

    @classmethod
    def is_format_matched(cls, result) -> bool:
        return '/' in result

    def format_result(self, result) -> t.Tuple[int, int, int]:
        """
        Do OCR on a counter, such as `14/15`, and returns 14, 1, 15

        Returns:
            int:
        """
        result = super().after_process(result)
        logger.attr(name=self.name, text=str(result))

        res = re.search(r'(\d+)\s*/\s*(\d+)', result)
        if res:
            groups = [int(s) for s in res.groups()]
            current, total = int(groups[0]), int(groups[1])
            # current = min(current, total)
            return current, total - current, total
        else:
            logger.warning(f'No digit counter found in {result}')
            return 0, 0, 0


class Duration(Ocr):
    @classmethod
    def timedelta_regex(cls, lang):
        regex_str = {
            'cn': r'^(?P<prefix>.*?)'
                  r'((?P<days>\d{1,2})\s*天\s*)?'
                  r'((?P<hours>\d{1,2})\s*小时\s*)?'
                  r'((?P<minutes>\d{1,2})\s*分钟\s*)?'
                  r'((?P<seconds>\d{1,2})\s*秒)?'
                  r'(?P<suffix>[^天时钟秒]*?)$',
            'en': r'^(?P<prefix>.*?)'
                  r'((?P<days>\d{1,2})\s*d\s*)?'
                  r'((?P<hours>\d{1,2})\s*h\s*)?'
                  r'((?P<minutes>\d{1,2})\s*m\s*)?'
                  r'((?P<seconds>\d{1,2})\s*s)?'
                  r'(?P<suffix>[^dhms]*?)$'
        }[lang]
        return re.compile(regex_str)

    def after_process(self, result):
        result = super().after_process(result)
        result = result.strip('.,。，')
        result = result.replace('Oh', '0h').replace('oh', '0h')
        return result

    def format_result(self, result: str) -> timedelta:
        """
        Do OCR on a duration, such as `18d 2h 13m 30s`, `2h`, `13m 30s`, `9s`

        Returns:
            timedelta:
        """
        matched = self.timedelta_regex(self.lang).search(result)
        if not matched:
            return timedelta()
        days = self._sanitize_number(matched.group('days'))
        hours = self._sanitize_number(matched.group('hours'))
        minutes = self._sanitize_number(matched.group('minutes'))
        seconds = self._sanitize_number(matched.group('seconds'))
        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    @staticmethod
    def _sanitize_number(number) -> int:
        if number is None:
            return 0
        return int(number)


class OcrWhiteLetterOnComplexBackground(Ocr):
    def pre_process(self, image):
        image = extract_white_letters(image, threshold=255)
        image = cv2.merge([image, image, image])
        return image

    def detect_and_ocr(self, *args, **kwargs):
        # Try hard to lower TextSystem.box_thresh
        backup = self.model.text_detector.box_thresh
        self.model.text_detector.box_thresh = 0.2

        result = super().detect_and_ocr(*args, **kwargs)

        self.model.text_detector.box_thresh = backup
        return result
