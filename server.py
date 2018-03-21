# Python program to implement server side of chat room.
import socket
import threading
import json


class server:

    users = []

    def __init__(self):
        print("starting the server")
        self._lock = threading.Lock()
        port = 10020
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', port))
        huc = threading.Thread(target=self.handle_user_connection)
        huc.start()
        self.listusers = []
        self.room = []
        self.listroom = [self.room]

    def handle_user_connection(self):
        while True:
            self.s.listen(5)
            sock, addr = self.s.accept()
            acu = threading.Thread(target=self.add_connected_user,
                                   kwargs=({"sock": sock, "addr": addr}))
            acu.start()
            print(self.listusers)
            # print('Connected with ' + addr[0] + ':' + str(addr[1]))
        self.s.close()

    def add_connected_user(self, sock, addr):
        new_user = User(sock, addr[0], addr[1])
        self.users.append(new_user)
        th = threading.Thread(target=self.recv_handler, kwargs={'sock': sock})
        th.start()

    def recv_handler(self, sock):
        while True:
            msg = sock.recv(1024)
            print(msg)
            data = json.loads(msg.decode())
            print(data)
            if data['message'] == "connexion":
                print(data["data"])
                # self.listusers.append([addr[0], addr[1]])
                self.listusers.append(data['data'])
            if data['message'] == "gethostlist":
                self.return_list_of_host(sock)
            # if message_type == 2:
            #     self.starting_hosting(sock)
            # if message_type == 3:
            #     self.return_list_of_host(sock)
            # if message_type == 4:
            #     username = str(msg[13:])
            #     print(username)
            #     self.change_user_name(sock, msg)
            # if message_type == 5:
            #     self.connectToHost()
            # if message_type != 1:
            #     print(msg)
                # break

    # def determine_message_type(self, msg):
    #     if not msg:
    #         return 1
    #     # print(msg)
    #     if "/startHost" in str(msg):
    #         print("hosting")
    #         return 2
    #     if "/gethostlist" in str(msg):
    #         print("get host list")
    #         return 3
    #     if "/changeName" in str(msg):
    #         return 4
    #     if "/connectToHost" in str(msg):
    #         return 5
    #     return 6

    def change_user_name(self, sock, username):
        for user in self.users:
            if user.sock == sock:
                user.username = username
        print("changing username")

    def starting_hosting(self, temp_sock):
        print("starting hosting")
        for user in self.users:
            if user.sock == temp_sock:
                user.hosting = True
                print("found the user")

    def return_list_of_host(self, sock):

        # tmp = []
        # for user in self.users:
        #     if sock != user.sock:
        #         if user.hosting:
        #             tmp.append(user)
        # temp_array = json.dumps(tmp)
        print(self.listusers)
        # temp_array = json.dumps(self.listusers)
        # print(temp_array)
        print("send list of host")
        sock.send(json.dumps(self.listusers).encode("utf-8"))
        # sock.send(temp_array.encode("utf-8"))

    def connect_to_host(self, sock, ip, port):
        for user in self.users:
            if ip == user.ip & port == user.port:
                sock.send(user)
                break
        print("connection to host")


class User:

    def __init__(self, sock, ip, port, name=None, hosting=False):
        self._sock = sock
        self._ip = ip
        self._port = port
        if name is None:
            self._name = ip
        else:
            self._name = name
        self.hosting = hosting

    @property
    def sock(self):
        return self._sock

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def name(self):
        return self._name


ser = server()
