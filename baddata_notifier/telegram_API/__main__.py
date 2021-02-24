# imports
import datetime as dt
import multiprocessing as mp

import telegram as tel

from .notification_send import main as notification_send
from ...global_imports.smmpl_opcodes import *


# params
_exception_t = (
    tel.error.TimedOut,
)


# relv func
def _keeptrysnend_f(msg, receiverid):
    retrycounter = 0
    while True:
        retrycounter += 1
        if retrycounter >= SENDRETRYTHRES:
            print('{:%Y%m%d%H%M} failed to send message to {}:'.format(
                dt.datetime.now(), receiverid
            ))
            print('\n'.join(['\t' + line for line in msg.split('\n')]))
            break
        try:
            notification_send(msg, receiverid)
        except _exception_t as e:
            continue
        break


# main func
@verbose
@announcer(newlineboo=True)
def main(msg):

    # sending message to each receiver_id
    sendfail_l = []             # list of failed telegram IDs
    for receiverid in RECEIVERIDS:
        print(f'sending to {receiverid}')
        try:
            feedback = notification_send(msg, receiverid)
            for key, val in feedback.items():
                print(f'\t{key}: {val}')
        except _exception_t as e:
            print(f'failed to send to {receiverid}')
            sendfail_l.append(receiverid)

    # starting child process for each sending retry attempt
    for sendfail in sendfail_l:
        print(f'starting child process to retry sending for {sendfail}')
        mp.Process(target=_keeptrysnend_f, args=(msg, receiverid)).start()


# testing
if __name__ == '__main__':
    msg = 'quickfire test'
    main(msg)
