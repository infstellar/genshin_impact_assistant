# Translate Guide

## Generate POT file

To Generate POT file, use follow command:

```
cd translation
python pygettext.py -d zh_CN -p locale/zh_CN/LC_MESSAGES ../*.py
python pygettext.py -d en_US -p locale/en_US/LC_MESSAGES ../*.py
cd ../
```

## Translate In PoEdit

- open .po file in PoEdit

- click `translate` `update from POT file`

- select .pot file

## Generate mo file

