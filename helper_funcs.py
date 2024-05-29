import logging

from os.path import splitext
from sys import exit as sysexit

def fileIsMobi(curr_filename:str):
    '''find if extension of a file is .mobi'''
    return True if getExtension(curr_filename) == ".mobi" else False

def getExtension(curr_filepath):
    '''get extension of a file'''
    return splitext(curr_filepath)[1]

def getNoExtensionPath(curr_filepath):
    '''get file path without extension'''
    return splitext(curr_filepath)[0]

def sysExitHelper(exit_message: str = ""):
    logger = logging.getLogger(__name__)
    if exit_message != "":
        logger.info(exit_message)
    _ = input("Press Any Key to EXIT") 
    sysexit()

if __name__=="__main__": 
    print()