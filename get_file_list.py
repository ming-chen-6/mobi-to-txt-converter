import logging

from glob import iglob
from os import listdir, getcwd, makedirs
from os.path import isfile, join, dirname


def getFileInCurrDir(rootdir: str)->list:
    '''get abs path of all files under current directory. Folders are ignored.'''
    return [join(rootdir, f) for f in listdir(rootdir) if isfile(join(rootdir, f))]

def getFileInResursive(rootdir: str, all_file_list: list)->list:
    '''get abs path of all files under current directory including files in sub folders.'''
    for f in listdir(rootdir):
        if isfile(join(rootdir, f)):
            all_file_list.append(join(rootdir, f))
        else:
            getFileInResursive(join(rootdir, f), all_file_list)
    return all_file_list

def getFileList(walk_mode: str, rootdir: str)->list:
    logger = logging.getLogger(__name__)
    allfiles_list = []
    match walk_mode:
        case "r":
            logger.info("retrieving files in recursive mode")
            allfiles_list = getFileInResursive(rootdir,[])
        case "currdir":
            logger.info("retrieving files in current directory")
            allfiles_list = getFileInCurrDir(rootdir)
        case _:
            raise Exception("Invalid OS walk mode")
    return allfiles_list



if __name__=="__main__": 
    print()



'''
def findFileByExtensionOSwalkDeterminer(os_walk_mode: str)->bool:
    return_val = False
    logger = logging.getLogger(__name__)
    match os_walk_mode:
        case "r":
            return_val = True
            logger.info("matching files recursively")
        case "currdir":
            logger.info("matching files in current directory")
        case _:
            raise Exception("Invalid OS walk mode")    
    print(return_val)
    return return_val
        

def findFileByExtension(rootdir: str, ext: str, os_walk_mode: str = 'currdir')->list:
    pattern = '**/*' + ext
    return iglob(rootdir + pattern, recursive=findFileByExtensionOSwalkDeterminer(os_walk_mode))
'''