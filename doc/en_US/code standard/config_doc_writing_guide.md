# Configuration document writing guide

## Naming format

The name is usually the name of the target document plus the suffix `{language}.jsondoc`.

For example, `auto_domain.json` should be named `auto_domain.json.zh_CN.jsondoc`.

## Storage location

It should be stored in the same directory as the corresponding configuration according to the naming convention.

## Translation

The translation of the key is written directly into the value. For example:

```json
{
  "domain_times": 1,
  "fast_mode": true,
  "isLiYueDomain": false,
  "resin": "20"
}
```

Change to

```json
{
  "domain_times": "secret_expedition_times",
  "fast_mode": "fast_mode",
  "isLiYueDomain": "Whether the domain is blocked by walls",
  "resin": "resin"
}
```

## Select box

I've thought about this before, but I didn't write it because I thought I could do without it, but this time it looks like I have to write it...

As above, the selection box just needs to add an item named `select_items` to the dict.

For example:

```json
{
  "itemname": {
    "select_items": [
      "Sweet Flower - Mund",
      "Neon flower - Riyuki",
      "Naruto - Inawashiro"
    ],
    "doc": "item_name"
  }
}
```
## Other

- If you think there are some unnecessary translations then you can delete the key-value pairs and the program will automatically use the configured values as headers.
- <strong>Please do not write json documents that cannot be parsed!!!</strong>