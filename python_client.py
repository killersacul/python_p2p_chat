import socket
import threading
import json
# import select
# import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog


class P2pChat(tk.Frame):

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
        self.client.s.send("/gethostlist".encode())
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

    server = ('127.0.0.1', 10000)

    def __init__(self):
        port = 10001
        print("hello")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = socket.gethostbyname(socket.gethostname())
        while True:
            try:
                self.s.bind((ip, port))
                break
            except:
                port += 1
        self.s.connect(self.server)
        ths = threading.Thread(target=self.recv_handler_server)
        ths.start()
        # lc = threading.Thread(target=self.listen_connection)
        # lc.start()

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
                print("message from server")
                print(msg)

    def recv_handler(self, sock):
        while True:
            msg = sock.recv(1024)
            msg.decode()
            if not msg:
                print("message is not from server")
                print(msg)


class Chat:

    def __init__():
        print("new chat")


root = tk.Tk()
p2p_chat = P2pChat(master=root)
p2p_chat.mainloop()
