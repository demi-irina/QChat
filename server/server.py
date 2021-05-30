import socket
import json
import mysql.connector
import threading
import time
import hashlib
import os

try:
    import config
except:
    print("You have to create config.py from config.py.example")
    os._exit(0)

sock = socket.socket()
sock.bind(('',config.PORT))
sock.listen(config.MAX_CONN_ALLOWED)

con = mysql.connector.connect(host=config.DB_HOST, database=config.DB, user=config.USER, password=config.PASS, autocommit=True)
cur = con.cursor()

def process_message(client_sock, client_addr):
    con_t = mysql.connector.connect(host=config.DB_HOST, database=config.DB, user=config.USER, password=config.PASS, autocommit=True)
    cur_t = con_t.cursor()

    while True:

        data1 = client_sock.recv(1024).decode()

        if not data1:
            dead.append(client_addr)
            break
        try:
            data = json.loads(data1)
        except:
            continue
        if 'type' not in data.keys():
            continue

        con_t.ping()

        if data['type'] == 'name':

            if 'name' in data.keys() and 'login_time' in data.keys() and online[data['name']]['login_time'] == data['login_time']:

                online[data['name']]['time'] = time.time()
                cur_t.execute("SELECT `sender`, `text` FROM `messages` WHERE `recipient` = %s AND `status` = 0 ORDER BY `time` ASC", (data['name'], ))
                rows = cur_t.fetchall()
                if rows != []:
                    client_sock.send(json.dumps(rows).encode())
                    cur_t.execute("UPDATE `messages` SET `status` = 1 WHERE `recipient` = %s", (data['name'], ))
                else:
                    client_sock.send('EMPTY'.encode())

            else:
                continue

        elif data['type'] == 'message':

            if 'recipient' in data.keys() and 'sender' in data.keys() and 'text' in data.keys() and 'login_time' in data.keys() and online[data['sender']]['login_time'] == data['login_time']:
                cur_t.execute("INSERT INTO `messages` (`recipient`, `sender`, `text`) VALUES (%s, %s, %s)",
                        (data['recipient'], data['sender'], data['text']))
            else:
                continue

        elif data['type'] == 'user name':

            if 'name' in data.keys():
                cur_t.execute("SELECT `name` FROM `users` WHERE `name` = %s", (data['name'], ))
                rows = cur_t.fetchall()
                if not rows:
                    client_sock.send('not'.encode())
                else:
                    client_sock.send('ok'.encode())
            else:
                continue

        elif data['type'] == 'password':

            if 'name' in data.keys() and 'password' in data.keys():

                hash_object = hashlib.sha1(data['password'].encode("UTF-8"))
                hex_dig = hash_object.hexdigest()

                cur_t.execute("SELECT `password` FROM `users` WHERE `name` = %s AND `password` = %s", (data['name'], hex_dig))
                rows = cur_t.fetchall()
                if not rows:
                    client_sock.send('not'.encode())
                else:
                    login_time = str(time.time())
                    client_sock.send(login_time.encode())
                    online[data['name']]['login_time'] = login_time

            else:
                continue

        elif data['type'] == 'new user':

            if 'name' in data.keys() and 'password' in data.keys():

                hash_object = hashlib.sha1(data['password'].encode("UTF-8"))
                hex_dig = hash_object.hexdigest()

                cur_t.execute("INSERT INTO `users` (`name`, `password`) VALUES (%s, %s)", (data['name'], hex_dig))

                login_time = str(time.time())
                online[data['name']] = {'time': time.time(), 'online_status': 1, 'login_time': login_time}
                client_sock.send(login_time.encode())

            else:
                continue

        elif data['type'] == 'new contact':

            if 'user' in data.keys() and 'contact' in data.keys() and online[data['user']]['login_time'] == data['login_time']:
                cur_t.execute("SELECT `contact` FROM `contacts` WHERE `user` = %s AND `contact` = %s", (data['user'], data['contact']))
                rows = cur_t.fetchall()
                if rows != []:
                    client_sock.send('not'.encode())
                else:
                    cur_t.execute("INSERT INTO `contacts` (`user`, `contact`) VALUES (%s, %s)", (data['user'], data['contact']))
                    client_sock.send('ok'.encode())
            else:
                continue

        elif data['type'] == 'contacts':

            if 'user' in data.keys() and online[data['user']]['login_time'] == data['login_time']:
                cur_t.execute("SELECT `contact` FROM `contacts` WHERE `user` = %s UNION SELECT DISTINCT `sender` FROM `messages` WHERE recipient = %s", (data['user'], data['user']))
                rows = cur_t.fetchall()
                contacts = []
                if rows != []:
                    for i in rows:
                        contact = {'contact': i[0], 'online status': online[i[0]]['online status']}
                        contacts.append(contact)
                    client_sock.send(json.dumps(contacts).encode())
                else:
                    client_sock.send('not'.encode())
            else:
                continue

        elif data['type'] == 'all messages':
            if 'user' in data.keys() and 'contact' in data.keys() and online[data['user']]['login_time'] == data['login_time']:
                cur_t.execute("SELECT `sender`, `text` FROM `messages` WHERE (`recipient` = %s AND `sender` = %s) OR (`recipient` = %s AND `sender` = %s) ORDER BY `time` ASC", (data['user'], data['contact'], data['contact'], data['user']))
                rows = cur_t.fetchall()
                if rows != []:
                    client_sock.send(json.dumps(rows).encode())
                else:
                    client_sock.send('EMPTY'.encode())

            else:
                continue

    client_sock.close()

online = {}

cur.execute("SELECT `name` FROM `users`")
rows = cur.fetchall()
for i in rows:
    online[i[0]] = {'time': 0, 'online status': 0, 'login_time': 0}

def online_users():
    while True:
        for key in online.keys():
            if time.time() - online[key]['time'] > 5:
                online[key]['online status'] = 0
            else:
                online[key]['online status'] = 1
        time.sleep(1)

t1 = threading.Thread(target=online_users)
t1.start()

threads = {}
dead = []

while True:
    client_sock, client_addr = sock.accept()
    t = threading.Thread(target=process_message, name=client_addr, args=(client_sock, client_addr))
    t.start()
    threads[client_addr] = t
    i = 0
    while i < len(dead):
        if dead[i] in threads.keys():
            threads[dead[i]].join()
            # if not threads[dead[i]].is_alive():
            #     print(threads[dead[i]], 'dead')
            del threads[dead[i]]
            del dead[i]
        else:
            i+=1






