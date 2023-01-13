import gettext
l10n = gettext.translation("zh_CN", localedir="./locale", languages=["zh_CN"])
l10n.install()
_ = l10n.gettext

print(_("This is a translatable string."))
print(_("Hello world!."))
ab=1
print(f"format test: {ab} 123")

# python pygettext.py -d zh_CN -p locale/zh_CN/LC_MESSAGES/zh_CN.po test.py
# python pygettext.py -d en_US -p locale/zh_CN/LC_MESSAGES/en_US.po test.py
# python msgfmt.py -o locale/zh_CN/LC_MESSAGES/zh_CN.mo locale/zh_CN/LC_MESSAGES/zh_CN.pot
# python msgfmt.py -o locale/en_US/LC_MESSAGES/en_US.mo locale/en_US/LC_MESSAGES/en_US.pot

'''
python pygettext.py -d zh_CN -p locale/zh_CN/LC_MESSAGES ../source/*.py
python pygettext.py -d en_US -p locale/en_US/LC_MESSAGES ../source/*.py

python pygettext.py -d zh_CN -p locale/zh_CN/LC_MESSAGES test.py
python pygettext.py -d en_US -p locale/en_US/LC_MESSAGES test.py
'''