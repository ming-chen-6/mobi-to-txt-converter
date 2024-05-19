import mobi
import html2text
import logging

from os import listdir, getcwd, makedirs
from os.path import isfile, join, dirname, splitext
from pprint import pformat
from sys import exit as sysexit

def main():     
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    # get all file name --- may add more mode in future
    allfiles_currdir = [f for f in listdir('./') if isfile(join('./', f))]
    logging.debug(f":\nAll files in dir:\n {allfiles_currdir}")

    # set file list, quit if no mobi file found
    all_file_list = allfiles_currdir
    if len(all_file_list) == 0:
        logging.info("\nNo Mobi File Found\n") 
        _ = input("Press Any Key to EXIT") 
        sysexit()

    # list all mobi files
    def endIsMobi(curr_filename:str):  # find mobi by checking last 5 char are .mobi
        if curr_filename[-5:] == ".mobi":
            return curr_filename
        return ""

    mobi_list = list(map(endIsMobi, all_file_list))
    logging.debug(f":\nPre-cleaned file list:\n {mobi_list}")
    cleaned_mobi_list = [curr_filename for curr_filename in mobi_list if curr_filename != ""]
    # cleaned_mobi_list now stores all mobi files in dir
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
        curr_name, ext = splitext(curr_filename)
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

    _ = input("Press Any Key to EXIT") 
    sysexit()


if __name__=="__main__": 
    main() 