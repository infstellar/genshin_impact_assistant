#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.
from source.util import *

logger.info(t2t('Creating yolox obj. It may takes a few second.'))

import sys, os

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_PATH)
import argparse
import datetime
import time
# from source.loguru import logger

import cv2

try:
    import torch
except Exception as error:
    logger.critical(t2t("导入torch时错误; err code: 002"))
    logger.exception(error)
from yolox.data.data_augment import ValTransform
from yolox.data.datasets import COCO_CLASSES
# from source.yolox.data.datasets import VOC_CLASSES
from yolox.exp import get_exp
from yolox.utils import fuse_model, get_model_info, postprocess, vis

IMAGE_EXT = [".jpg", ".jpeg", ".webp", ".bmp", ".png"]
globaldevice = GIAconfig.General_DeviceTorch
if globaldevice == 'auto':
    if torch.cuda.is_available():
        globaldevice = 'gpu'
    else:
        globaldevice = 'cpu'


class Sim_Args:
    def __init__(self, demo, experiment_name, name, path, camid, save_result, exp_file, device, conf, nms, tsize,
                 fp16=False, legacy=False,
                 fuse=False, trt=False, ckpt=None):
        self.demo = demo
        self.experiment_name = experiment_name
        self.name = name
        self.path = path
        self.camid = camid
        self.save_result = save_result
        self.exp_file = exp_file
        self.device = device
        self.conf = conf
        self.nms = nms
        self.tsize = tsize
        self.fp16 = fp16
        self.legacy = legacy
        self.fuse = fuse
        self.trt = trt
        self.ckpt = ckpt


def make_parser():
    parser = argparse.ArgumentParser("YOLOX Demo!")
    parser.add_argument(
        "demo", default="image", help="demo type, eg. image, video and webcam"
    )
    parser.add_argument("-expn", "--experiment-name", type=str, default=None)
    parser.add_argument("-n", "--name", type=str, default=None, help="model name")

    parser.add_argument(
        "--path", default="./assets/dog.jpg", help="path to images or video"
    )
    parser.add_argument("--camid", type=int, default=0, help="webcam demo camera id")
    parser.add_argument(
        "--save_result",
        action="store_true",
        help="whether to save the inference result of image/video",
    )

    # exp file
    parser.add_argument(
        "-f",
        "--exp_file",
        default=None,
        type=str,
        help="please input your experiment description file",
    )
    parser.add_argument("-c", "--ckpt", default=None, type=str, help="ckpt for eval")
    parser.add_argument(
        "--device",
        default="cpu",
        type=str,
        help="device to run our model, can either be cpu or gpu",
    )
    parser.add_argument("--conf", default=0.3, type=float, help="test conf")
    parser.add_argument("--nms", default=0.3, type=float, help="test nms threshold")
    parser.add_argument("--tsize", default=None, type=int, help="test img size")
    parser.add_argument(
        "--fp16",
        dest="fp16",
        default=False,
        action="store_true",
        help="Adopting mix precision evaluating.",
    )
    parser.add_argument(
        "--legacy",
        dest="legacy",
        default=False,
        action="store_true",
        help="To be compatible with older versions",
    )
    parser.add_argument(
        "--fuse",
        dest="fuse",
        default=False,
        action="store_true",
        help="Fuse conv and bn for testing.",
    )
    parser.add_argument(
        "--trt",
        dest="trt",
        default=False,
        action="store_true",
        help="Using TensorRT model for testing.",
    )
    return parser


def make_parser_2(
        demo="image",
        experiment_name=None,
        name='yolox-s',
        path='D:\\Program Data\\IDEA\\yolo3_test1\\YOLOX\\assets\\head2.jpg',
        camid=0,
        save_result=True,
        exp_file=None,
        device=globaldevice,
        conf=0.3,
        nms=0.5,
        tsize=640,
        fp16=True,
        legacy=False,
        trt=False,
        ckpt="D:\\Program Data\\vscode\\yolox_test4\\YOLOX_outputs\\tree_exp\\best_ckpt.pth"

):
    path1 = "D:\\Program Data\\IDEA\\yolo3_test1\\yoloxmodel\\yolox_ss.pth"
    path2 = "D:\\Program Data\\IDEA\\yolo3_test1\\YOLOX\\YOLOX_outputs\\yolox_voc_s\\best_ckpt.pth"
    args = Sim_Args(demo=demo,
                    experiment_name=experiment_name,
                    name=name,
                    path=path,
                    camid=camid,
                    save_result=save_result,
                    exp_file=exp_file,
                    device=device,
                    conf=conf,
                    nms=nms,
                    tsize=tsize,
                    fp16=fp16,
                    legacy=legacy,
                    trt=trt,
                    ckpt=ckpt)
    return args


def get_image_list(path):
    image_names = []
    for maindir, subdir, file_name_list in os.walk(path):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            ext = os.path.splitext(apath)[1]
            if ext in IMAGE_EXT:
                image_names.append(apath)
    return image_names


class Predictor(object):
    def __init__(
            self,
            model,
            exp,
            cls_names=COCO_CLASSES,
            trt_file=None,
            decoder=None,
            device="cpu",
            fp16=True,
            legacy=False,
    ):
        self.model = model
        self.cls_names = cls_names
        self.decoder = decoder
        self.num_classes = exp.num_classes
        self.confthre = exp.test_conf
        self.nmsthre = exp.nmsthre
        self.test_size = exp.test_size
        self.device = device
        self.fp16 = fp16
        self.preproc = ValTransform(legacy=legacy)
        if trt_file is not None:
            # torch2trt=None
            # from source.torch2trt import TRTModule

            # model_trt = TRTModule()
            # model_trt.load_state_dict(torch.load(trt_file))

            # x = torch.ones(1, 3, exp.test_size[0], exp.test_size[1]).cuda()
            # self.model(x)
            # self.model = model_trt
            pass

    def inference(self, img):
        img_info = {"id": 0}
        if isinstance(img, str):
            img_info["file_name"] = os.path.basename(img)
            img = cv2.imread(img)
        else:
            img_info["file_name"] = None

        height, width = img.shape[:2]
        img_info["height"] = height
        img_info["width"] = width
        img_info["raw_img"] = img

        ratio = min(self.test_size[0] / img.shape[0], self.test_size[1] / img.shape[1])
        img_info["ratio"] = ratio

        img, _ = self.preproc(img, None, self.test_size)
        img = torch.from_numpy(img).unsqueeze(0)
        img = img.float()
        if self.device == "gpu":
            img = img.cuda()
            if self.fp16:
                img = img.half()  # to FP16

        with torch.no_grad():
            t0 = time.time()
            outputs = self.model(img)
            if self.decoder is not None:
                outputs = self.decoder(outputs, dtype=outputs.type())
            outputs = postprocess(
                outputs, self.num_classes, self.confthre,
                self.nmsthre, class_agnostic=True
            )

            logger.debug("Infer time: {:.4f}s".format(time.time() - t0))
        return outputs, img_info

    def visual(self, output, img_info, cls_conf=0.35):
        ratio = img_info["ratio"]
        img = img_info["raw_img"]
        if output is None:
            return img
        output = output.cpu()

        bboxes = output[:, 0:4]

        # preprocessing: resize
        bboxes /= ratio

        cls = output[:, 6]
        scores = output[:, 4] * output[:, 5]

        vis_res = vis(img, bboxes, scores, cls, cls_conf, self.cls_names)
        return vis_res, [bboxes, scores, cls, cls_conf, self.cls_names]


def image_demo(predictor: Predictor, vis_folder, path, current_time, save_result, img_id=-1):
    # if os.path.isdir(path):
    #     files = get_image_list(path)
    # else:
    files = [path]  # path is a list in this time
    files.sort()
    addition_info = []

    for image_name in files:
        if isinstance(image_name, str):
            # img_info["file_name"] = os.path.basename(image_name)
            img = cv2.imread(image_name)
        else:
            img = image_name
            if img_id != -1:
                image_name = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f') + str(img_id) + '.jpg'
                # image_name = time.strftime("%Y_%m_%d_%H_%M_%S_%F", current_time)+'.jpg'+str(img_id)
            else:
                image_name = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f') + '.jpg'
                # image_name = time.strftime("%Y_%m_%d_%H_%M_%S_%F", current_time)+'.jpg'

        # img = cv2.imread(image_name)
        outputs, img_info = predictor.inference(img)
        if outputs[0] is not None:
            result_image, adi = predictor.visual(outputs[0], img_info, predictor.confthre)
        else:
            return None, None
        addition_info.append(adi)
        if save_result:
            save_folder = os.path.join(
                vis_folder  # , "visimg"   # time.strftime("%Y_%m_%d_%H_%M_%S", current_time)
            )
            # os.makedirs(save_folder, exist_ok=True)
            save_file_name = os.path.join(save_folder, os.path.basename(image_name))

            logger.debug("Saving detection result in {}".format(save_file_name))
            cv2.imwrite(save_file_name, result_image)
        ch = cv2.waitKey(0)
        if ch == 27 or ch == ord("q") or ch == ord("Q"):
            break
        return addition_info, result_image


def imageflow_demo(predictor, vis_folder, current_time, args):
    cap = cv2.VideoCapture(args.path if args.demo == "video" else args.camid)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
    fps = cap.get(cv2.CAP_PROP_FPS)
    if args.save_result:
        save_folder = os.path.join(
            vis_folder, time.strftime("%Y_%m_%d_%H_%M_%S", current_time)
        )
        os.makedirs(save_folder, exist_ok=True)
        if args.demo == "video":
            save_path = os.path.join(save_folder, os.path.basename(args.path))
        else:
            save_path = os.path.join(save_folder, "camera.mp4")

            logger.debug(f"video save_path is {save_path}")
        vid_writer = cv2.VideoWriter(
            save_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (int(width), int(height))
        )
    while True:
        ret_val, frame = cap.read()
        if ret_val:
            outputs, img_info = predictor.inference(frame)
            result_frame = predictor.visual(outputs[0], img_info, predictor.confthre)
            if args.save_result:
                vid_writer.write(result_frame)
            else:
                cv2.namedWindow("yolox", cv2.WINDOW_NORMAL)
                cv2.imshow("yolox", result_frame)
            ch = cv2.waitKey(1)
            if ch == 27 or ch == ord("q") or ch == ord("Q"):
                break
        else:
            break


def main(exp, args):
    if not args.experiment_name:
        args.experiment_name = exp.exp_name

    file_name = os.path.join(exp.output_dir, args.experiment_name)
    os.makedirs(file_name, exist_ok=True)

    vis_folder = None
    if args.save_result:
        vis_folder = os.path.join(file_name, "vis_res")
        os.makedirs(vis_folder, exist_ok=True)

    if args.trt:
        args.device = "gpu"

        logger.debug("Args: {}".format(args))

    if args.conf is not None:
        exp.test_conf = args.conf
    if args.nms is not None:
        exp.nmsthre = args.nms
    if args.tsize is not None:
        exp.test_size = (args.tsize, args.tsize)

    model = exp.get_model()

    logger.debug("Model Summary: {}".format(get_model_info(model, exp.test_size)))

    if args.device == "gpu":
        model.cuda()
        if args.fp16:
            model.half()  # to FP16
    model.eval()

    if not args.trt:
        if args.ckpt is None:
            ckpt_file = os.path.join(file_name, "best_ckpt.pth")
        else:
            ckpt_file = args.ckpt

            logger.debug("loading checkpoint")
        ckpt = torch.load(ckpt_file, map_location="cpu")
        # load the model state dict
        model.load_state_dict(ckpt["model"])

        logger.debug("loaded checkpoint done.")

    if args.fuse:
        logger.debug("\tFusing model...")
        model = fuse_model(model)

    if args.trt:
        assert not args.fuse, "TensorRT model is not support model fusing!"
        trt_file = os.path.join(file_name, "model_trt.pth")
        assert os.path.exists(
            trt_file
        ), "TensorRT model is not found!\n Run python3 tools/trt.py first!"
        model.head.decode_in_inference = False
        decoder = model.head.decode_outputs

        logger.debug("Using TensorRT to inference")
    else:
        trt_file = None
        decoder = None

    predictor = Predictor(
        model, exp, COCO_CLASSES, trt_file, decoder,
        args.device, args.fp16, args.legacy,
    )
    current_time = time.localtime()
    if args.demo == "image":
        return image_demo(predictor, vis_folder, args.path, current_time, args.save_result)
    elif args.demo == "video" or args.demo == "webcam":
        imageflow_demo(predictor, vis_folder, current_time, args)


class Yolox_Api:
    def __init__(self, vis_folder=None,
                 save_result=False,
                 ckpt="assets/YoloxModels/best_ckpt.pth"
                 ):

        self.args = make_parser_2(save_result=save_result,
                                  ckpt=ckpt
                                  )
        logger.debug("yolox device: " + self.args.device)
        self.exp = get_exp(self.args.exp_file, self.args.name)
        if not self.args.experiment_name:
            self.args.experiment_name = self.exp.exp_name

        file_name = os.path.join(self.exp.output_dir, self.args.experiment_name)
        os.makedirs(file_name, exist_ok=True)

        self.vis_folder = os.path.join(file_name, "vis_res")
        os.makedirs(self.vis_folder, exist_ok=True)
        if self.args.save_result:
            if vis_folder is not None:
                self.vis_folder = vis_folder

        if self.args.trt:
            self.args.device = "gpu"

        logger.debug("Args: {}".format(self.args))

        if self.args.conf is not None:
            self.exp.test_conf = self.args.conf
        if self.args.nms is not None:
            self.exp.nmsthre = self.args.nms
        if self.args.tsize is not None:
            self.exp.test_size = (self.args.tsize, self.args.tsize)

        model = self.exp.get_model()

        logger.debug("Model Summary: {}".format(get_model_info(model, self.exp.test_size)))

        if self.args.device == "gpu":
            model.cuda()
            if self.args.fp16:
                model.half()  # to FP16
        model.eval()

        if not self.args.trt:
            if self.args.ckpt is None:
                ckpt_file = os.path.join(file_name, "best_ckpt.pth")
            else:
                ckpt_file = self.args.ckpt

            logger.debug("loading checkpoint")
            ckpt = torch.load(ckpt_file, map_location="cpu")
            # load the model state dict
            # may should ###
            model.load_state_dict(ckpt["model"])

            logger.debug("loaded checkpoint done.")

        if self.args.fuse:
            logger.debug("\tFusing model...")
            model = fuse_model(model)

        if self.args.trt:
            assert not self.args.fuse, "TensorRT model is not support model fusing!"
            trt_file = os.path.join(file_name, "model_trt.pth")
            assert os.path.exists(
                trt_file
            ), "TensorRT model is not found!\n Run python3 tools/trt.py first!"
            model.head.decode_in_inference = False
            decoder = model.head.decode_outputs

            logger.debug("Using TensorRT to inference")
        else:
            trt_file = None
            decoder = None

        self.predictor = Predictor(
            model, self.exp, COCO_CLASSES, trt_file, decoder,
            self.args.device, self.args.fp16, self.args.legacy,
        )

        logger.debug("predictor has been created")

    def predicte(self, imgsrc, img_id=-1):

        logger.debug("predicte img")
        self.current_time = time.localtime()
        if self.args.demo == "image":
            if True:
                return image_demo(self.predictor, self.vis_folder, imgsrc, self.current_time, self.args.save_result,
                                  img_id=img_id)

            # else:
            #    return image_demo(self.predictor, self.vis_folder, self.args.path, self.current_time,
            #                      self.args.save_result)  # just backup

        elif self.args.demo == "video" or self.args.demo == "webcam":
            imageflow_demo(self.predictor, self.vis_folder, self.current_time, self.args)
        pass

    @staticmethod
    def get_maxap_pic_bbox(addinfo):
        return addinfo[0][0][0].numpy()

    @staticmethod
    def get_center(addinfo):
        a = addinfo[0][0][0].numpy()
        return a[0] + (a[2] - a[0]) / 2, a[1] + (a[3] - a[1]) / 2


yolo_tree = Yolox_Api()
logger.info(t2t('Created yolox obj.'))
if __name__ == "__main__":
    # yolox=yolox_api_custom()
    # yolox.predicte(cv2.imread("D:\\Program Data\\IDEA\\yolo3_test1\\YOLOX\\assets\\head.jpg",1))
    # yolox.predicte(cv2.imread("D:\\Program Data\\IDEA\\yolo3_test1\\YOLOX\\assets\\head2.jpg",1))
    # yolox.predicte(cv2.imread("D:\\Program Data\\IDEA\\yolo3_test1\\YOLOX\\assets\\head3.jpg",1))
    # args = make_parser()#.parse_args()
    # print(args)
    # exp = get_exp(args.exp_file, args.name)

    # main(exp, args)
    # ya = Yolox_Api()
    a = yolo_tree.predicte(cv2.imread("D:\\Program Data\\vscode\\yolox_test4\\assets\\84.jpg"))
    # print()
