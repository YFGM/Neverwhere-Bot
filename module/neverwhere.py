import willie.module
import re
import datetime
import time
import sys

sys.path.append("/home/willie/Neverwhere-Bot")
sys.path.append("/home/willie/Neverwhere-Bot/Neverwherebot")
import Neverwherebot.interface as interface

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


@willie.module.commands('register')
def register(bot, trigger):
    if not check_nick(bot, str(trigger.nick)):
        bot.say("Please register your nick with NickServ.")
        return
    debug(bot, "User %s ok, registering." % str(trigger.nick))
    s = interface.register(str(trigger.nick))
    if isinstance(s, basestring):
        bot.say(s)
        return
    bot.say("User %s succesfully registered." % str(trigger.nick))


@willie.module.commands("sendmessage")
@willie.module.commands("sendm")
def send_message(bot, trigger):
    if not check_nick(bot, str(trigger.nick) or not check_user(trigger.nick)):
        bot.say("Please register your nick to use this function.")
        return
    if trigger.group(2) is not None:
        args = re.compile('\w+').findall(trigger.group(2))
    else:
        bot.say("Usage: !sendmessage RECEIVER MESSAGE")
        return
    if len(args) < 2:
        bot.say("Usage: !sendmessage RECEIVER MESSAGE")
        return
    debug(bot, "Sending message '%s' from user %s to user %s." % (trigger.group(2)[len(args[0])+1:], str(trigger.nick), args[0]))
    s = interface.send_message(str(trigger.nick), args[0], trigger.group(2)[len(args[0])+1:])
    if isinstance(s, basestring):
        bot.say(s)
        return
    bot.say("Message sent.")


# TODO: Add a unique ID to messages to make it less stupid, add telling you if it's read or not
@willie.module.commands("showmessages")
@willie.module.commands("showm")
def show_messages(bot, trigger):
    messages = interface.get_messages(str(trigger.nick))
    unread = 0
    for m in messages:
        if not m[3]:
            unread += 1
    bot.msg(trigger.nick, "You have %i messages, %i unread. To view a complete message, use !viewm MESSAGE_ID. To "
                          "delete a message, use !deletem MESSAGE_ID." % (
        len(messages),
        unread,
    ))
    count = 1
    for m in messages:
        res = ("Message %i " % count) + ("from '" + m[0] + "':") + m[4][:100]
        if len(m[4]) > 100:
            res += "..."
        bot.msg(trigger.nick, res)
        count += 1


@willie.module.commands("viewmessage")
@willie.module.commands("viewm")
def view_message(bot, trigger):
    if not trigger.group(2).isdigit():
        bot.msg(trigger.nick, "Message ID must be a number.")
    messages = interface.get_messages(str(trigger.nick))
    if not int(trigger.group(2)) <= len(messages):
        bot.msg(trigger.nick, "No message with that ID.")
    m = messages[int(trigger.group(2))]
    bot.msg(trigger.nick, "Message %i from %s. Sent %s" % (int(trigger.group(2)), m[0], m[2]))
    bot.msg(trigger.nick, m[4])


@willie.module.commands("argshow")
def show_args(bot, trigger):
    s = trigger.group(0)
    bot.say("Group 0: " + s)
    s = trigger.group(1)
    bot.say("Group 1: " + s)
    s = trigger.group(2)
    bot.say("Group 2: " + s)


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


def check_user(nick):
    return interface.is_user(nick)


def debug(bot, text):
    bot.msg('#neverwhere-debug', text=text)