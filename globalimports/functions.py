# imports
from functools import wraps
from glob import glob
import os.path as osp
import re
import sys

import numpy as np

from ._modifications import *


def haltlogging(func):
    '''
    Halts redirection of stdout and stderr logfiles and outputs to __stdout__ and
    __stderr__
    '''
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        oldstdout_logdir = sys.stdout.name
        oldstderr_logdir = sys.stderr.name
        SETLOGFN()
        ret = func(*args, **kwargs)
        SETLOGFN(oldstdout_logdir, oldstderr_logdir)
        return ret
    return wrapper_func


# defining functions

def FINDFILESFN(ufmtfilename, directories, *fieldsd):
    '''
    finds files in the stated directory using glob of a wildcard expression of the
    unformatted filename

    Parameters
        ufmtfilename (str): filename unformatted field entries
        directories (str or list of strings): directories we are searching in
        fieldsd (dict): contains fields in which we want to fill with entries,
                        leaving wild card for all other unspecified entries
                        keys are field indexes, values are the field inputs

    Return
        list of file directories with the expression fiven in filename
    '''
    # filling in fields if specified
    try:
        fieldsd = fieldsd[0]
        field_l, del_l = DIRPARSEFN(ufmtfilename, retdelimboo=True)
        for key, value in fieldsd.items():
            field_l[key] = field_l[key].format(value)
        filename = ''.join([x for y in zip(del_l, field_l) for x in y])
    except IndexError:
        filename = ufmtfilename

    # replacing fields with asterisk
    filename = re.sub('{.*?}', '*', filename)

    # finding files
    if type(directories) in [list, np.ndarray]:
        return np.concatenate(
            [glob(DIRCONFN(dire, filename)) for dire in directories], axis=0
        )
    else:
        return glob(DIRCONFN(directories, filename))


def DIRPARSEFN(
        dirstr=None, fieldsli=slice(None), delimiters='(\W|_)', retdelimboo=False
):
    '''
    parenthesis in delimeters garantees that we are keeping the delimeters

    Parameters
        dirstr (str or array of str): for parsing, can also parse array of strings
        fieldsli (int or slice): returns fields specified
        delimeter (str): has to follow the requirements of re.split
        retdelimboo (boolean): decides whether or not to return delimeters

    Return
        dirstr (str) -> parsed string [, parsed strings]
        dirstr (array like) -> list of parsed strings [, list of parsed strings]
        dirstr (None) -> function to be used as key for sorting or mapping
    '''
    # params
    fmtspecflag = 'FORMATSPECIFIERFLAG'

    # operations
    if type(dirstr) in [list, np.ndarray]:
        try:
            return np.vectorize(DIRPARSEFN)(
                dirstr, fieldsli, delimiters, retdelimboo
            )
        except ValueError:
            raise ValueError('when working with arrays of strings, fieldsli must'
                             f' be an integer index, right now {fieldsli=}')
    elif not dirstr:
        return lambda x: DIRPARSEFN(x, fieldsli, delimiters)
    else:
        dirstr = osp.basename(dirstr)
        # first replace format specifiers to something else before splitting
        fmtspec_l = re.findall('{.*?}', dirstr)
        dirstr = re.sub('{.*?}', fmtspecflag, dirstr)
        field_l = re.split(delimiters, dirstr)
        # replace back the format specifiers after splitting
        field_l = [
            re.sub(fmtspecflag, fmtspec_l.pop(0), fielde)
            if fmtspecflag in fielde
            else fielde
            for fielde in field_l
        ]
        # parsing
        try:
            del_l = [''] + field_l[1::2]  # first field has no delimeter
        except IndexError:                # single field string
            del_l = ['']
        field_l = field_l[::2]
        if retdelimboo:
            return field_l[fieldsli], del_l[fieldsli]
        else:
            return field_l[fieldsli]


def DIRCONFN(*dirl):
    '''
    Windows friendly directory concat function. Works exactly as os.path.join
    in linux.
    Here we assume that the directories are delimited by '/'

    Parameters
        dirl (list): list of path strings
    '''
    path = ''
    for i, dirstr in enumerate(dirl):
        if i == 0:
            path += dirstr
        else:

            if dirstr[0] == '/':    # start anew if argument starts with root
                path = dirstr
            else:
                if path[-1] == '/':
                    path += dirstr
                else:
                    path += '/' + dirstr
    return path


def SETLOGFN(stdoutlog=None, stderrlog=None):
    if stdoutlog:               # setting new logfile
        SETLOGFN()
        if stdoutlog != '<stdout>':
            sys.stdout = open(stdoutlog, 'a+')
        if stderrlog != '<stderr>':
            if stderrlog:
                sys.stderr = open(stderrlog, 'a+')
            else:
                sys.stderr = open(stdoutlog, 'a+')
    else:           # resets the stdout and stderr to go sys default
        if sys.stdout.name != '<stdout>':
            sys.stdout.close()
        if sys.stderr.name != '<stderr>':
            sys.stderr.close()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


@haltlogging
def GETRESPONSEFN(message, exitboo, twiceboo, checkboo=False, prevmsg=None):
    '''
    input function can only be used on main thread.
    Keeps prompting for response until it is a definite yes or no

    Parameters
        message (str): prompting string
        exitboo (boolean): decides whether or not to exit when response is 'n'
        twiceboo (boolean): prompts a second time if response == 'y'
        checkboo (boolean): determines whether or not the prompt is from the
                            second check, managed by recursive nature
        prevmsg (str): original prompt message, managed by recursive nature

    Return
        ret (boolean): True -> response was 'y'
                       False -> response was 'n'
    '''
    while True:
        response = input(message + ' y or n\n')
        if response == 'y':
            if twiceboo:
                return GETRESPONSEFN('Are you sure?', exitboo, False,
                                     True, message)
            else:
                return True
        elif response == 'n':
            if exitboo and not checkboo:
                sys.exit(0)         # exits without error
            elif not exitboo and not checkboo:
                return False
            elif checkboo:      # repeats the original prompt
                return GETRESPONSEFN(prevmsg, exitboo, True)
        else:
            print('Enter either y or n\n')


# testing
if __name__ == '__main__':

    teststr = '{1:2}_{}_{!@}_dsa.txt'
    print(DIRPARSEFN([teststr, teststr], fieldsli=2, retdelimboo=True))
    # print(DIRPARSEFN(teststr))
