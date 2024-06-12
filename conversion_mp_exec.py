import mobi
import time
import html2text

from os import makedirs
from shutil import rmtree
import multiprocessing as mp
from os.path import join, dirname, basename

from helper_funcs import getNoExtensionPath


def mobiToTxtMPexec(job_list, root_dir, encoding:str = "utf8", save_path_mode:str = "together"):
    '''
    function that execute mobiToTxtMPworker in multiprocess mode.
    '''
    job_list_packed = [(j, root_dir, encoding, save_path_mode) for j in job_list]
    num_of_core = mp.cpu_count()
    print(f" Number of Workers: {num_of_core}\n")
    with mp.Pool(num_of_core) as pool:
        pool.map(mobiToTxtMPworker, job_list_packed)
    print() # this is only for print format
    return


def mobiToTxtMPworker(args)->bool:
    '''
    multiprocessing worker that does the same job as mobiToTxt. Using print() for
    logging.
    '''
    process_name = mp.current_process().name

    logging_debug_str = ""
    temp_str = f"Worker: {process_name}"
    logging_debug_str += temp_str

    mobi_path, root_dir, encoding, save_path_mode, = args

    try:
        tempdir = mobi.extract(mobi_path)[0]    # extract file and get temp file path
    except Exception as e:
        temp_str = f"\nFailed to convert mobi to html for file {mobi_path} \n{e}"    # return false if job fail
        logging_debug_str += temp_str
        temp_str = f"\nJob aborted due to mobi to html conversion failure."
        logging_debug_str += temp_str
        print(logging_debug_str)
        return False 
    
    htmldir = join(tempdir, 'mobi7','book.html')    # join path to get html file path
    temp_str = f"\n finished extracting html from mobi file with html temp file at {htmldir}"
    logging_debug_str += temp_str
    
    html2txt_success, txt_data = htmlToTxt(htmldir, encoding = encoding)    # convert html to txt file
    if not html2txt_success:    
        temp_str = f"\nJob aborted due to html to txt conversion failure."     # return false if job fail
        logging_debug_str += temp_str
        print(logging_debug_str)
        return False
    
    temp_str = f"\n finished converting html file to txt file. File at {htmldir}"
    logging_debug_str += temp_str

    save_path = getSavePath(mobi_path, root_dir, save_path_mode)
    savetxt_success = saveAsTxt(txt_data, save_path, "w+", encoding)
    if not savetxt_success:
        temp_str = f"\nJob aborted due to txt file writing to {save_path} failed."    # return false if job fail
        logging_debug_str += temp_str
        return False
    
    temp_str = f"\n finished saving txt file as {save_path}."
    logging_debug_str += temp_str

    try:
        rmtree(tempdir)    # remove temp files after job is done
        temp_str = f"\n finished removing temp file at {tempdir}."    # return false if job fail
        logging_debug_str += temp_str
    except Exception as e:
        temp_str = f"Failed to remove temp files at {tempdir} \n{e}"
        logging_debug_str += temp_str
        temp_str = "Program continues without removing temp files."
        logging_debug_str += temp_str
        print(logging_debug_str)
    
    #print(logging_debug_str)
    print(f"Worker: {process_name}\n Finished converting file {mobi_path}")
    return True


def htmlToTxt(htmldir, encoding: str = "utf8"):
    '''
    a helper function that reads a html file and returns a converted text as str,
    and a bool indicating if job is successful.
    '''
    file_read_mode: str = "r"
    conversion_result = ""
    job_success = False
    try:
        with open(htmldir, mode = file_read_mode, encoding = encoding) as f:  # read converted html
            data = f.read()
            conversion_result = html2text.html2text(data)  # convert html to text
            job_success = True
    except Exception as e:
       print(f"Failed to convert html to txt for file {htmldir} \n{e}")
    return job_success, conversion_result


def getSavePath(file_path:str, root_dir:str, save_path_mode:str = "together") -> str:
    ''' a helper function that returns abs path of the txt file to be saved. '''
    match save_path_mode:
        case "together" | "t":
            file_name = basename(file_path)
            txt_name = getNoExtensionPath(file_name) + '.txt'
            save_path = join(root_dir, "converted_files", txt_name)
        case "same as file" | "saf":
            save_path = getNoExtensionPath(file_path) + '.txt'
        case _:
            raise Exception("Invalid save path mode")
    return save_path


def saveAsTxt(txt_data, target_path: str, write_mode: str = "w+", encoding: str = "utf8") -> bool:
    '''
    a helper function that saves string to txt file and returns a bool 
    indicating if job is successful.
    '''
    job_success = False
    try:
        makedirs(dirname(target_path), exist_ok=True)
        with open(target_path, mode = write_mode, encoding = encoding) as f:
            f.write(txt_data)
        job_success = True
    except Exception as e:
        print(f"Failed to write to file: {e}")
    return job_success    


if __name__=="__main__": 
    print()
