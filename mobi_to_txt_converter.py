import logging

from os import listdir, getcwd, makedirs
from pprint import pformat, pprint

from helper_funcs import fileIsMobi, getNoExtensionPath, sysExitHelper, attentionMsgStrBuilder
from get_file_list import getFileList
from conversion_utilities import mobiToTxt

alowed_os_walk_mode = ['currdir','r']

def main():     
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    os_walk_mode = 'r'
    root_dir = getcwd()
    converted_file_save_mode = "together"
    encoding = "utf8"

    # set file list, quit if no mobi file found
    all_file_list = getFileList(os_walk_mode, root_dir)
    logging.debug("All files in directory:\n" + pformat(all_file_list))

    # list all mobi files
    cleaned_mobi_list = [f for f in all_file_list if fileIsMobi(f)]
    
    # exit if no mobi file found
    if len(cleaned_mobi_list) == 0:
        logging.info("\n\nNo Mobi File Found!")
        sysExitHelper()
    
    # showing all mobi files found
    logging.info("\n" + str(len(cleaned_mobi_list)) + " mobi files found:\n"+pformat(cleaned_mobi_list))    

    logging.info(attentionMsgStrBuilder("Start Converting Files"))
    # conversion loop
    for curr_file_path in cleaned_mobi_list:
        logging.info(f"Converting File {curr_file_path}")
        mobiToTxt(curr_file_path, root_dir, os_walk_mode, encoding, converted_file_save_mode)
        logging.info(f"Conversion finished.")
    logging.info(attentionMsgStrBuilder("All Conversion Jobs Finished."))
    sysExitHelper()



if __name__=="__main__": 
    main() 