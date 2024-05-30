import logging
import time
import functools
from fnmatch import fnmatch

from os.path import splitext
from sys import exit as sysexit


def fileIsMobi(curr_filename:str):
    '''find if extension of a file is .mobi'''
    return True if getExtension(curr_filename) == ".py" else False
"""

def fileIsMobi(curr_filename:str):
    '''find if extension of a file is .mobi'''
    return True if fnmatch(curr_filename, '*.py') else False
"""

def getExtension(curr_filepath):
    '''get extension of a file'''
    return splitext(curr_filepath)[1]

def getNoExtensionPath(curr_filepath):
    '''get file path without extension'''
    return splitext(curr_filepath)[0]

def sysExitHelper():
    _ = input("Press Any Key to EXIT") 
    sysexit()





def timeChecker(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"Starting {func.__name__}...")
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Finished {func.__name__} in {duration:.4f} seconds.")
        return result
    return wrapper



if __name__=="__main__": 
    print()