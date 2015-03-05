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

# TODO: Make a better RegEx that can handle - and _

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
    bot.reply("Current character successfully set.")


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
        args = str(trigger.group(2)).split()
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
        args = str(trigger.group(2)).split()
    else:
        bot.reply("Usage: !storage COMMAND ARGUMENTS")
        return
    
    if args[0] == "create":
        if len(args) == 3 and args[1] is not None and args[2] is not None and args[2].isdigit():
            if args[1] in ["create", "allow", "description", "store", "move", "disallow", "steal", "delete", "remove",
                           "resize", "transfer", "upgrade", "self", "get"]:
                bot.reply("Invalid name.")
                return
            s = interface.create_storage(interface.get_current_character(str(trigger.nick)), str(args[1]), int(args[2]))
            if isinstance(s, basestring):
                bot.say(s)
                return
            bot.reply("Storage %s successfully created!" % str(args[1]))
            return
        else:
            bot.reply("Usage: !storage create NAME SIZE")
            return
            
    elif args[0] == "description":
        if len(args) > 2 and args[1] is not None and args[2] is not None:
            storage = interface.get_storage(args[1])
            if not str(trigger.nick) == storage["owner"]:
                bot.reply("You don't own this storage.")
                return
            if storage["inventory"]:
                bot.reply("This storage is an inventory and cannot be edited.")
                return
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
        
    elif args[0] == "allow":
        if len(args) == 3:
            storage = interface.get_storage(args[1])
            if isinstance(storage, basestring):
                bot.say(storage)
                return
            if not interface.get_current_character(str(trigger.nick)) == storage["owner"]:
                bot.reply("You don't own this storage.")
                return
            if storage["inventory"]:
                bot.reply("This storage is an inventory and cannot be edited.")
                return
            s = interface.storage_allow(args[2], args[1])
            if isinstance(s, basestring):
                bot.say(s)
                return
            bot.reply("Character succesfully added to allowed list.")
            return
        else:
            bot.reply("Usage: !storage allow STORAGE CHARACTER")
            
    elif args[0] == "disallow":
        if len(args) == 3:
            storage = interface.get_storage(args[1])
            if isinstance(storage, basestring):
                bot.say(storage)
                return
            if not interface.get_current_character(str(trigger.nick)) == storage["owner"]:
                bot.reply("You don't own this storage.")
                return
            if storage["inventory"]:
                bot.reply("This storage is an inventory and cannot be edited.")
                return
            s = interface.storage_disallow(args[2], args[1])
            if isinstance(s, basestring):
                bot.say(s)
                return
            bot.reply("Character successfully removed from allowed list.")
        else:
            bot.reply("Usage: !storage disallow STORAGE CHARACTER")
            
    elif args[0] == "resize":
        if len(args) == 3:
            storage = interface.get_storage(args[1])
            if isinstance(storage, basestring):
                bot.say(storage)
                return
            if not interface.get_current_character(str(trigger.nick)) == storage["owner"]:
                bot.reply("You don't own this storage.")
                return
            if storage["inventory"]:
                bot.reply("This storage is an inventory and cannot be edited.")
                return
            s = interface.storage_resize(args[1], int(args[2]))
            if isinstance(s, basestring):
                bot.say(s)
                return
            bot.reply("Storage successfully resized.")
        else:
            bot.reply("Usage: !storage resize STORAGE SIZE")
            
    elif args[0] == "store":
        if len(args) > 2:
            storage = interface.get_storage(args[1])
            if isinstance(storage, basestring):
                bot.say(storage)
                return
            if not interface.get_current_character(str(trigger.nick)) in storage["allowed"] and not interface.get_current_character(str(trigger.nick)) in storage["owner"]:
                bot.reply("You aren't allowed to store items in this storage.")
                return
            if storage["inventory"]:
                bot.reply("This storage is an inventory, you cannot store things" \
                          " in it. Use !give to give an item to a character " \
                          "instead.")
                return
            
            if len(args) == 3:
                s = interface.store(interface.get_current_character(str(trigger.nick)),
                                    args[1], args[2], 1.0)
                if isinstance(s, basestring):
                    if s == "No item of that type in storage.":
                        s = "No item of that type in your inventory."
                    bot.say(s)
                    return
            else:
                try:
                    amount = float(args[3])
                except:
                    bot.reply("Amount must be a number.")
                    return
                s = interface.store(interface.get_current_character(str(trigger.nick)),
                                    args[1], args[2], amount)
                if isinstance(s, basestring):
                    if s == "No item of that type in storage.":
                        s = "No item of that type in your inventory."
                    bot.say(s)
                    return
                
            bot.reply("Stored %g%s of %s into storage %s successfully." % (float(s), interface.get_item_type(args[2])["unit"], 
                                                                    args[2], args[1]))
        else:
            bot.reply("Usage: !storage store STORAGE ITEM [AMOUNT]")
    
    elif args[0] == "move" or args[0] == "get":
        if len(args) > 2:
            storage = interface.get_storage(args[1])
            if isinstance(storage, basestring):
                bot.say(storage)
                return
            if not interface.get_current_character(str(trigger.nick)) in storage["allowed"] and not interface.get_current_character(str(trigger.nick)) in storage["owner"]:
                bot.reply("You aren't allowed to retrieve items from this storage.")
                return
            if storage["inventory"]:
                bot.reply("This storage is an inventory, you cannot retrieve things" \
                          " in it. Use !give to give an item to a character " \
                          "instead.")
                return
            if len(args) > 4:
                dest = interface.get_storage(args[4])
                if isinstance(dest, basestring):
                    bot.say(dest)
                    return
                if not interface.get_current_character(str(trigger.nick)) in dest["allowed"] and not interface.get_current_character(str(trigger.nick)) in dest["owner"]:
                    bot.reply("You aren't allowed to store items in this storage.")
                    return
                if dest["inventory"]:
                    bot.reply("This storage is an inventory, you cannot store things" \
                              " in it. Use !give to give an item to a character " \
                              "instead.")
                    return
            
            if len(args) == 3:
                s = interface.move(args[1],
                                    args[2], 1.0, interface.get_current_character(str(trigger.nick)) + "-Inventory")
                amount = 1.0
                if isinstance(s, basestring):
                    if s == "Not enough room left in the storage.":
                        s = "Not enough room left in your inventory."
                    bot.say(s)
                    return
            elif len(args) == 4:
                try:
                    amount = float(args[3])
                except:
                    bot.reply("Amount must be a number.")
                    return
                s = interface.move(args[1],
                                    args[2], amount, interface.get_current_character(str(trigger.nick)) + "-Inventory")
                if isinstance(s, basestring):
                    if s == "Not enough room left in the storage.":
                        s = "Not enough room left in your inventory."
                    bot.say(s)
                    return
                
            elif len(args) > 4:
                try:
                    amount = float(args[3])
                except:
                    bot.reply("Amount must be a number.")
                    return
                s = interface.move(args[1],
                                    args[2], amount, args[4])
                if isinstance(s, basestring):
                    bot.say(s)
                    return 
            if len(args) > 4:
                bot.reply("Successfully moved %g%s of %s to storage %s." % (amount, interface.get_item_type(args[2])["unit"], 
                                                                        args[2], args[4]))
            else:
                bot.reply("Successfully moved %g%s of %s to your inventory." % (amount, interface.get_item_type(args[2])["unit"], 
                                                                        args[2]))
        else:
            bot.reply("Usage: !storage move STORAGE ITEM [AMOUNT] [DESTINATION]")
        
    elif args[0] == "delete":
        if len(args) > 1:
            storage = interface.get_storage(args[1])
            if isinstance(storage, basestring):
                bot.say(storage)
                return
            if not interface.get_current_character(str(trigger.nick)) in storage["owner"]:
                bot.reply("You don't own this storage.")
                return
            if storage["inventory"]:
                bot.reply("This storage is an inventory and cannot be deleted.")
                return
            s = interface.storage_delete(args[1])
            if isinstance(s, basestring):
                    bot.say(s)
                    return 
            bot.reply("Storage %s successfully deleted." % args[1])
        else:
            bot.reply("Usage: !storage delete STORAGE")
            
    elif args[0] == "steal":
        bot.reply("Stealing is currently not implemented, sorry!")
        
    elif args[0] == "transfer":
        if len(args) > 1:
            storage = interface.get_storage(args[1])
            if isinstance(storage, basestring):
                bot.say(storage)
                return
            if not interface.get_current_character(str(trigger.nick)) in storage["owner"]:
                bot.reply("You don't own this storage.")
                return
            if storage["inventory"]:
                bot.reply("This storage is an inventory and cannot be transferred.")
                return
            s = interface.storage_transfer(args[1], args[2])
            if isinstance(s, basestring):
                    bot.say(s)
                    return 
            bot.reply("Storage %s ownership transferred to %s." % (args[1], args[2]))
        else:
            bot.reply("Usage: !storage transfer STORAGE CHARACTER")
            
    # TODO
    elif args[0] == "upgrade":
        bot.reply("Upgrading is TODO.")
            
    else:
        d = interface.get_storage(args[0])
        c = interface.get_storage_contents(args[0])
        debug(bot, str(d))
        debug(bot, str(c))


@willie.module.commands("worksite")
def worksite(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.reply("Please register your nick to use this function.")
        return
    if trigger.group(2) is not None:
        args = str(trigger.group(2)).split()
    else:
        bot.reply("Usage: !worksite COMMAND ARGUMENTS")
        return
    
    if args[0] == "create":
        if len(args) > 3:
            if args[2] in ["create", "delete", "description", "changestorage", 
                           "add", "upgrade", "hire", "fire", "salary", "createjob"]:
                bot.reply("Invalid name.")
                return
            s = interface.worksite_create(interface.get_current_character(str(trigger.nick)), args[1], args[2], args[3])
            if isinstance(s, basestring):
                    bot.reply(s)
                    return
            bot.reply("Worksite %s successfully created!" % args[2])
        else:
            bot.reply("Usage: !worksite create TYPE NAME STORAGE")
        
    elif args[0] == "delete":
        if len(args) > 1:
            w = interface.get_worksite(args[1])
            if not isinstance(w, dict):
                bot.reply(w)
                return
            if interface.get_current_character(str(trigger.nick)) != w["owner"]:
                bot.reply("You don't own this worksite.")
                return
            s = interface.delete_worksite(args[1])
            if isinstance(s, basestring):
                    bot.reply(s)
                    return
            bot.reply("Worksite %s succesfully deleted." % args[1])
        else:
            bot.reply("Usage: !worksite delete NAME")
    
    elif args[0] == "description":
        if len(args) > 2:
            w = interface.get_worksite(args[1])
            if not isinstance(w, dict):
                bot.reply(w)
                return
            if interface.get_current_character(str(trigger.nick)) != w["owner"]:
                bot.reply("You don't own this worksite.")
                return
            desc = ""
            for i in range(2, len(args)):
                desc += args[i]
                if i != len(args) - 1:
                    desc += " "
            s = interface.worksite_description(args[1], desc)
            if isinstance(s, basestring):
                    bot.reply(s)
                    return
            bot.reply("Worksite %s's description successfully set." % args[1])
        else:
            bot.reply("Usage: !worksite description NAME DESCRIPTION")
        
    elif args[0] == "changestorage":
        if len(args) > 2:
            w = interface.get_worksite(args[1])
            if not isinstance(w, dict):
                bot.reply(w)
                return
            if interface.get_current_character(str(trigger.nick)) != w["owner"]:
                bot.reply("You don't own this worksite.")
                return
            s = interface.worksite_changestorage(args[1], args[2])
            if isinstance(s, basestring):
                    bot.reply(s)
                    return
            bot.reply("Worksite %s's storage successfully changed to %s." % (args[1], args[2]))
        else:
            bot.reply("Usage: !worksite changestorage WORKSITE_NAME STORAGE_NAME")
            
    elif args[0] == "add":
        if len(args) > 2:
            a = interface.get_acre(args[2])
            if not isinstance(a, dict):
                bot.reply(a)
                return
            if interface.get_current_character(str(trigger.nick)) != a["owner"]:
                bot.reply("You don't own this acre.")
                return
            s = interface.worksite_add(args[1], args[2])
            if isinstance(s, basestring):
                bot.reply(s)
                return
            bot.reply("Acre %s successfully added to worksite %s." % (args[2], args[1]))
        else:
            bot.reply("Usage: !worksite add NAME ACRE_ID")
        
    elif args[0] == "upgrade":
        if len(args) > 2:
            w = interface.get_worksite(args[1])
            if not isinstance(w, dict):
                bot.reply(w)
                return
            if interface.get_current_character(str(trigger.nick)) != w["owner"]:
                bot.reply("You don't own this worksite.")
                return
            u = interface.get_upgrade(args[2])
            if not isinstance(u, dict):
                bot.reply(u)
                return
            i = interface.remove_item(u["item"], interface.get_current_character(str(trigger.nick)) + "-Inventory", 1.0)
            if isinstance(i, basestring):
                if i == "No item of that type in storage.":
                    i = "The required item for this upgrade was not found in your inventory."
                bot.reply(i)
                
            if i != 1.0:
                s = interface.add_item(u["item"], interface.get_current_character(str(trigger.nick)) + "-Inventory", i)
                if isinstance(s, basestring):
                    bot.reply(s)
                    return
                bot.reply("Failed to remove 1 of the necessary upgrade item. This is a bug.")
                return
            s = interface.worksite_upgrade(args[1], args[2])
            if isinstance(s, basestring):
                    bot.reply(s)
                    return
            bot.reply("Upgrade successfully applied.")
        else:
            bot.reply("Usage: !worksite upgrade NAME UPGRADE")
            
    elif args[0] == "hire":
        if len(args) == 4:
            w = interface.get_worksite(args[1])
            if not isinstance(w, dict):
                bot.reply(w)
                return
            if interface.get_current_character(str(trigger.nick)) != w["owner"]:
                bot.reply("You don't own this worksite.")
                return
            s = interface.worksite_hire(args[1], args[2], args[3])
            if isinstance(s, basestring):
                    bot.reply(s)
                    return
            bot.reply("You have hired %s as a %s at your worksite %s." % (args[2], args[3], args[1]))
        if len(args) > 4:
            if args[4] == "p" or args[4] == "-p":
                w = interface.get_worksite(args[1])
                if not isinstance(w, dict):
                    bot.reply(w)
                    return
                if interface.get_current_character(str(trigger.nick)) != w["owner"]:
                    bot.reply("You don't own this worksite.")
                    return
                s = interface.worksite_hire(args[1], args[2], args[3], parttime=True)
                if isinstance(s, basestring):
                        bot.reply(s)
                        return
                bot.reply("You have hired %s as a %s at your worksite %s." % (args[2], args[3], args[1]))
        else:
            bot.reply("Usage: !worksite hire WORKSITE_NAME CHARACTER_NAME JOB_NAME [-p]")
                
    elif args[0] == "fire":
        if len(args) == 3:
            w = interface.get_worksite(args[1])
            if not isinstance(w, dict):
                bot.reply(w)
                return
            if interface.get_current_character(str(trigger.nick)) != w["owner"]:
                bot.reply("You don't own this worksite.")
                return
            s = interface.worksite_fire(args[1], args[2])
            if isinstance(s, basestring):
                bot.reply(s)
                return
            bot.reply("You have fired %s from %s." % (args[2], args[1]))
        else:
            bot.reply("Usage: !worksite fire WORKSITE_NAME CHARACTER_NAME")
            
    elif args[0] == "salary":
        if len(args) == 4:
            w = interface.get_worksite(args[1])
            if not isinstance(w, dict):
                bot.reply(w)
                return
            if interface.get_current_character(str(trigger.nick)) != w["owner"]:
                bot.reply("You don't own this worksite.")
                return
            if not args[3].isdigit():
                bot.reply("Amount must be a number.")
                return
            s = interface.worksite_salary(args[1], args[2], int(args[3]))
            if isinstance(s, basestring):
                bot.reply(s)
                return
            bot.reply("Successfully set salary of job %s at worksite %s to %s." % (args[2], args[1], args[3]))
        else:
            bot.reply("Usage: !worksite salary WORKSITE_NAME JOB_NAME AMOUNT")
            
    elif args[0] == "createjob":
        if len(args) == 3:
            w = interface.get_worksite(args[1])
            if not isinstance(w, dict):
                bot.reply(w)
                return
            if interface.get_current_character(str(trigger.nick)) != w["owner"]:
                bot.reply("You don't own this worksite.")
                return
            s = interface.create_job(args[1], args[2])
            if isinstance(s, basestring):
                bot.reply(s)
                return
            bot.reply("Succesfully created %s job at worksite %s." % (args[2], args[1]))
        else:
            bot.reply("Usage: !worksite createjob WORKSITE_NAME JOB_NAME")
            
        
    else:
        debug(bot, str(interface.get_worksite(args[0])))


@willie.module.commands("job")
def job(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.reply("Please register your nick to use this function.")
        return
    if trigger.group(2) is not None:
        args = str(trigger.group(2)).split()
    else:
        bot.reply("Usage: !job COMMAND ARGUMENTS")
        return
    
    if args[0] == "apply":
        if len(args) == 3:
            s = interface.apply_job(args[1], args[2], interface.get_current_character(str(trigger.nick)))
            if isinstance(s, basestring):
                bot.reply(s)
                return
            bot.reply("You are now working at %s." % args[1])
        elif len(args) == 4 and (args[3] == "p" or args[3] == "-p"):
            s = interface.apply_job(args[1], args[2], interface.get_current_character(str(trigger.nick)), parttime=True)
            if isinstance(s, basestring):
                bot.reply(s)
                return
            bot.reply("You are now working at %s part time." % args[1])
        else:
            bot.reply("Usage: !job apply WORKSITE_NAME JOB_NAME [-p]")
            
    elif args[0] == "remapply":
        if len(args) == 2:
            s = interface.remove_apply(interface.get_current_character(str(trigger.nick)), args[1])
            if isinstance(s, basestring):
                bot.reply(s)
                return
            bot.reply("Successfully removed all applications to %s." % args[1])
        else:
            bot.reply("Usage: !job remapply WORKSITE_NAME")
                      
    elif args[0] == "quit":
        if len(args) == 1:
            s = interface.quit_job(interface.get_current_character(str(trigger.nick)))
            if isinstance(s, basestring):
                bot.reply(s)
                return
            bot.reply("Successfully quit your job(s).")
            
        elif len(args) == 2 and args[1].isdigit():
            s = interface.quit_job(interface.get_current_character(str(trigger.nick)), int(args[1]))
            if isinstance(s, basestring):
                bot.reply(s)
                return
            bot.reply("Successfully quit your job.")
        else:
            bot.reply("Usage: !job quit [JOB]")
            
    else:
        debug(bot, str(interface.get_job(args[0])))


@willie.module.commands("additem")
@willie.module.commands("addi")
def add_item(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.reply("Please register your nick to use this function.")
        return
    if trigger.group(2) is not None:
        args = str(trigger.group(2)).split()
    else:
        bot.reply("Usage: !addi STORAGE ITEM [AMOUNT]")
        return
    if len(args) < 2:
        bot.reply("Usage: !addi STORAGE ITEM [AMOUNT]")
        return
    storage = interface.get_storage(args[0])
    if isinstance(storage, basestring):
        bot.say(storage)
        return
    if not interface.get_current_character(str(trigger.nick)) == storage["owner"]:
        bot.reply("You don't own this storage.")
        return
    if len(args) == 2:
        amount = 1.0
        s = interface.add_item(args[1], args[0], 1.0)
    else:
        try:
            amount = float(args[2])
        except:
            bot.reply("Amount must be a number.")
            return
        s = interface.add_item(args[1], args[0], amount)
        
    if isinstance(s, basestring):
        bot.say(s)
        return
    bot.reply("Successfully added %g %s to storage %s." % (amount, args[1], args[0]))
    
    
@willie.module.commands("removeitem")
@willie.module.commands("remi")
def remove_item(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        bot.reply("Please register your nick to use this function.")
        return
    if trigger.group(2) is not None:
        args = str(trigger.group(2)).split()
    else:
        bot.reply("Usage: !remi STORAGE ITEM [AMOUNT]")
        return
    if len(args) < 2:
        bot.reply("Usage: !remi STORAGE ITEM [AMOUNT]")
        return
    storage = interface.get_storage(args[0])
    if not interface.get_current_character(str(trigger.nick)) == storage["owner"]:
        bot.reply("You don't own this storage.")
        return
    if len(args) == 2:
        s = interface.remove_item(args[1], args[0], 1.0)
        amount = 1.0
        if isinstance(s, basestring):
            bot.say(s)
            return
    else:
        try:
            amount = float(args[2])
        except:
            bot.reply("Amount must be a number.")
            return
        s = interface.remove_item(args[1], args[0], amount)
        if isinstance(s, basestring):
            bot.say(s)
            return
    bot.reply("Removed %g%s of %s from storage %s successfully." % (s, interface.get_item_type(args[1])["unit"], 
                                                                    args[1], args[0]))


@willie.module.commands("tick")
def tick(bot, trigger):
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick) or str(trigger.nick) != "YFGM":
        bot.reply("Admin only function.")
        return
    if trigger.group(2) is not None:
        args = str(trigger.group(2)).split()
    else:
        bot.reply("Parameter must be a number.")
        return
    if len(args) > 0 and not args[0].isdigit():
        bot.reply("Parameter must be a number.")
        return
    
    for i in range(int(args[0])):
        t = interface.get_time()
        debug(bot, "Ticking hour %i of day %i." % (t["hour"], t["day"]))
        interface.tick()

@willie.module.commands("argshow")
def show_args(bot, trigger):
    s = trigger.group(0)
    bot.say("Group 0: " + s)
    s = trigger.group(1)
    bot.say("Group 1: " + s)
    s = trigger.group(2)
    bot.say("Group 2: " + s)

news = "Welcome to the Neverwherebot Testing Channels. Why don't you try our latest functions (if you get a NoneType error, try using !setc): " \
        "!worksite create, !worksite description, !worksite delete, !worksite changestorage, !worksite add, !worksite upgrade (non functional atm)" \
        ", !worksite hire, !worksite fire, !worksite salary, !worksite createjob, !job apply, !job remapply and !job quit. For some info, see the first " \
        "few sections of http://pastebin.com/gMmCBJbs (Everything in here is WIP)."

@willie.module.event('JOIN')
@willie.module.rule('.*')
@willie.module.priority('low')
def on_join(bot, trigger):
    news = "Welcome to the Neverwherebot Testing Channels. Why don't you try our latest functions (if you get a NoneType error, try using !setc): " \
        "!worksite create, !worksite description, !worksite delete, !worksite changestorage, !worksite add, !worksite upgrade (non functional atm)" \
        ", !worksite hire, !worksite fire, !worksite salary, !worksite createjob, !job apply, !job remapply and !job quit. For some info, see the first " \
        "few sections of:"
    paste = "http://pastebin.com/gMmCBJbs (Everything in here is WIP)."
    if not check_nick(bot, str(trigger.nick)) or not check_user(trigger.nick):
        return
    bot.msg(trigger.nick, "Welcome back %s!" % str(trigger.nick))
    bot.msg(trigger.nick, news)
    bot.msg(trigger.nick, paste)
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
    

@willie.module.commands("news")
def news(bot, trigger):
    news = "Welcome to the Neverwherebot Testing Channels. Why don't you try our latest functions (if you get a NoneType error, try using !setc): " \
        "!worksite create, !worksite description, !worksite delete, !worksite changestorage, !worksite add, !worksite upgrade (non functional atm)" \
        ", !worksite hire, !worksite fire, !worksite salary, !worksite createjob, !job apply, !job remapply and !job quit. For some info, see the first " \
        "few sections of:"
    paste = "http://pastebin.com/gMmCBJbs (Everything in here is WIP)."
    bot.say(news)
    bot.say(paste)

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