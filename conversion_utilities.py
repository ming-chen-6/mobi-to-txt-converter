import mobi
import time
import logging
import html2text

from os import makedirs
from shutil import rmtree
from os.path import join, dirname, basename

from helper_funcs import attentionMsgStrBuilder, getNoExtensionPath

def mobiToTxt(mobi_path, root_dir, encoding:str = "utf8", save_path_mode:str = "together", **kwargs)->bool:
    '''
    a helper function that convert mobi file at mobi_path to txt file by converting
    mobit firstly to html and convert html to txt. 
    '''
    logger = logging.getLogger(__name__)
    if mobi_path in kwargs:
        mobi_path = kwargs["mobi_path"]
    if root_dir in kwargs:
        root_dir = kwargs["root_dir"]
    if encoding in kwargs:
        encoding = kwargs["encoding"]
    if save_path_mode in kwargs:
        save_path_mode = kwargs["save_path_mode"]
    
    logger.debug(f"start extracting html from mobi.")
    try:
        tempdir = mobi.extract(mobi_path)[0]    # extract file and get temp file path
    except Exception as e:
        logger.error(f"Failed to convert mobi to html for file {mobi_path} \n{e}")    # return false if job fail
        logger.error(f"Job aborted due to mobi to html conversion failure.")
        return False 
    logger.debug(f"finished extracting html from mobi file.")

    logger.debug(f"start converting html to text.")
    htmldir = join(tempdir, 'mobi7','book.html')    # join path to get html file path
    logger.debug(f"html temp file root: {tempdir}")
    logger.debug(f"html temp file path: {htmldir}")
    html2txt_success, txt_data = htmlToTxt(htmldir, encoding = encoding)    # convert html to txt file
    if not html2txt_success:    
        logger.error(f"Job aborted due to html to txt conversion failure.")     # return false if job fail
        return False
    logger.debug(f"finished converting html file to txt file.")

    logger.debug(f"start saving txt file.")
    save_path = getSavePath(mobi_path, root_dir, save_path_mode)
    savetxt_success = saveAsTxt(txt_data, save_path, "w+", encoding)
    if not savetxt_success:
        logger.error(f"Job aborted due to txt file writing failure.")     # return false if job fail
        return False
    logger.debug(f"finished saving txt file.")

    logger.debug(f"start removing temp file.")      # remove temp files after job is done
    try:
        rmtree(tempdir)
        logger.debug(f"finished removing temp file.")
    except Exception as e:
        logger.error(f"Failed to remove temp files at {tempdir} \n{e}")  
        logger.error(f"Program continues without removing temp files.")

    return True


def htmlToTxt(htmldir, encoding: str = "utf8"):
    '''
    a helper function that reads a html file and returns a converted text as str,
    and a bool indicating if job is successful.
    '''
    logger = logging.getLogger(__name__)
    file_read_mode: str = "r"
    conversion_result = ""
    job_success = False
    try:
        logger.debug("opening html file")
        with open(htmldir, mode = file_read_mode, encoding = encoding) as f:  # read converted html
            data = f.read()
            logger.debug("finished reading html file")
            conversion_result = html2text.html2text(data)  # convert html to text
            att_str = attentionMsgStrBuilder("CONVERTED TEXT")
            logger.debug(f"{att_str} \n{data}")
            job_success = True
    except Exception as e:
       logger.error(f"Failed to convert html to txt for file {htmldir} \n{e}")
    return job_success, conversion_result


def getSavePath(file_path:str, root_dir:str, save_path_mode:str = "together") -> str:
    ''' a helper function that returns abs path of the txt file to be saved. '''
    logger = logging.getLogger(__name__)
    match save_path_mode:
        case "together" | "t":
            file_name = basename(file_path)
            txt_name = getNoExtensionPath(file_name) + '.txt'
            save_path = join(root_dir, "converted_files", txt_name)
            logger.debug(f"save file in one folder. File path {save_path}")
        case "same as file" | "saf":
            save_path = getNoExtensionPath(file_path) + '.txt'
            logger.debug(f"save file in the same folder as original file. File path {save_path}")
        case _:
            raise Exception("Invalid save path mode")
    return save_path


def saveAsTxt(txt_data, target_path: str, write_mode: str = "w+", encoding: str = "utf8") -> bool:
    '''
    a helper function that saves string to txt file and returns a bool 
    indicating if job is successful.
    '''
    job_success = False
    logger = logging.getLogger(__name__)
    try:
        logger.debug("make new directory to save file")
        makedirs(dirname(target_path), exist_ok=True)
        logger.debug("opening file for writing")
        with open(target_path, mode = write_mode, encoding = encoding) as f:
            f.write(txt_data)
        job_success = True
        logger.debug(f"wite finished. File saved with path {target_path}")
    except Exception as e:
        logger.error(f"Failed to write to file: {e}")
    return job_success    


if __name__=="__main__": 
    print()

