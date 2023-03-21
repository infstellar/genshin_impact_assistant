from source.util import *
import shutil

def template_generator():
    config_files = []
    for root, dirs, files in os.walk(os.path.join(ROOT_PATH, 'config', 'settings')):
        for f in files:
            if f[f.index('.')+1:] == "json":
                config_files.append({"label": f, "value": os.path.join(root, f)})

    for root, dirs, files in os.walk(os.path.join(ROOT_PATH, 'config', 'tactic')):
        for f in files:
            if f[f.index('.')+1:] == "json":
                config_files.append({"label": f, "value": os.path.join(root, f)})

    for json_file in config_files:
        json_item = json.load(open(json_file["value"], 'r', encoding='utf-8'))
        json.dump(json_item, open( os.path.join( os.path.dirname(json_file["value"]), json_file["label"]+"template"), 'w', encoding='utf-8'), sort_keys=True, indent=2, ensure_ascii=False)


def template_translator():
    template_files = []
    oflag = False
    for root, dirs, files in os.walk(os.path.join(ROOT_PATH, 'config', 'settings')):
        for f in files:
            if f[f.index('.')+1:] == "jsontemplate":
                template_files.append({"label": f, "value": os.path.join(root, f)})
    for root, dirs, files in os.walk(os.path.join(ROOT_PATH, 'config', 'mission_groups')):
        for f in files:
            if f[f.index('.')+1:] == "jsontemplate":
                template_files.append({"label": f, "value": os.path.join(root, f)})

    for template_file in template_files:
        config_file_path = os.path.join( os.path.dirname(template_file["value"]), template_file["label"].replace(".jsontemplate", ".json"))
        if os.path.exists(config_file_path) == False:
            json.dump({}, open(config_file_path, 'w'), sort_keys=True, indent=2, ensure_ascii=False)
            oflag = True
        config_file = json.load(open(config_file_path, 'r', encoding='utf-8'))
        template_json = json.load(open(template_file["value"], 'r', encoding='utf-8'))
        for i in template_json:
            a = config_file.setdefault(i, template_json[i])

        json.dump(config_file, open(config_file_path, 'w', encoding='utf-8'), sort_keys=True, indent=2, ensure_ascii=False)
    if oflag:
        return "template translate successfully"
    else:
        return "no operation required"

def template_translator_tactic():
    template_files = []
    oflag = False
    for root, dirs, files in os.walk(os.path.join(ROOT_PATH, 'config', 'tactic')):
        for f in files:
            if f[f.index('.')+1:] == "jsontemplate":
                template_files.append({"label": f, "value": os.path.join(root, f)})

    for template_file in template_files:
        config_file_path = os.path.join( os.path.dirname(template_file["value"]), template_file["label"].replace(".jsontemplate", ".json"))
        template_json = json.load(open(template_file["value"], 'r', encoding='utf-8'))
        if os.path.exists(config_file_path) == False:
            shutil.copyfile(template_file["value"], config_file_path)
            oflag = True

    if oflag:
        return "template translate successfully"
    else:
        return "no operation required"
