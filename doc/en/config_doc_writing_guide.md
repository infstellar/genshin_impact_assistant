# Configuration document writing guide

```
Portions of this document may be machine translated.
```

## naming format

The name is generally the name of the target document to accelerate the suffix `.jsondoc`.

For example, the document name corresponding to `auto_domain.json` should be `auto_domain.json.jsondoc`.

## storage location

It should be stored in the same directory as the corresponding configuration according to the naming convention.

## single layer dict

If the document is a single-level dict, the easiest way is to copy the json file and change the value to the text you want.
E.g:

```json
{
   "domain_times": 1,
   "fast_mode": true,
   "isLiYueDomain": false,
   "resin": "20"
}
```

changed to

```json
{
   "domain_times": "Times of Secret Land Exploration",
   "fast_mode": "Fast Mode",
   "isLiYueDomain": "Is it LiYueDomain?",
   "resin": "resin"
}
```

## nested dict

It is inevitable that there will be nested dicts in the writing of json, of course, this has been considered at the beginning.
Just fill in the value when writing:

```json
{"doc": "your text","data":<nested dict>}
```

example:

```json
{
   "bennett": {
     "E_long_cd_time": 10,
     "E_short_cd_time": 3,
     "Ecd_float_time": 0,
     "Elast_time": 0
   }
}
```

should be written as:

```json
{
   "bennett": {
     "doc": "Bennett",
     "data": {
       "E_long_cd_time": "Elemental Combat Technique Long CD",
       "E_short_cd_time": "Elemental Combat Technique Short CD",
       "Ecd_float_time": "Ecd_float_time": "Elemental Combat Skill Float Time",
       "Elast_time": "The time since the last elemental combat skill was performed"
     }
   }
}
```

## select box

I thought about this problem before, but I didn't write it because I thought it should be unnecessary. This time it seems that I have to write it..

As above, the select box only needs to add an item named `select_items` in the dict.

E.g:

```json
{
   "itemname": {
     "select_items": [
       "Sweet Flower - Mond",
       "Neon Flowers - Liyue",
       "Ningcao - Inazuma"
     ],
     "doc": "Item Name"
   }
}
```

## other

- If you think there are some unnecessary translations, you can delete the key-value pair, and the program will automatically use the configured value as the title.
- <strong>Please do not write unparseable json documents!!!</strong>