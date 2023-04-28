from source.error_code.util import *
IMPORT_ERROR_1 = ERR_CODE(level=LEVEL_CRI, message="IMPORT_ERROR", err_id=1, addition_id=0)
IMPORT_ERROR_2 = ERR_CODE(level=LEVEL_CRI, message="IMPORT_ERROR", err_id=1, addition_id=1)

if __name__ == '__main__':
    print(IMPORT_ERROR_1)