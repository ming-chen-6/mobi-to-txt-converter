import logging
import mobi
import html2text

from os import listdir, getcwd, makedirs
from helper_funcs import attentionMsgStrBuilder
from os.path import isfile, join, dirname, basename
from sys import exit as sysexit
from helper_funcs import fileIsMobi, getNoExtensionPath

from get_file_list import getFileList

# read mobi file and convert to html 
#   cont to next job if fail
# read html file
# convert to txt 
#   cont to next job if fail
# save data as txt
#   cont to next job if fail
def mobiToTxt(mobi_path, oswalk_mode:str = "currdir", encoding:str = "utf8", save_path_mode:str = "together")->bool:
    logger = logging.getLogger(__name__)
    mobi_path = mobi_path
    oswalk_mode = oswalk_mode
    encoding = encoding
    save_path_mode = save_path_mode

    try:
        tempdir = mobi.extract(mobi_path)[0]    # extract file and get temp file path
    except Exception as e:
        logger.error(f"Failed to convert mobi to html for file {htmldir} \n{e}")    # return false if job fail
        logger.error(f"Job aborted due to mobi to html conversion failure.")
        return False 
    logger.debug(f"finished extracting mobi file as html file")

    htmldir = join(tempdir, 'mobi7','book.html')    # join path to get html file path
    logger.debug(f"html temp file root: {tempdir}")
    logger.debug(f"html temp file path: {htmldir}")
    html2txt_success, txt_data = htmlToTxt(htmldir, oswalk_mode, encoding)    # convert html to txt file
    if not html2txt_success:    
        logger.error(f"Job aborted due to html to txt conversion failure.")     # return false if job fail
        return False
    logger.debug(f"finished converting html file to txt file")

    save_path = getSavePath(mobi_path, save_path_mode)
    savetxt_success = saveAsTxt(txt_data, save_path, "w+", encoding)
    if not savetxt_success:
        logger.error(f"Job aborted due to txt file writing failure.")     # return false if job fail
        return False
    logger.debug(f"finished saving txt file")
    # to-do: remove tempfiles 

    return True


def htmlToTxt(htmldir, mode: str = "r", encoding: str = "utf8"):
    '''
    a helper function that reads a html file and returns a converted text as str,
    and a bool indicating if job is successful.
    '''
    logger = logging.getLogger(__name__)
    conversion_result = ""
    job_success = False
    try:
        with open(htmldir, mode = mode, encoding = encoding) as f:  # read converted html
            data = f.read()
            conversion_result = html2text.html2text(data)  # convert html to text
            logger.debug(f"{attentionMsgStrBuilder("CONVERTED TEXT")}\n{data}")
            job_success = True
    except Exception as e:
       logger.error(f"Failed to convert html to txt for file {htmldir} \n{e}")
    return job_success, conversion_result


def getSavePath(file_path:str, save_path_mode:str = "together") -> str:
    logger = logging.getLogger(__name__)
    match save_path_mode:
        case "together" | "t":
            working_directory = getcwd()        # note: since cwd is always the same, could change to global var to reduce repeated work
            file_name = basename(file_path)
            txt_name = getNoExtensionPath(file_name) + '.txt'
            save_path = join(working_directory, "converted-files", txt_name)
            logger.debug(f"save file in one folder. File path {save_path}")
        case "same as file" | "saf":
            save_path = getNoExtensionPath(file_path) + '.txt'
            logger.debug(f"save file in the same folder as original file. File path {save_path}")
        case _:
            raise Exception("Invalid save path mode")
    return save_path


def saveAsTxt(txt_data, target_path: str, mode: str = "w+", encoding: str = "utf8") -> bool:
    '''
    a helper function that saves string to txt file and returns a bool 
    indicating if job is successful.
    '''
    job_success = False
    logger = logging.getLogger(__name__)
    try:
        with open(target_path, mode = mode, encoding = encoding) as f:
            f.write(txt_data)
        job_success = True
        logger.debug(f"file saved with path {target_path}")
    except Exception as e:
        logger.error(f"Failed to write to file: {e}")
    return job_success    


if __name__=="__main__": 
    print()
