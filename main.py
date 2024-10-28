from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import json

api_id = '25836426'
api_hash = '23fb31c8eea83588c3894a30cda72f7f'

app = Client('account', api_id, api_hash)


@app.on_message(filters.regex(r'^\.бот'))
def cid(client, message):
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

app.run()
