# Python program to implement server side of chat room.
import socket
import threading
import json


class server:

    users = []
    listrooms = []
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
        while True:
            # try:
                msg = ""
                while True:
                    tmp = sock.recv(1024).decode()
                    msg += tmp
                    if tmp is not True: break
                data = json.loads(msg)
                print(data)
                if data['message'] == "connexion":
                    print("connexion data :" + str(data["data"]))
                    self.listusers.append([sock.getsockname()[0], data["data"][0][1], sock.getsockname()[1], data["data"][1]])
                    print("list user :"+str(self.listusers))
                    self.return_list_of_users(sock)
                elif data['message'] == "list_of_users":
                    print("list_of_users")
                elif data['message'] == "new_room":
                    print("new_room")
                    self.create_new_room(sock, data)
                elif data['message'] == "list_of_room":
                    print("list_of_room")
                    self.return_list_of_rooms(sock)
                else:
                    print("probleme : " + str(data))

            # except Exception as e:
            #     print("merde :" + str(e))
            #     for i, user in enumerate(self.listusers):
            #         print("deconnection etape 1")
            #         print(user)
            #         print(sock.getsockname())
            #         if str(sock.getsockname()[0]) == str(user[0]) and  int(sock.getsockname()[1]) == int(user[2]):
            #             del self.listusers[i]
            #             print("deconnexion de :" + str(user))

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

        def return_list_of_rooms(self, sock):
            print("send list of room :")
            data = {}
            data['message'] = "list_of_rooms"
            data["data"] = self.listrooms
            sock.send(json.dumps(data).encode("utf-8"))

        def create_new_room(self, sock, data):
            dat["data"][0][0] = sock.getsockname()[0]
            print(data)
            self.listrooms = data['data']

        def connect_to_host(self, sock, ip, port):
            for user in self.users:
                if ip == user.ip & port == user.port:
                    sock.send(user)
                    break
            print("connection to host")

ser = server()
