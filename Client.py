import socket
import threading
import json
from server_room import Server_room

class Client:
    users = []
    server = ()
    p2pclient = []
    my_rooms = []
    def __init__(self, p2p_chat, host="127.0.0.1", port=10049, username=None):
        self.username = username
        self.server = (host, port)
        self.p2p_chat = p2p_chat
        print("connection to :")
        print(self.server)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.su = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = socket.gethostbyname(socket.gethostname())

        self.s.bind(('', 0))
        self.s.connect(self.server)
        self.su.bind(('', 0))
        print(self.su.getsockname())
        self.send_data(self.s, "connexion", [self.su.getsockname(), username])
        self.ths1 = threading.Thread(target=self.recv_handler_server)
        self.ths1.start()

        ths2 = threading.Thread(target=self.server_user)
        ths2.start()


    def recv_handler_server(self):
        tmp = ""
        while True:
            print("message from server test")
            msg = self.s.recv(1024).decode("utf-8")
            tmp = tmp + msg
            if msg is not True: break
        data = json.loads(tmp)
        if data["message"] == "list_of_users":
            self.connect_to_room_generale(data["data"])
        if data["message"] == "list_of_room":
            self.p2p_chat.create_room_list(data["data"])


    def recv_handler(self, sock):
        print("recv_handler")
        print("message is not from user")
        while True:
            msg = sock.recv(1024).decode()
            if not msg: break
            self.p2p_chat.update_message_list(str(msg))


    def server_user(self):
        while True:
            self.su.listen(5)
            sock, addr = self.su.accept()
            self.p2pclient.append(sock)
            print("connexion " + str(sock))

            acu = threading.Thread(target=self.add_connected_user,
                                   kwargs=({"sock": sock, "addr": addr}))
            acu.start()
            print(self.p2pclient)
            # print('Connected with ' + addr[0] + ':' + str(addr[1]))
        # self.su.close()


    def send_message_user(self, type_message, data):
        self.send_data(self.s, "list_of_room", [None])
        for user in self.p2pclient:
            user.send(data.encode())

    def add_connected_user(self, sock, addr):
        print(sock, addr)
        new_user = [sock, addr[0], addr[1]]
        self.users.append(new_user)
        th = threading.Thread(target=self.recv_handler, kwargs={'sock': sock})
        th.start()

    def connect_to_room(self, room):
        print("connect to room" + str(room))

    def create_new_room(self, room_name):
        self.my_rooms.append(Server_room(room_name, self.username))
        self.my_rooms[-1].info
        self.send_data(self.s, "new_room", self.my_rooms[-1].info)
        print("creating room :" + str(self.my_rooms[-1].info))

    def connect_to_room_generale(self, room):
        for user in room:
            print(user)
            if user[1] != self.su.getsockname()[1]:
                self.p2pclient.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                self.p2pclient[-1].bind(('', 0))
                print("demande de connection : " +str(user[0]) +" " +str(user[1]))
                self.p2pclient[-1].connect((user[0], user[1]))
                print("user connection")
                th = threading.Thread(target=self.recv_handler, kwargs={'sock': self.p2pclient[-1]})
                th.start()

    def get_room_list(self, colback):

        colback()

    def send_data(self, sock, type_message, array):
        data = {}
        data["message"] = type_message
        data["data"] = array
        print("send_data: " + str(data) + " to " + str(type_message) + "for"+ str(sock))
        sock.send(json.dumps(data).encode("utf-8"))

    def destroy(self):
        print("destroy")
        # self.s.close()
        self.su.close()
        pass
