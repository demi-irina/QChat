import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor, QFont
import design_login
import design_main
import socket
import threading
import json
import time
import config

from PyQt5.QtWidgets import QMessageBox, QListWidgetItem

class MainWindow(QtWidgets.QMainWindow, design_main.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class LoginWindow(QtWidgets.QMainWindow, design_login.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class UserItem(QListWidgetItem):
    def __init__(self, user_name, *args):
        super().__init__(*args)
        self.user_name = user_name
        self.unread_count = 0
        self.online_status = False


class Client():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = MainWindow()
        self.login_window = LoginWindow()
        self.login_window.registerButton.clicked.connect(self.register)
        self.login_window.loginButton.clicked.connect(self.login)
        self.main_window.add_name.clicked.connect(self.new_contact)
        self.main_window.send.clicked.connect(self.send_message)

        self.sock = socket.socket()
        self.sock.connect((config.SERVER_IP, config.SERVER_PORT))
        self.socket_lock = threading.Lock()

        self.name = None
        self.login_time = None
        self.selected_recipient = None

        self.main_window.recipients_list.currentItemChanged.connect(self.process_contact_click)
        self.main_window.send.setEnabled(False)
        self.main_window.input_text.setEnabled(False)

        self.contact_asker_t = threading.Thread(target=self.contacts)
        self.name_sender_t = threading.Thread(target=self.name_sender)
        self.abort = False

    def get_name_pass(self):
        name = self.login_window.loginInput.text()
        password = self.login_window.passwordInput.text()
        if len(name) == 0 or len(password) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Empty name or password not allowed')
            msg.setWindowTitle("Error")
            msg.exec_()
            return None, None
        return name, password

    def login(self):
        name, password = self.get_name_pass()
        if name is None:
            return
        self.sock.send(json.dumps({'type': 'user name', 'name': name}).encode())
        data = self.sock.recv(1024).decode()
        if data == 'not':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Enter another name")
            msg.setInformativeText('There is no user with this name')
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        self.sock.send(json.dumps({'type': 'password', 'name': name, 'password': password}).encode())
        data = self.sock.recv(1024).decode()
        if data == 'not':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Enter another password")
            msg.setInformativeText('Wrong password')
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        self.login_time = data
        self.name = name
        self.login_window.hide()
        self.main_window.show()
        self.contact_asker_t.start()

        self.name_sender_t.start()

    def register(self):
        name, password = self.get_name_pass()
        if name is None:
            return
        self.sock.send(json.dumps({'type': 'user name', 'name': name}).encode())
        data = self.sock.recv(1024).decode()
        if data == 'ok':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Enter another name")
            msg.setInformativeText('There is another user with this name')
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        self.sock.send(json.dumps({'type': 'new user', 'name': name, 'password': password}).encode())
        data = self.sock.recv(1024).decode()
        self.login_time = data
        self.name = name
        self.login_window.hide()
        self.main_window.show()
        self.contact_asker_t.start()

        self.name_sender_t.start()

    def new_contact(self):
        contact = self.main_window.input_name_add.text()
        with self.socket_lock:
            self.sock.send(json.dumps({'type': 'user name', 'name': contact}).encode())
            data = self.sock.recv(1024).decode()
        if data == 'not':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Enter another name")
            msg.setInformativeText('There is no user with this name')
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        with self.socket_lock:
            self.sock.send(json.dumps({'type': 'new contact', 'user': self.name, 'contact': contact, 'login_time': self.login_time}).encode())
            data = self.sock.recv(1024).decode()
        if data == 'not':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Enter another name")
            msg.setInformativeText('This user is already on the list')
            msg.setWindowTitle("Error")
            msg.exec_()
            return

    def process_contact_click(self, contact):
        self.main_window.send.setEnabled(True)
        self.main_window.input_text.setEnabled(True)
        font = QFont()
        font.setBold(False)
        contact.setFont(font)
        contact.setText(contact.user_name)
        self.main_window.recipient.setText(contact.user_name + (' (online)' if contact.online_status else ' (offline)'))
        self.selected_recipient = contact.user_name
        self.main_window.messages.clear()
        self.sock.send(json.dumps({'type': 'all messages', 'user': self.name, 'contact': self.selected_recipient, 'login_time': self.login_time}).encode())
        data1 = self.sock.recv(1024).decode()
        if data1 == 'EMPTY':
            return
        data = json.loads(data1)
        for i in data:
            if i[0] == self.name:
                sender = '<span style="color: #0000ff;">%s</span>' % i[0]
            else:
                sender = '<span style="color: #ff8c00;">%s</span>' % i[0]
            mes = '<br>'.join(i[1].split('\n'))
            message = sender + ': ' + mes
            self.main_window.messages.append(message)

    def find_contact_item(self, user_name):
        for i in range(self.main_window.recipients_list.count()):
            item = self.main_window.recipients_list.item(i)
            if item.user_name == user_name:
                return item

    def contacts(self):
        old_list = []
        while not self.abort:
            with self.socket_lock:
                self.sock.send(json.dumps({'type': 'contacts', 'user': self.name, 'login_time': self.login_time}).encode())
                data1 = self.sock.recv(1024).decode()
            if data1 == 'not':
                time.sleep(1)
                continue
            data = json.loads(data1)
            dl = []
            for c in data:
                dl.append(c['contact'])
                if c['contact'] not in old_list:
                    UserItem(c['contact'], c['contact'], self.main_window.recipients_list)
                item = self.find_contact_item(c['contact'])
                if c['online status']:
                    item.setForeground(QColor(21, 122, 13))
                    item.online_status = True
                else:
                    item.setForeground(QColor(207, 39, 39))
                    item.online_status = False

                if c['contact'] == self.selected_recipient:
                    self.main_window.recipient.setText(item.user_name + (' (online)' if item.online_status else ' (offline)'))

            for c in old_list:
                if c not in dl:
                    item_to_remove = self.main_window.recipients_list.self.find_contact_item(c)
                    index_to_remove = self.main_window.recipients_list.row(item_to_remove)
                    self.main_window.recipients_list.takeItem(index_to_remove)

            self.main_window.recipients_list.viewport().update()
            old_list = dl
            time.sleep(1)

    def name_sender(self):
        while not self.abort:
            with self.socket_lock:
                self.sock.send(json.dumps({'type': 'name', 'name': self.name, 'login_time': self.login_time}).encode())
                data1 = self.sock.recv(1024).decode()
            if data1 == 'EMPTY':
                time.sleep(0.5)
                continue
            data = json.loads(data1)
            updated_items = []
            for i in data:
                if i[0] == self.selected_recipient:
                    sender = '<span style="color: #ff8c00;">%s</span>' % i[0]
                    mes = '<br>'.join(i[1].split('\n'))
                    message = sender + ': ' + mes
                    self.main_window.messages.append(message)
                else:
                    item = self.find_contact_item(i[0])
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.unread_count += 1
                    updated_items.append(item)
            for i in updated_items:
                i.setText(i.user_name + ' (' + str(i.unread_count) + ')')

    def send_message(self):
        text = self.main_window.input_text.toPlainText()
        recipient = self.selected_recipient
        self.sock.send(json.dumps({'type': 'message', 'recipient': recipient, 'sender': self.name, 'text': text, 'login_time': self.login_time}).encode())
        sender = '<span style="color: #0000ff;">%s</span>' % self.name
        mes = '<br>'.join(text.split('\n'))
        message = sender + ': ' + mes
        self.main_window.messages.append(message)
        self.main_window.input_text.clear()

    def main(self):
        self.login_window.show()
        self.app.exec_()

if __name__ == '__main__':
    c = Client()
    c.main()
    c.abort = True