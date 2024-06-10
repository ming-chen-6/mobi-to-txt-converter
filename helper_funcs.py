from os.path import splitext
from sys import exit as sysexit


def attentionMsgStrBuilder(message_str: str)->str:
    '''
    add ### at front and end of input string, and a line with \n=========...\n 
    of the same length as decorated input string before and after it.
    '''
    number_sign_added_str = "### " + message_str + " ###"
    dashes_with_newline = "\n" + "="*len(number_sign_added_str) + "\n"
    return dashes_with_newline + number_sign_added_str + dashes_with_newline

def fileIsMobi(curr_filename:str)->bool:
    '''find if extension of a file is .mobi'''
    return True if getExtension(curr_filename) == ".mobi" else False

def getExtension(curr_filepath):
    '''get extension of a file'''
    return splitext(curr_filepath)[1]

def getNoExtensionPath(curr_filepath):
    '''get file path without extension'''
    return splitext(curr_filepath)[0]

def sysExitHelper():
    '''Press Any Key to EXIT with sys.exit'''
    _ = input("Press Any Key to EXIT") 
    sysexit()



if __name__=="__main__": 
    print()