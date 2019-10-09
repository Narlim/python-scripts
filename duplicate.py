import os
import hashlib
import pysnooper
from pathlib import Path
from operator import itemgetter
from collections import Counter
from itertools import groupby
import time

def getfilemd5(filepath):
    ha = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            ha.update(data)
    return ha.hexdigest()


# @pysnooper.snoop()
def getfilepath(startpath):
    filepaths = []
    for (root, _, files) in os.walk(startpath):
        if files:
            for file in files:
                filepath = os.path.join(root, file)
                p = Path(filepath)
                try:
                    size = os.path.getsize(filepath)
                except FileNotFoundError as e:
                    pass
                if not p.is_socket() and not p.is_symlink() and size != 0:
                    fileinfo = (filepath, size, getfilemd5(filepath))
                    filepaths.append(fileinfo)
    sorted_filepaths = sorted(filepaths, key=itemgetter(1))
    # print(len(sorted_filepaths))
    duplicate_files_size = compare(sorted_filepaths)
    return [item for item in filepaths if item[1] in duplicate_files_size]
    

def compare(sorted_filepaths):
    files_size_dic = dict(Counter([item[1] for item in sorted_filepaths]))
    result = {key: value for key, value in files_size_dic.items() if value >= 2}
    return result.keys()

def get_result(startpath):
    duplicate_files = sorted(getfilepath(startpath), key=lambda item: item[1])
    res_dict =  {size: list(item) for size, item in groupby(duplicate_files, key=lambda item: item[1])}
    filepath_list = []
    for value in res_dict.values():
        if value[0][2] == value[1][2]:
            filepath_list.append(value[0])
    return filepath_list

def delete_file():
    pass

if __name__ == "__main__":
    starttime = time.time()
    print(get_result('/Users/marlin/Braid'))
    # getfilepath('/Users/marlin/Documents')
    endtime = time.time()
    print(endtime - starttime)