import socket
import threading
import json
# import select
# import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog


class P2pChat(tk.Frame):
    client = []
    def __init__(self, master=None):

        master.wm_title("test name")
        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH, expand=1)
        master.geometry("1280x640")
        self.create_mainmenu()
        self.client = Client()

    def create_mainmenu(self):
        menubar = tk.Menu(self)
        menu = tk.Menu(menubar, tearoff=0)
        menu.add_command(label="Start hosting", command=self.start_hosting)
        menu.add_command(label="Connect to chat", command=self.connect_to_chat)
        menu.add_command(label="Change Username", command=self.change_username)
        menu.add_command(label="Get list of chats", command=self.get_chat_list)
        menu.add_separator()
        menu.add_command(label="Exit", command=self.close_app)
        menubar.add_cascade(label="Menu", menu=menu)
        self.master.config(menu=menubar)
        msg_frame = tk.Frame(self)
        msg_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        msg_window = scrolledtext.ScrolledText(msg_frame, height=10, width=80)
        msg_window.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        msg_window.config(state=tk.DISABLED)
        self.msg_window = msg_window

        msg_entry_frame = tk.Frame(msg_frame, relief=tk.RAISED, bd=1)
        msg_entry_frame.pack(side=tk.BOTTOM, fill=tk.X)

        msg_entry = tk.Entry(msg_entry_frame)
        msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=1)
        msg_entry.focus()
        self.msg_entry = msg_entry

        send_btn = tk.Button(msg_entry_frame)
        send_btn["text"] = "Send"
        send_btn["command"] = self.send_message_to_chat
        send_btn.pack(side=tk.RIGHT)
        master = self.master
        master.update()

    def close_app(self):
        root.destroy()

    def connect_to_chat(self):
        print("connecting to chat")

    def change_username(self):
        temp = simpledialog.askstring("Input", "what is you new username",
                                      parent=self.master)
        msg = "/changeName :" + str(temp)
        self.client.s.send(msg.encode())
        print("changing username")

    def get_chat_list(self):
        self.client.send_data(self.client.s, "gethostlist", ['null'])
        print("getting chat list")

    def send_message_to_chat(self):
        print("sending message to chat")
        msg = self.msg_entry.get()
        print(msg)
        self.msg_entry.delete(0, tk.END)
        self.client.s.send(msg.encode())

    def update_message_list(self):
        print("updating the message_list")

    def start_hosting(self):
        self.client.s.send("/startHost".encode())
        print("starting to host")


class Client:

    server = ('127.0.0.1', 10020)

    def __init__(self):
        self.port = 10001
        print("init")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.su = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = socket.gethostbyname(socket.gethostname())

        self.bind_port(self.s, ip, self.port)
        self.portU = self.port
        self.bind_port(self.su, ip, self.portU)

        self.s.connect(self.server)
        self.send_data(self.s, "connexion", ["127.0.0.1", self.portU])
        ths = threading.Thread(target=self.recv_handler_server)
        threading.Thread(target=self.handle_user_connection)
        ths.start()
        # lc = threading.Thread(target=self.listen_connection)
        # lc.start()
    def bind_port(self, sock, ip, port):
        while True:
            try:
                sock.bind(ip, port)
                break
            except:
                port += 1

    def listen_connection(self):
        while True:
            # self.s.listen(5)
            sock, addr = self.s.accept()
            if addr[0] == "127.0.0.1" & addr[1] == 10000:
                ths = threading.Thread(target=self.recv_handler_server,
                                       kwargs={'sock': sock})
                ths.start()
            else:
                th = threading.Thread(target=self.recv_handler,
                                      kwargs={'sock': sock})
                th.start()
        self.s.close()

    def recv_handler_server(self):
        while True:
            msg = self.s.recv(1024)
            msg = msg.decode("utf-8")
            temp = json.loads(msg)
            print(str(temp))
            if msg:
                print("message from server test")
                for user in temp:
                    if user[1] != self.portU:
                        self.client.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                        self.client[-1].bind('', 0)
                        print(str(user[0]), user[1])
                        self.client[-1].connect((user[0], user[1]))

    def recv_handler(self, sock):
        while True:
            msg = sock.recv(1024)
            msg.decode()
            if not msg:
                print("message is not from server")
                print(msg)

    def handle_user_connection(self):
        while True:
            self.s.listen(5)
            sock, addr = self.s.accept()
            acu = threading.Thread(target=self.add_connected_user,
                                   kwargs=({"sock": sock, "addr": addr}))
            acu.start()
            self.listusers.append([addr[0], addr[1]])
            print(sock)
            # print('Connected with ' + addr[0] + ':' + str(addr[1]))
        self.s.close()
    def send_data(self, sock, type_message, data):
        sock.send(str("{\"message\": \""+str(type_message)+"\", \"data\": "+json.dumps(data)+"}").encode("utf-8"))
    def add_connected_user(self, sock, addr):
        print(sock, addr)
        # new_user = User(sock, addr[0], addr[1])
        # self.users.append(new_user)
        # th = threading.Thread(target=self.recv_handler, kwargs={'sock': sock})
        # th.start()
class Chat:

    def __init__():
        print("new chat")


root = tk.Tk()
p2p_chat = P2pChat(master=root)
p2p_chat.mainloop()
