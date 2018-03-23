from Client import Client
import tkinter as tk
from tkinter import scrolledtext, simpledialog
from functools import partial


class P2pChat(tk.Frame):

    width = 1280
    height = 640

    def __init__(self, master=None):

        master.wm_title("test name")
        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH, expand=1)
        master.geometry(str(self.width) + "x" + str(self.height))
        self.create_mainmenu()
        self.client = Client(self)

    def create_mainmenu(self):
        menubar = tk.Menu(self)
        menu = tk.Menu(menubar, tearoff=0)
        menu.add_command(label="Connect to chat",
                         command=self.connect_to_server_window)
        menu.add_command(label="Change Username", command=self.change_username)
        menu.add_separator()
        menu.add_command(label="Exit", command=self.close_app)
        menubar.add_cascade(label="Menu", menu=menu)
        self.master.config(menu=menubar)

        room_list_frame = tk.LabelFrame(self, text="Room list",
                                        bd=5, width="150")
        room_list_frame.pack(side=tk.RIGHT,
                             fill=tk.Y, expand=0)
        self.room_list_frame = room_list_frame
        self.create_room_list()
        create_room_frame = tk.LabelFrame(room_list_frame,
                                          text="Create new room",
                                          width="130", bd=3)
        create_room_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=0)
        self.create_room_frame = create_room_frame
        room_name_entry = tk.Entry(create_room_frame)
        room_name_entry.pack(side=tk.LEFT)
        room_name_button = tk.Button(create_room_frame)
        room_name_button["text"] = "Create"
        room_name_button.pack(side=tk.LEFT)

        room_user_list_frame = tk.LabelFrame(self, text="User list",
                                             bd=5, width="150")
        room_user_list_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=0)
        self.room_user_list_frame = room_user_list_frame
        self.create_room_user_list()

        msg_frame = tk.Frame(self)
        msg_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

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
        master.bind('<Return>', self.send_message_to_chat)
        master.bind('<KP_Enter>', self.send_message_to_chat)
        master.bind('<Escape>', self.close_app)

        master.update()

    def connect_to_server_window(self):
        chat_connection_window = tk.Toplevel(root)
        chat_connection_window.wm_title("connect to server directly")
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
        username_label = tk.Label(chat_connection_frame, text="USERNAME:")
        username_label.grid(row=0, column=4)
        username_entry = tk.Entry(chat_connection_frame)
        username_entry.grid(row=0, column=5)
        done_button = tk.Button(chat_connection_frame)
        done_button["text"] = "connect"
        args = []
        args.append(ip_entry.get())
        args.append(port_entry.get())
        args.append(username_entry.get())
        done_button["command"] = partial(self.close_window_and_call_function,
                                             args, chat_connection_window)
        done_button.grid(row=1, column=2)
        self.port_entry = port_entry

    def close_window_and_call_function(self, args, frame):
        frame.destroy()
        print(args)
        self.client = Client(self, args[0], args[1], args[2])

    def create_room_user_list(self, users=[]):
        self.clean_frame_widgets(self.room_user_list_frame)
        users = [{"name": "les cons"}, {"name": "god is just really dog spelled backwards"}, {"name": "alexis"},
                 {"name": "jerem"}, {"name": "lothare"}]
        for user in users:
            user_label = tk.Label(self.room_user_list_frame,
                                  text=str(user["name"]), anchor="w")
            user_label.pack(side=tk.TOP, fill=tk.X, padx="10")

    # def create_room_user_list(self):
        # self.client.send_data(self.client.s, "gethostlist", ['null'], )

    def create_room_list(self, table=[]):
        self.clean_frame_widgets(self.room_list_frame)
        table = [{"name": "room1"}, {"name": "room2"}, {"name": "room3"}, {"name": "room4"}]
        for room in table:
            new_btn = tk.Button(self.room_list_frame, relief="ridge")
            new_btn["text"] = str(room["name"])
            # new_btn["command"] = self.client.connect_to_room.bind(room)
            new_btn.pack(side=tk.TOP, fill=tk.X, ipadx="20", padx="10", pady="5")

    def clean_frame_widgets(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def close_app(self, Event=None):
        root.destroy()

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
        self.msg_entry.delete(0, tk.END)
        self.client.send_message_user('msg', msg)

    def update_message_list(self, msg):
        self.msg_window.config(state=tk.NORMAL)
        self.msg_window.insert(tk.END, "%s\n" % msg)
        self.msg_window.yview(tk.END)
        self.msg_window.config(state=tk.DISABLED)
        print("updating the message_list")

    def start_hosting(self):
        self.client.s.send("/startHost".encode())
        print("starting to host")


root = tk.Tk()
p2p_chat = P2pChat(master=root)
p2p_chat.mainloop()
