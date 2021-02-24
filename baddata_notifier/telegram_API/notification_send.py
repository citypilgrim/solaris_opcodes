# imports
import telegram as tel

from ...global_imports.smmpl_opcodes import *


# params
_msgprepend = f'''
Message Type: Equipment Status
Equipment: {LIDARNAME}
'''


# relv func
def _getusefulfeedback_f(feedback):
    chat = feedback['chat']
    ret_d = {
        'date': feedback['date'],
        'receiver_id': chat['id'],
        'receiver_user': chat['username'],
    }
    return ret_d


# main func
def main(msg, receiverid):
    '''
    prepends meta info about the message and sends the message

    Return
        feedback (dict): feedbackoutput from the tel.Bot.send_message method,
                         one element for each user
    '''
    bot = tel.Bot(token=BOTTOKEN)

    feedback = bot.send_message(
        chat_id=receiverid,
        text=(_msgprepend + msg),
        parse_mode=tel.ParseMode.HTML
    )
    return _getusefulfeedback_f(feedback)


# testing
if __name__ == '__main__':

    msg = \
        '''
<pre>
|B|Code | OP    | CP    | %   |
|-|-----|-------|-------|-----|
|{:1}|{:5}|{:6.4f}|{:6.4f}|{:4.1f}|
        </pre>
        '''.format(
            '', 'RDS', 25.97488, 25.974,  100,
        )
    msg = 'quick fire'

    for feedback in main(msg):
        print(feedback)
