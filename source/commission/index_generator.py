from source.util import *

"""
生成commission index，提供导入。
"""

def str_to_position(commission_position):
    iii = 0
    cp = []
    ii = 1
    for i in commission_position[1:]:
        if not is_int(i):
            cp.append(commission_position[0:ii])
            cp.append(commission_position[ii:])
            break
        ii+=1
    position = [0,0]
    if cp[0][0] == 'N':
        position[0]=-int(cp[0][1:])
    else:
        position[0]=int(cp[0][1:])

    if cp[1][0] == 'N':
        position[1]=-int(cp[1][1:])
    else:
        position[1]=int(cp[1][1:])

    return position

commission_list = []
commission_dict = {}
for root, dirs, files in os.walk(os.path.join(ROOT_PATH,"source\\commission\\commissions")):
    for file in files:
        if file[file.index('.'):]==".py":
            commission_list.append(file.replace('.py',''))
            filename = file.replace('.py','')
            commission_type = filename.split('_')[0]
            commission_position = filename.split('_')[1]
            commission_dict[filename]={
                "type":commission_type,
                "position":str_to_position(commission_position)
            }

with open(os.path.join(ROOT_PATH,"source\\commission\\commission_index.py"), "w") as f:
    f.write("\"\"\"This file is generated automatically. Do not manually modify it.\"\"\"\n")
    f.write(f"COMMISSION_INDEX = {str(commission_dict)}\n")
    f.write("def get_commission_object(commission_name:str):\n")
    for i in commission_list:
        f.write(f"    if commission_name == '{i}':\n")
        f.write(f"        import source.commission.commissions.{i}\n")
        f.write(f"        return source.commission.commissions.{i}.{i}()\n")