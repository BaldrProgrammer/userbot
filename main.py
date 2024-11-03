from funcs import get_video, generate_text
from pyrogram import Client, filters
from pyrogram.enums import ParseMode, ChatType
from pyrogram.types import ChatPermissions
from pyrogram.handlers import MessageHandler
from datetime import datetime
from dotenv import load_dotenv
import importlib
import json
import time
import os

load_dotenv()
api_id = os.getenv('API_KEY')
api_hash = os.getenv('API_HASH')

app = Client('account', api_id, api_hash)

# ИМЯ ТВОИХ МОДУЛЕЙ ДОБАВЛЯТЬ СЮДА
import_files = ['handlers']
for file in import_files:
    module = importlib.import_module('your_modules.' + file)
    funcs = dir(module)
    for func in funcs:
        if not '__' in func:
            app.add_handler(MessageHandler(getattr(module, func), filters.command('start')))


@app.on_message(filters.regex(r'^\.бот'))
def bot(client, message):
    client.send_message(message.chat.id, 'Работает.')


@app.on_message(filters.regex(r'^\.сид'))
def cid(client, message):
    client.send_message(message.chat.id, f'`{message.chat.id}`', parse_mode=ParseMode.MARKDOWN)


@app.on_message(filters.regex(r'^\.пп'))
def newpasswd(client, message):
    print('хуй')
    if message.from_user.id == client.get_me().id:
        args = message.text.split()
        with open('storage/passwords.json', 'r', encoding='utf-8') as file:
            passwords = json.loads(file.read())
        passwords[args[1]] = args[2]
        passwords = json.dumps(passwords, indent=4)
        with open('storage/passwords.json', 'w', encoding='utf-8') as file:
            file.write(passwords)
        client.send_message(message.chat.id, f'Создан/перезаписан пароль {args[1]} на "{args[2]}"')


@app.on_message(filters.regex(r'^\.мп'))
def delpasswd(client, message):
    if message.from_user.id == client.get_me().id:
        args = message.text.split()
        with open('storage/passwords.json', 'r', encoding='utf-8') as file:
            passwords = json.loads(file.read())
        if args[1] in passwords:
            del passwords[args[1]]
            passwords = json.dumps(passwords, indent=4)
            with open('storage/passwords.json', 'w', encoding='utf-8') as file:
                file.write(passwords)
            client.send_message(message.chat.id, f'Пароль {args[1]} удалён.')
        else:
            client.send_message(message.chat.id, 'Такого пароля не сохранено.')


@app.on_message(filters.regex(r'^\.п'))
def passwd(client, message):
    if message.from_user.id == client.get_me().id:
        args = message.text.split()
        with open('storage/passwords.json', 'r', encoding='utf-8') as file:
            passwords = json.loads(file.read())
        if len(args) == 1:
            text = 'Вот список ключей по которым доступны ваши пароли:\n'
            for password in passwords:
                text += f'`{password}`' + '\n'
            client.send_message(message.chat.id, text, parse_mode=ParseMode.MARKDOWN)
        else:
            password = args[1]
            client.send_message(message.chat.id, f'`{passwords[password]}`', parse_mode=ParseMode.MARKDOWN)


@app.on_message(filters.regex(r'^\.бан'))
def ban(client, message):
    cid = message.chat.id
    uid = message.from_user.id
    if uid == client.get_me().id:
        user_status = client.get_chat_member(cid, uid)
        if user_status.privileges.can_restrict_members:
            if message.reply_to_message:
                client.ban_chat_member(cid, message.reply_to_message.from_user.id)


@app.on_message(filters.regex(r'^\.разбан'))
def unban(client, message):
    cid = message.chat.id
    uid = message.from_user.id
    if uid == client.get_me().id:
        user_status = client.get_chat_member(cid, uid)
        if user_status.privileges.can_restrict_members:
            if message.reply_to_message:
                client.unban_chat_member(cid, message.reply_to_message.from_user.id)
            else:
                args = message.text.split()
                if len(args) != 1:
                    client.unban_chat_member(cid, args[1])


@app.on_message(filters.regex(r'^\.мут'))
def mute(client, message):
    cid = message.chat.id
    uid = message.from_user.id
    args = message.text.split()
    if uid == client.get_me().id:
        user_status = client.get_chat_member(cid, uid)
        if user_status.privileges.can_restrict_members:
            if message.reply_to_message:
                id_to_mute = message.reply_to_message.from_user.id
            else:
                id_to_mute = args[3]
            times = {
                'с': 1,
                'м': 60,
                'ч': 3600,
                'д': 86400,
                'н': 604800
            }
            time_now = time.time()
            time_arg = int(args[1])
            time_how = args[2]
            if time_how in times:
                client.restrict_chat_member(cid, id_to_mute,
                                            permissions=ChatPermissions(can_send_messages=False),
                                            until_date=datetime.fromtimestamp(time_now + time_arg * times[time_how]))


@app.on_message(filters.regex(r'^\.размут'))
def unmute(client, message):
    cid = message.chat.id
    uid = message.from_user.id
    if uid == client.get_me().id:
        user_status = client.get_chat_member(cid, uid)
        if user_status.privileges.can_restrict_members:
            if message.reply_to_message:
                client.restrict_chat_member(cid, message.reply_to_message.from_user.id,
                                            permissions=ChatPermissions(can_send_messages=True))
            else:
                args = message.text.split()
                if len(args) != 1:
                    client.restrict_chat_member(cid, args[3], permissions=ChatPermissions(can_send_messages=True))


@app.on_message(filters.regex(r'\.скачать'))
def install(client, message):
    cid = message.chat.id
    args = message.text.split()
    print(args)
    url = args[1]
    get_video(url)
    client.send_video(cid, 'cache/video.mp4')
    os.remove('cache/video.mp4')
    if os.path.exists('cache/video'):
        os.remove('cache/video')


@app.on_message(filters.regex(r'\.гпт'))
def gpt(client, message):
    cid = message.chat.id
    args = message.text.split()
    del args[0]
    prompt = ' '.join(args)
    text = generate_text(prompt)
    client.send_message(cid, text)


@app.on_message(filters.regex(r'\.автоответчик'))
def autoanswer(client, message):
    cid = message.chat.id
    phrase = ' '.join(message.text.split(' ')[1:])
    if phrase == 'выключить':
        phrase = None
    with open('storage/config.json', 'r', encoding='utf-8') as file:
        config = json.loads(file.read())
    config['autoanswer'] = phrase
    with open('storage/config.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(config, indent=2))


@app.on_message()
async def any_message(client, message):
    cid = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        history = [message async for message in client.get_chat_history(cid, limit=2)]
        if message.from_user.id == (await client.get_me()).id:
            if len(history) == 1:
                with open('storage/config.json', 'r', encoding='utf-8') as file:
                    config = json.loads(file.read())
                if config['autoanswer']:
                    await client.send_message(cid, config['autoanswer'])


app.run()
