# Python program to implement server side of chat room.
import socket
import threading
import json


class server:

    users = []

    def __init__(self):
        print("starting the server")
        self._lock = threading.Lock()
        port = 10049
        print("port :" + str(port))
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
            print("connexion " + str(sock))
            acu = threading.Thread(target=self.add_connected_user,
                                   kwargs=({"sock": sock, "addr": addr}))
            acu.start()
        self.s.close()

    def add_connected_user(self, sock, addr):
        th = threading.Thread(target=self.recv_handler, kwargs={'sock': sock})
        th.start()

    def recv_handler(self, sock):
        try:
            while True:
                msg = sock.recv(1024)
                data = json.loads(msg.decode())
                if data['message'] == "connexion":
                    print("connexion data :" + str(data["data"]))
                    self.listusers.append([sock.getsockname()[0], data["data"][1], sock.getsockname()[1], data["data"][2]])
                elif data['message'] == "list_of_users":
                    print("list_of_users")
                    self.return_list_of_users(sock)
        except Exception as e:
            print(e)
            for i, user in enumerate(self.listusers):
                print("deconnection etape 1")
                print(user)
                print(sock.getsockname())
                if str(sock.getsockname()[0]) == str(user[0]) and  int(sock.getsockname()[1]) == int(user[2]):
                    del self.listusers[i]
                    print("deconnexion de :" + str(user))

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

    def return_list_of_users(self, sock):
        print("send list of host :")
        data = {}
        data["message"] = "list_of_users"
        data["data"] = self.listusers
        print(data)
        sock.send(json.dumps(data).encode("utf-8"))

    def connect_to_host(self, sock, ip, port):
        for user in self.users:
            if ip == user.ip & port == user.port:
                sock.send(user)
                break
        print("connection to host")

ser = server()
