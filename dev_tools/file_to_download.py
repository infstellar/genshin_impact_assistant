import shutil, os
path1 = "D:\\Program Data\\vscode\\GIA\\forGIALDL\\genshin_impact_assistant_forLDL"
path2 = "D:\\Program Data\\vscode\\GIA_Launcher_Download_Lib"

def verify_path(root):
    if not os.path.exists(root):
        verify_path(os.path.join(root, "../"))
        os.mkdir(root)
        print(f"dir {root} has been created")

def copy_from_to(rootpath):
    times = 0
    for root, dirs, files in os.walk(rootpath):
        if ".git" in root:
            continue
        for f in files:
            if f not in [".gitmodules", ".git"]:
                print(f"{f} has been copied.\n from {os.path.join(root, f)}\n to {os.path.join(root.replace(path1, path2), f)}")
                verify_path(root.replace(path1, path2))
                shutil.copy(os.path.join(root, f), os.path.join(root.replace(path1, path2), f))
                times+=1
    print(times)
    # for d in dirs:
    #     if d not in [".git"]:
    #         copy_from_to(os.path.join(root, d))



copy_from_to(path1)
                