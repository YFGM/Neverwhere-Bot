import willie.module
import re
import datetime
import time
import os

import sys
sys.path.append("home/willie/Neverwhere-Bot")
os.environ["DJANGO_SETTINGS_MODULE"] = "Neverwhere.settings"
import Neverwherebot.interface

nicks = {}


@willie.module.commands('checknick')
def checknick(bot, trigger):
    if not check_nick(bot, str(trigger.nick)):
        bot.say("Please register your nick with NickServ.")
    else:
        bot.say("Nick ok!")


@willie.module.commands('test')
def test(bot, trigger):
    bot.say("Test!")


@willie.module.event('NOTICE')
@willie.module.rule('(.*)')
@willie.module.priority('low')
def listen_nickserv(bot, trigger):
    if not trigger.sender == "NickServ":
        return
    if trigger.startswith('STATUS'):
        bot.msg('#neverwhere-debug', text="STATUS found")
        w = re.compile('\w+').findall(trigger)
        bot.msg('#neverwhere-debug', text=str(w))
        if int(w[2]) == 3:
            nicks[str(w[1])] = datetime.datetime.now()
            bot.msg('#neverwhere-debug', text="STATUS for user %s updated." % w[1])
        else:
            return False


def check_nick(bot, nick):
    bot.msg('NickServ', "STATUS " + nick)
    bot.msg('#neverwhere-debug', text="STATUS for user %s sent to NickServ." % nick)
    time.sleep(1.5)
    if nick in nicks:
        if (datetime.datetime.now() - nicks[nick]).seconds < 10:
            return True
        else:
            return False
    else:
        return False