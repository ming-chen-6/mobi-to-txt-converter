import mobi
import html2text
import logging

from os import listdir, getcwd, makedirs
from os.path import isfile, join, dirname
from pprint import pformat, pprint
from sys import exit as sysexit

from helper_funcs import fileIsMobi, getNoExtensionPath, sysExitHelper
from get_file_list import getFileList

alowed_os_walk_mode = ['currdir','r']

def main():     
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    os_walk_mode = 'currdir'
    rootdir = getcwd()

    # set file list, quit if no mobi file found
    all_file_list = getFileList(os_walk_mode, rootdir)
    logging.debug("All files in directory:\n" + pformat(all_file_list))

    # list all mobi files
    cleaned_mobi_list = [f for f in all_file_list if fileIsMobi(f)]
    
    # exit if no mobi file found
    if len(cleaned_mobi_list) == 0:
        logging.info("\n\nNo Mobi File Found!")
        sysExitHelper()
    
    logging.info("\nMobi Files found:\n"+pformat(cleaned_mobi_list))    

    logging.info("\n======================\nStart Converting Files\n======================")
    # conversion loop
    for curr_filename in cleaned_mobi_list:
        logging.info(f"Converting File {curr_filename}")
        tempdir, filepath = mobi.extract(curr_filename)  # extract file and get temp file path
        logging.debug(tempdir)
        temp_htmldir = join(tempdir, 'mobi7','book.html')
        logging.debug(temp_htmldir)

        with open(temp_htmldir, mode="r", encoding="utf8") as f:  # read converted html
            data = f.read()
            logging.debug(f"\n===========\n ### CONVERTED HTML ### \n===========\n {data}")
        
        convert_result = html2text.html2text(data)  # convert html to text
        logging.debug(f"\n===========\n ### CONVERTED TEXT ### \n===========\n {convert_result}")
        
        # create target dir for writing
        curr_name = getNoExtensionPath(curr_filename)
        txt_filename = curr_name + '.txt'
        curr_path = getcwd()
        target_path = join(curr_path,"converted-files",txt_filename)
        logging.debug(f"target path: {target_path}")
        makedirs(dirname(target_path), exist_ok=True)
        # write to file
        with open(target_path, mode="w+", encoding="utf8") as f:
            f.write(convert_result)
        logging.info("Finished")   
    logging.info("\n============================\nAll Conversion Jobs Complete\n============================")

    sysExitHelper()



if __name__=="__main__": 
    main() 