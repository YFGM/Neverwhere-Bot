import willie.module
import re
import datetime
import time
import sys
import humanize
from slugify import slugify

sys.path.append("/home/willie/Neverwhere-Bot")
sys.path.append("/home/willie/Neverwhere-Bot/Neverwherebot")
import Neverwherebot.interface as interface

nicks = {}


@willie.module.commands('checknick')
def checknick(bot, trigger):
    if not check_nick(bot, str(trigger.nick)):
        bot.reply("Please register your nick with NickServ.")
    else:
        bot.reply("Nick ok!")


@willie.module.commands('test')
def test(bot, trigger):
    bot.reply("Test!")


@willie.module.commands('register')
def register(bot, trigger):
    if not check_nick(bot, str(trigger.nick)):
        bot.reply("Please register your nick with NickServ.")
        return
    if check_user(str(trigger.nick)):
        bot.reply("You are already registered.")
        return
    s = interface.register(str(trigger.nick))
    if isinstance(s, basestring):
        bot.say(s)
        return
    bot.say("User %s succesfully registered." % str(trigger.nick))


@willie.module.commands("sendmessage")
@willie.module.commands("sendm")
def send_message(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.reply("Please register your nick to use this function.")
        return
    if trigger.group(2) is not None:
        args = re.compile('\w+').findall(trigger.group(2))
    else:
        bot.reply("Usage: !sendmessage RECEIVER MESSAGE")
        return
    if len(args) < 2:
        bot.reply("Usage: !sendmessage RECEIVER MESSAGE")
        return
    s = interface.send_message(str(trigger.nick), args[0], trigger.group(2)[len(args[0])+1:])
    if isinstance(s, basestring):
        bot.say(s)
        return
    bot.reply("Message sent.")


@willie.module.commands("showmessages")
@willie.module.commands("showm")
def show_messages(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.reply("Please register your nick to use this function.")
        return
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
    unread = []
    read = []
    for m in messages:
        res = ("Message %i " % m[5]) + ("from '" + m[0] + "': ") + m[4][:100]
        if len(m[4]) > 100:
            res += "..."
        else:
            interface.set_message_read(m[5])
        if m[3]:
            read.append(res)
        else:
            unread.append(res)
    if len(unread) > 0:
        bot.msg(trigger.nick, "Unread:")
        for s in unread:
            bot.msg(trigger.nick, s)
    if len(read) > 0:
        bot.msg(trigger.nick, "Read:")
        for s in read:
            bot.msg(trigger.nick, s)


@willie.module.commands("viewmessage")
@willie.module.commands("viewm")
def view_message(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.reply("Please register your nick to use this function.")
        return
    if trigger.group(2) is None:
        bot.msg(trigger.nick, "Message ID must be a number.")
        return
    if not trigger.group(2).isdigit():
        bot.msg(trigger.nick, "Message ID must be a number.")
        return
    messages = interface.get_messages(str(trigger.nick))
    for m in messages:
        if m[5] == int(trigger.group(2)):
            bot.msg(trigger.nick, "Message %i from %s. Sent %s" % (int(trigger.group(2)), m[0], humanize.naturaltime(datetime.datetime.now()-m[2])))
            bot.msg(trigger.nick, m[4])
            interface.set_message_read(m[5])
            return
    bot.msg(trigger.nick, "No message with that ID.")


@willie.module.commands("deletemessage")
@willie.module.commands("delm")
@willie.module.commands("deletem")
def delete_message(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.reply("Please register your nick to use this function.")
        return
    if trigger.group(2) is None:
        bot.msg(trigger.nick, "Message ID must be a number.")
        return
    if not trigger.group(2).isdigit():
        bot.msg(trigger.nick, "Message ID must be a number.")
        return
    m = interface.get_message(int(trigger.group(2)))
    if isinstance(m, basestring):
        bot.say(m)
        return
    if not m[6] == str(trigger.nick):
        bot.reply("You don't own this message.")
        return
    interface.delete_message(int(trigger.group(2)))
    bot.msg(trigger.nick, "Message %i deleted." % int(trigger.group(2)))


@willie.module.commands("create")
def create_character(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.reply("Please register your nick to use this function.")
        return
    if trigger.group(2) is not None:
        args = re.compile('\w+').findall(trigger.group(2))
    else:
        bot.reply("Usage: !create NAME SEX STR DEX INT VIT")
        return
    if len(args) != 6:
        bot.reply("Usage: !create NAME SEX STR DEX INT VIT")
        return
    if not isinstance(args[0], basestring) or not isinstance(args[1], basestring) or not args[2].isdigit() or not args[3].isdigit() or not args[4].isdigit() or not args[5].isdigit():
        bot.reply("Usage: !create NAME SEX STR DEX INT VIT")
        return
    s = interface.create_character(str(trigger.nick), str(args[0]), str(args[1]), int(args[2]), int(args[3]), int(args[4]), int(args[5]))
    if isinstance(s, basestring):
        bot.say(s)
        return
    bot.reply("Character %s succesfully created." % str(args[0]))
    if interface.get_current_character(str(trigger.nick)) is None:
        d = interface.set_current_character(str(trigger.nick), str(args[0]))
        if isinstance(d, basestring):
            bot.reply(d)
            return


@willie.module.commands("getc")
def get_character(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.reply("Please register your nick to use this function.")
        return
    if trigger.group(2) is None:
        bot.reply("Usage: !getc CHARACTER")
        return
    char = interface.get_character(str(trigger.group(2)))
    if isinstance(char, basestring):
        bot.say(char)
        return
    debug(bot, str(char))


@willie.module.commands("setcharacter")
@willie.module.commands("setc")
def set_current_character(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.reply("Please register your nick to use this function.")
        return
    if trigger.group(2) is None:
        bot.reply("Usage: !getc CHARACTER")
        return
    args = re.compile('\w+').findall(trigger.group(2))
    if not interface.is_owner(str(trigger.nick), args[0]):
        bot.reply("You do not own that character.")
        return
    s = interface.set_current_character(str(trigger.nick), args[0])
    if isinstance(s, basestring):
        bot.say(s)
        return
    bot.reply("Current character succesfully set.")


@willie.module.commands("show")
def show_character(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.reply("Please register your nick to use this function.")
        return
    if trigger.group(2) is not None:
        args = re.compile('\w+').findall(trigger.group(2))
    else:
        bot.reply("Usage: !show CHARACTER")
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
    desc.append("\x02" + str(trigger.group(2)) + "\x0F" + ", " + gender + " Human")
    desc.append("%i \x02Str\x0F %i \x02Dex\x0F %i \x02Int\x0F %i \x02Vit\x0F" % (char["str"], char["dex"], char["int"], char["vit"]))
    desc.append("%i/%i \x02HP\x0F %i/%i \x02FP\x0F %i/%i \x02SAN\x0F" % (char["current_hp"], char["hp"], char["current_fp"], char["fp"],
                                                    char["current_san"], char["san"]))
    desc.append("%s%i \x02MAB\x0F %s%i \x02RAB\x0F %i \x02AC\x0F" % (prefixes["mab"], char["mab"], prefixes["rab"], char["rab"], char["ac"]))
    desc.append("%s%i \x02Will\x0F %s%g \x02Re\x0F %s%i \x02Fort\x0F" % (prefixes["will"], char["will"], prefixes["re"], char["re"], prefixes["fort"], char["fort"]))
    desc.append("%s%i \x02Per\x0F %i \x02Mo\x0F %g \x02BL\x0F" % (prefixes["per"], char["per"], char["mo"], char["bl"]))
    perks = ""
    for n in range(1, len(char["perks"])+1):
        perks += interface.get_perk_name(char["perks"][n])
        if n != len(char["perks"]):
            perks += ", "
    desc.append("\x02Perks\x0F: %s" % perks)
    skills = ""
    count = 1
    for k in (char["skills"]):
        s = k
        s += " "
        if not char["skills"][k] < 0:
            s += "+"
        s += str(char["skills"][k])
        if not count == len(char["skills"]):
            s += ", "
        count += 1
        skills += s
    desc.append("\x02Skills\x0F: %s" % skills)
    desc.append("\x02Spells\x0F: WIP")
    s = ""
    for i in range(0, len(desc)-3):
        s += desc[i] + ", "
    bot.say(s[:-2])
    bot.say(desc[len(desc)-3])
    bot.say(desc[len(desc)-2])
    bot.say(desc[len(desc)-1])


@willie.module.commands("addperk")
@willie.module.commands("addp")
def add_perk(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.reply("Please register your nick to use this function.")
        return
    if trigger.group(2) is not None:
        args = re.compile('\w+').findall(str(trigger.group(2)))
    else:
        bot.reply("Usage: !addperk CHARACTER PERK")
        return
    if len(args) == 1:
        bot.reply("Usage: !addperk CHARACTER PERK")
        return
    if not interface.is_owner(str(trigger.nick), args[0]):
        bot.reply("You do not own that character.")
        return
    s = ""
    for i in range(1, len(args)):
        s += args[i] + " "
    s = slugify(s)
    debug(bot, "Slug: " + s)
    r = interface.add_perk(s, args[0])
    if isinstance(r, basestring):
        bot.say(r)
        return
    bot.reply("Perk succesfully added.")
    
    
@willie.module.commands("storage")
def storage(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.reply("Please register your nick to use this function.")
        return
    if trigger.group(2) is not None:
        args = re.compile('\w+').findall(str(trigger.group(2)))
    else:
        bot.reply("Usage: !storage COMMAND ARGUMENTS")
        return
    
    if args[0] == "create":
        if len(args) == 3 and args[1] is not None and args[2] is not None and args[2].isdigit():
            if args[1] in ["create", "allow", "description", "store", "move", "disallow", "steal", "delete", "remove",
                           "resize", "transfer", "upgrade"]:
                bot.reply("Invalid name.")
                return
            s = interface.create_storage(interface.get_current_character(str(trigger.nick)), str(args[1]), int(args[2]))
            if isinstance(s, basestring):
                bot.say(s)
                return
            bot.reply("Storage %s succesfully created!" % str(args[1]))
            return
        else:
            bot.reply("Usage: !storage create NAME SIZE")
            return
            
    elif args[0] == "description":
        if len(args) > 2 and args[1] is not None and args[2] is not None:
            s = ""
            for i in range(2, len(args)):
                s += args[i] + " "
            d = interface.set_storage_description(args[1], s[:-1])
            if isinstance(d, basestring):
                bot.say(d)
                return
            bot.reply("Description successfully set!")
            return
        else:
            bot.reply("Usage: !storage description NAME DESCRIPTION")
            return
            
    else:
        d = interface.get_storage(args[0])
        debug(bot, str(d))


@willie.module.commands("argshow")
def show_args(bot, trigger):
    s = trigger.group(0)
    bot.say("Group 0: " + s)
    s = trigger.group(1)
    bot.say("Group 1: " + s)
    s = trigger.group(2)
    bot.say("Group 2: " + s)


@willie.module.event('JOIN')
@willie.module.rule('.*')
@willie.module.priority('low')
def on_join(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        return
    bot.msg(trigger.nick, "Welcome back %s!" % str(trigger.nick))
    messages = interface.get_messages(str(trigger.nick))
    if len(messages) < 1:
        bot.msg(trigger.nick, "You currently have no messages.")
        return
    if isinstance(messages, basestring):
        bot.msg(trigger.nick, messages)
        return
    unread = 0
    for m in messages:
        if not m[3]:
            unread += 1
    bot.msg(trigger.nick, "You have %i messages, %i unread. To view all messages, use !showm." % (
        len(messages),
        unread,
    ))

@willie.module.event('NOTICE')
@willie.module.rule('(.*)')
@willie.module.priority('high')
def listen_nickserv(bot, trigger):
    if not trigger.sender == "NickServ":
        return
    if trigger.startswith('STATUS'):
        w = re.compile('\w+').findall(trigger)
        if int(w[2]) == 3:
            nicks[str(w[1])] = datetime.datetime.now()
        else:
            return False


def check_nick(bot, nick):
    bot.msg('NickServ', "STATUS " + nick)
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