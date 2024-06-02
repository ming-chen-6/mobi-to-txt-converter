import logging
import html2text

def htmlToTxt(htmldir, mode: str = "r", encoding: str = "utf8"):
     '''a helper function that reads a html file and returns a converted txt file as str'''
     with open(htmldir, mode = mode, encoding = encoding) as f:  # read converted html
        data = f.read()
        logging.debug(f"\n===========\n ### CONVERTED HTML ### \n===========\n {data}")
        convert_result = html2text.html2text(data)  # convert html to text
    
def saveTxt(html_data, target_path: str, mode: str = "w+", encoding: str = "utf8") -> bool:
    job_success = True
    logger = logging.getLogger(__name__)
    try:
        with open(target_path, mode = mode, encoding = encoding) as f:
            f.write(html_data)
    except Exception as e:
        job_success = False
        logger.error(f"Failed to write to file: {e}")
    return job_success    
