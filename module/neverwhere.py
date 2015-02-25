import willie.module
import re
import datetime
import time
import Neverwherebot.interface as interface

nicks = {}


@willie.module.commands('register')
def register(bot, trigger):
    if not check_nick:
        bot.say("Please register your nick with NickServ.")
    else:
        bot.say("Nick ok!")


@willie.module.commands('test')
def test(bot, trigger):
    bot.say("Test!")


@willie.module.rule('(.*)')
@willie.module.priority('low')
def listen_nickserv(bot, nick):
    if not trigger.sender == "NickServ":
        return
    if trigger.startswith('STATUS'):
        bot.debug(text="STATUS found", level='always')
        w = re.compile('\w+').findall(trigger)
        if w[2] == 3:
            nicks[w[1]] = datetime.datetime.now()
            bot.debug(text="STATUS for user %s updated." % nick, level='always')
        else:
            return False


def check_nick(bot, nick):
    bot.msg('NickServ', "STATUS " + nick)
    bot.debug(text="STATUS for user %s sent to NickServ." % nick, level='always')
    time.sleep(1)
    if (datetime.datetime.now() - nicks[nick]).seconds < 10:
        return True
    else:
        return False