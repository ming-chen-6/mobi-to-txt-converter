import logging

from glob import iglob
from os import listdir, getcwd, makedirs
from os.path import isfile, join, dirname


def getFileInCurrDir(rootdir: str)->list:
    '''get abs path of all files under current directory. Folders are ignored.'''
    return [join(rootdir, f) for f in listdir(rootdir) if isfile(join(rootdir, f))]

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



def getFileList(walk_mode: str, rootdir: str)->list:
    logger = logging.getLogger(__name__)
    allfiles_list = []
    match walk_mode:
        case "r":
            logger.info("retrieving files in recursive mode")
        case "currdir":
            logger.info("retrieving files in current directory")
            allfiles_list = getFileInCurrDir(rootdir)
        case _:
            raise Exception("Invalid OS walk mode")
    return allfiles_list



if __name__=="__main__": 
    print()