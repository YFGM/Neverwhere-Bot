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

# TODO: If user is already registered
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
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
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
    if len(messages) < 1:
        bot.msg(trigger.nick, "You currently have no messages.")
        return
    if isinstance(messages, basestring):
        bot.say(messages)
        return
    unread = 0
    for m in messages:
        if not m[3]:
            unread += 1
    bot.msg(trigger.nick, "You have %i messages, %i unread. To view a complete message, use !viewm MESSAGE_ID. To "
                          "delete a message, use !deletem MESSAGE_ID." % (
        len(messages),
        unread,
    ))
    for m in messages:
        res = ("Message %i " % m[5]) + ("from '" + m[0] + "':") + m[4][:100]
        if len(m[4]) > 100:
            res += "..."
        bot.msg(trigger.nick, res)

# TODO: Set message as read.
@willie.module.commands("viewmessage")
@willie.module.commands("viewm")
def view_message(bot, trigger):
    if trigger.group(2) is None:
        bot.msg(trigger.nick, "Message ID must be a number.")
        return
    if not trigger.group(2).isdigit():
        bot.msg(trigger.nick, "Message ID must be a number.")
        return
    messages = interface.get_messages(str(trigger.nick))
    for m in messages:
        if m[5] == int(trigger.group(2)):
            bot.msg(trigger.nick, "Message %i from %s. Sent %s" % (int(trigger.group(2)), m[0], m[2]))
            bot.msg(trigger.nick, m[4])
            return
    bot.msg(trigger.nick, "No message with that ID.")


@willie.module.commands("create")
def create_character(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.say("Please register your nick to use this function.")
        return
    if trigger.group(2) is not None:
        args = re.compile('\w+').findall(trigger.group(2))
    else:
        bot.say("Usage: !create NAME SEX STR DEX INT VIT")
        return
    if len(args) != 6:
        bot.say("Usage: !create NAME SEX STR DEX INT VIT")
        return
    if not isinstance(args[0], basestring) or not isinstance(args[1], basestring) or not args[2].isdigit() or not args[3].isdigit() or not args[4].isdigit() or not args[5].isdigit():
        bot.say("Usage: !create NAME SEX STR DEX INT VIT")
        return
    debug(bot, "Creating character using: " + str(args))
    s = interface.create_character(str(trigger.nick), str(args[0]), str(args[1]), int(args[2]), int(args[3]), int(args[4]), int(args[5]))
    if isinstance(s, basestring):
        bot.say(s)
        return
    bot.say("Character %s succesfully created." % str(args[0]))


@willie.module.commands("show")
def show_character(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.say("Please register your nick to use this function.")
        return
    if trigger.group(2) is not None:
        args = re.compile('\w+').findall(trigger.group(2))
    else:
        bot.say("Usage: !show CHARACTER")
        return
    char = interface.get_character(str(trigger.group(2)))
    if isinstance(char, basestring):
        bot.say(char)
        return
    desc = []
    if char["sex"].lower() == "f":
        gender = "Female"
    else:
        gender = "Male"
    prefixes = {}
    if char["mab"] >= 0:
        prefixes["mab"] = "+"
    else:
        prefixes["mab"] = ""
    if char["rab"] >= 0:
        prefixes["rab"] = "+"
    else:
        prefixes["rab"] = ""
    if char["will"] >= 0:
        prefixes["rab"] = "+"
    else:
        prefixes["rab"] = ""
    if char["will"] >= 0:
        prefixes["will"] = "+"
    else:
        prefixes["will"] = ""
    if char["re"] >= 0:
        prefixes["re"] = "+"
    else:
        prefixes["re"] = ""
    if char["fort"] >= 0:
        prefixes["fort"] = "+"
    else:
        prefixes["fort"] = ""
    if char["per"] >= 0:
        prefixes["per"] = "+"
    else:
        prefixes["per"] = ""
    desc.append(str(trigger.group(2)) + ", " + gender + " Human")
    desc.append("%i Str %i Dex %i Int %i Vit" % (char["str"], char["dex"], char["int"], char["vit"]))
    desc.append("%i/%i HP %i/%i FP %i/%i SAN" % (char["hp"], char["current_hp"], char["fp"], char["current_fp"],
                                                    char["san"], char["current_san"]))
    desc.append("%s%i MAB %s%i RAB %i AC" % (prefixes["mab"], char["mab"], prefixes["rab"], char["rab"], char["ac"]))
    desc.append("%s%i Will %s%i Re %s%i Fort" % (prefixes["will"], char["will"], prefixes["re"], char["re"], prefixes["fort"], char["fort"]))
    desc.append("%s%i Per %i Mo %d BL" % (prefixes["per"], char["per"], char["mo"], char["bl"]))
    desc.append("Perks: WIP")
    desc.append("Skills: WIP")
    desc.append("Spells: WIP")
    for i in range(len(desc)):
        bot.say(desc[i])





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
        debug(bot, "STATUS found")
        w = re.compile('\w+').findall(trigger)
        debug(bot, str(w))
        if int(w[2]) == 3:
            nicks[str(w[1])] = datetime.datetime.now()
            debug(bot, "STATUS for user %s updated." % w[1])
        else:
            return False


def check_nick(bot, nick):
    bot.msg('NickServ', "STATUS " + nick)
    debug(bot, "STATUS request for user %s sent to NickServ." % nick)
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