# imports
from functools import wraps
import sys

from ._modifications import *


# defining decorators for global functions
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

import datetime as dt
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
    # from .params import *

    # print('{}'.format(DIRCONFN(WINDOWFILESDIR, SEDFILE)))

    # Process class
    import multiprocessing as mp
    class _procwrapper(mp.Process):
        '''
        To be used in a way similar to multiprocessing.Process.
        It logs the print statements in the specified logfiles
        '''
        def __init__(self, logfile, target, args=(), kwargs={}):
            print(
                '{:%Y%m%d%H%M} run {}.{}...'.
                format(dt.datetime.now(), target.__module__, target.__name__)
            )
            super().__init__(target=target, args=args, kwargs=kwargs)
            self.logfile = logfile

        def run(self):
            '''
            This runs on self.start() in a new process
            '''
            SETLOGFN(self.logfile)
            if self._target:
                self._target(*self._args, **self._kwargs)
            SETLOGFN()

    mainlog = 'C:/Users/mpluser/Desktop/mainlog.txt'
    print('main func is running')
    SETLOGFN(mainlog)
    def play_func():
        print('play_func')
    pplay_func = _procwrapper(
        'C:/Users/mpluser/Desktop/playfunc.txt', play_func
    )
    pplay_func.start()
    pplay_func.join()

    SETLOGFN('C:/Users/mpluser/Desktop/sublog.txt')
    print('pretend sub func is running')
    GETRESPONSEFN('this is a test?', True, True)
    SETLOGFN(mainlog)
    print('main func is running', flush=True)
    import time
    time.sleep(10)
