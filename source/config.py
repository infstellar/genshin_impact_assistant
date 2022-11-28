from util import *

def template_generator():
    config_files = []
    for root, dirs, files in os.walk(os.path.join(root_path,'config')):
        for f in files:
            if f[f.index('.')+1:] == "json":
                config_files.append({"label": f, "value": os.path.join(root, f)})

    for json_file in config_files:
        json_item = json.load(open(json_file["value"], 'r', encoding='utf-8'))
        json.dump(json_item, open( os.path.join( os.path.dirname(json_file["value"]), json_file["label"]+"template"), 'w', encoding='utf-8'), sort_keys=True, indent=2, ensure_ascii=False)


def template_translator():
    template_files = []
    for root, dirs, files in os.walk(os.path.join(root_path,'config')):
        for f in files:
            if f[f.index('.')+1:] == "jsontemplate":
                template_files.append({"label": f, "value": os.path.join(root, f)})

    config_files = []
    for root, dirs, files in os.walk(os.path.join(root_path,'config')):
        for f in files:
            if f[f.index('.')+1:] == "json":
                config_files.append({"label": f, "value": os.path.join(root, f)})

    for template_file in template_files:
        json_item = json.load(open(template_file["value"], 'r', encoding='utf-8'))
        json.dump(json_item, open( os.path.join( os.path.dirname(template_file["value"]), template_file["label"].replace(".jsontemplate", ".json")), 'w', encoding='utf-8'), sort_keys=True, indent=2, ensure_ascii=False)

# template_translator()