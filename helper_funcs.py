from os.path import splitext

def fileIsMobi(curr_filename:str):
    '''find mobi by checking last 5 char are .mobi'''
    if curr_filename[-5:] == ".mobi":
        return curr_filename
    return ""

def getExtension(curr_filepath):
    '''get extension of a file'''
    ext = splitext(curr_filepath)[1]
    return ext

def getNoExtensionPath(curr_filepath):
    '''get file path without extension'''
    no_ext_path = splitext(curr_filepath)[0]
    return no_ext_path
