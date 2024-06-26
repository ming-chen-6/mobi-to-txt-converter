import logging

from os import listdir
from os.path import isfile, join


def getFileInCurrDir(rootdir: str)->list:
    '''get abs path of all files under current directory. Subfolders are ignored.'''
    return [join(rootdir, f) for f in listdir(rootdir) if isfile(join(rootdir, f))]

def getFileResursive(rootdir: str, all_file_list: list)->list:
    '''get abs path of all files under current directory including files in subfolders.'''
    for f in listdir(rootdir):
        if isfile(join(rootdir, f)):
            all_file_list.append(join(rootdir, f))
        else:
            getFileResursive(join(rootdir, f), all_file_list)
    return all_file_list

def getFileList(walk_mode: str, rootdir: str)->list:
    '''get abs path of all files based on walk_mode. 
         walk_mode = "currdir": Subfolders are ignored.
         walk_mode = "r": Subfolder files are included.
    '''
    logger = logging.getLogger(__name__)
    allfiles_list = []
    match walk_mode:
        case "r":
            logger.info("retrieving files in recursive mode")
            allfiles_list = getFileResursive(rootdir,[])
        case "currdir":
            logger.info("retrieving files in current directory")
            allfiles_list = getFileInCurrDir(rootdir)
        case _:
            raise Exception("Invalid OS walk mode")
    return allfiles_list



if __name__=="__main__": 
    print()
