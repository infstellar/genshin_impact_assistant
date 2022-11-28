import os
def unzip():
    if not os.path.exists(os.path.join('source', 'cvAutoTrack_7.2.3', 'CVAUTOTRACK.dll')):
        import zipfile
        file = zipfile.ZipFile(os.path.join('source', 'cvAutoTrack_7.2.3', 'CVAUTOTRACK.zip'))
        file.extractall(os.path.join('source', 'cvAutoTrack_7.2.3'))
        file.close()