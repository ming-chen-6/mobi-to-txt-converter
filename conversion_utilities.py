import logging
import html2text




def htmlToTxt(htmldir, mode: str = "r", encoding: str = "utf8"):
    '''a helper function that reads a html file and returns a converted text as str,
       and a bool indicating if job is successful.
    '''
    logger = logging.getLogger(__name__)
    convert_result = ""
    job_success = False
    try:
        with open(htmldir, mode = mode, encoding = encoding) as f:  # read converted html
            data = f.read()
            logging.debug(f"\n===========\n ### CONVERTED HTML ### \n===========\n {data}")
            convert_result = html2text.html2text(data)  # convert html to text
            job_success = True
    except Exception as e:
       logger.error(f"Failed to write to file: {e}")
    return job_success, convert_result
    
def saveAsTxt(txt_data, target_path: str, mode: str = "w+", encoding: str = "utf8") -> bool:
    '''a helper function that saves string to txt file 
       and returns a bool indicating if job is successful.
    '''
    job_success = False
    logger = logging.getLogger(__name__)
    try:
        with open(target_path, mode = mode, encoding = encoding) as f:
            f.write(txt_data)
        job_success = True
    except Exception as e:
        logger.error(f"Failed to write to file: {e}")
    return job_success    


# read mobi file and convert to html 
#   cont to next job if fail
# read html file
# convert to txt 
#   cont to next job if fail
# save data as txt
#   cont to next job if fail