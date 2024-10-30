from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import ChatPermissions
import json
import time

api_id = '25836426'
api_hash = '23fb31c8eea83588c3894a30cda72f7f'

app = Client('account', api_id, api_hash)


@app.on_message(filters.regex(r'^\.бот'))
def bot(client, message):
    client.send_message(message.chat.id, 'Работает.')


@app.on_message(filters.regex(r'^\.сид'))
def cid(client, message):
    client.send_message(message.chat.id, f'`{message.chat.id}`', parse_mode=ParseMode.MARKDOWN)


@app.on_message(filters.regex(r'^\.\+пароль'))
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


@app.on_message(filters.regex(r'^\.\-пароль'))
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


@app.on_message(filters.regex(r'^\.пароль'))
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
            time_arg = args[1]
            time_how = args[2]
            if time_how in times:
                client.restrict_chat_member(cid, id_to_mute,
                                            permissions=ChatPermissions(can_send_messages=False),
                                            until_date=time_now + time_arg * times[time_how])


app.run()
