import socket
import threading
import json
# import select
# import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from functools import partial


class P2pChat(tk.Frame):

    width = 1280
    height = 640

    def __init__(self, master=None):

        master.wm_title("test name")
        tk.Frame.__init__(self, master)
        # self.grid()
        self.pack(fill=tk.BOTH, expand=1)
        master.geometry(str(self.width) + "x" + str(self.height))
        self.create_mainmenu()
        self.client = Client()

    def create_mainmenu(self):
        menubar = tk.Menu(self)
        menu = tk.Menu(menubar, tearoff=0)
        menu.add_command(label="Start hosting", command=self.start_hosting)
        menu.add_command(label="Connect to chat",
                         command=self.connect_to_chat_window)
        menu.add_command(label="Change Username", command=self.change_username)
        menu.add_command(label="Get list of chats",
                         command=self.room_list_window)
        menu.add_separator()
        menu.add_command(label="Exit", command=self.close_app)
        menubar.add_cascade(label="Menu", menu=menu)
        self.master.config(menu=menubar)

        # # create all the main frames
        # toolbar_frame = tk.Frame(self, relief="sunken", width=self.width,
        #                          height=(self.height / 10), padx=5,
        #                          bg="red")
        # middle_frame = tk.Frame(self, width=self.width,
        #                         height=(8 * (self.height / 10)), padx=5,
        #                         bg="green")
        # footer_frame = tk.Frame(self, width=self.width,
        #                         height=(self.height / 10), padx=5,
        #                         bg="yellow")

        # # sets the weight of the main window
        # self.master.grid_rowconfigure(1, weight=1)
        # self.master.grid_columnconfigure(0, weight=1)

        # # grids the frames
        # toolbar_frame.grid(row=0, sticky="ew")
        # middle_frame.grid(row=1, sticky="nesw")
        # footer_frame.grid(row=2, sticky="ew")

        # toolbar_button_connect = tk.Button(toolbar_frame, text="Cth",
        #                                    bg="white", bd=0, padx=10)
        # toolbar_button_username = tk.Button(toolbar_frame, text="Cun",
        #                                     bg="white", bd=0, padx=10)
        # toolbar_label_username = tk.Label(toolbar_frame, text="cun",
        #                                   bg="blue")
        # toolbar_button_connect.grid(row=0, column=0, columnspan=3, sticky="e")
        # toolbar_button_username.grid(row=0, column=4, columnspan=3, sticky="e")
        # toolbar_label_username.grid(row=0, column=7)

        # toolbar_frame.grid(row=0, column=0, columnspan=10)
        # connect_to_host_button = tk.Button(toolbar_frame, relief="groove")
        # connect_to_host_button["text"] = "cth"
        # connect_to_host_button.grid(row=0, column=0, sticky="nesw")
        # get_room_list_button = tk.Button(toolbar_frame, relief="groove")
        # get_room_list_button["text"] = "grl"
        # get_room_list_button.grid(row=0, column=1, sticky="nesw")
        # change_username_button = tk.Button(toolbar_frame, relief="groove")
        # change_username_button["text"] = "cun"
        # change_username_button.grid(row=0, column=2, sticky="nesw")
        # username_label_frame = tk.LabelFrame(toolbar_frame, text="UserName", bg="blue")
        # username_label_frame.grid(row=0, column=5)
        # username_label = tk.Label(text="UserName")
        # username_label.grid(row=0, column=5)

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

        # user_list = tk.LabelFrame(self, text="user in chat", bg="red")
        # user_list.grid(row=0, column=1, sticky="W")
        master = self.master
        master.bind('<Return>', self.send_message_to_chat)
        master.bind('<KP_Enter>', self.send_message_to_chat)

        master.update()

    def close_window_and_call_function(self, args, window, function):
        window.destroy()


    def room_list_window(self):
        table = [{"name": "room1"}, {"name": "room2"}, {"name": "room3"},
                 {"name": "room4"}]
        room_list_window = tk.Toplevel(root)
        room_list_frame = tk.Frame(room_list_window)
        room_list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # room_list_window.geometry("500x500")
        for room in table:
            new_btn = tk.Button(room_list_frame)
            new_btn["text"] = str(room["name"])
            # new_btn["command"] = self.client.connect_to_room.bind(room)
            new_btn.pack(side=tk.TOP, fill=tk.X)

    def close_app(self):
        root.destroy()

    def connect_to_chat_window(self):
        chat_connection_window = tk.Toplevel(root)
        chat_connection_window.wm_title("connect to chat directly")
        chat_connection_frame = tk.Frame(chat_connection_window)
        chat_connection_frame.grid(row=0, column=0)
        ip_label = tk.Label(chat_connection_frame, text="IP:")
        ip_label.grid(row=0, column=0)
        ip_entry = tk.Entry(chat_connection_frame)
        ip_entry.insert(0, "127.0.0.1")
        ip_entry.grid(row=0, column=1)
        self.ip_entry = ip_entry
        port_label = tk.Label(chat_connection_frame, text="PORT:")
        port_label.grid(row=0, column=2)
        port_entry = tk.Entry(chat_connection_frame)
        port_entry.insert(0, 40000)
        port_entry.grid(row=0, column=3)
        done_button = tk.Button(chat_connection_frame)
        done_button["text"] = "connect"
        args = []
        args.append(ip_entry.get())
        args.append(port_entry.get())
        done_button["command"] = partial(self.close_window_and_call_function,
                                         args, chat_connection_window,
                                         "self.client.connect_to_chat")
        done_button.grid(row=1, column=2)
        self.port_entry = port_entry

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

    def send_message_to_chat(self, event):
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
        # port = 10001
        # print("heightllo")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ip = socket.gethostbyname(socket.gethostname())
        # while True:
            # try:
                # self.s.bind((ip, port))
                # break
            # except:
                # port += 1
        # self.s.connect(self.server)
        # ths = threading.Thread(target=self.recv_handler_server)
        # ths.start()
        # lc = threading.Thread(target=self.listen_connection)
        # lc.start()

    def connect_to_chat(self, ip, port):
        print(ip)
        print(port)

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
