import socket
import threading
import json

class Client:
    users = []
    server = ('127.0.0.1', 10049)
    p2pclient = []
    def __init__(self, p2p_chat, host="127.0.0.1", port=10049, username=None):
        self.server[0] = host
        self.server[1] = port
        self.p2p_chat = p2p_chat
        print("init")
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


    def listen_connection(self):
        print("listen")
        while True:
            # self.s.listen(5)
            sock, addr = self.s.accept()
            if addr[0] == "127.0.0.1" & addr[1] == server[1]:
                ths = threading.Thread(target=self.recv_handler_server,
                                       kwargs={'sock': sock})
                ths.start()
            else:
                print("user reac_handler")
                th = threading.Thread(target=self.recv_handler,
                                      kwargs={'sock': sock})
                th.start()
        self.s.close()

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

    def send_data(self, sock, type_message, array):
        data = {}
        data["message"] = type_message
        data["data"] = array
        print("send_data: " + str(data) + " to " + str(type_message))
        sock.send(json.dumps(data).encode("utf-8"))

    def send_message_user(self, type_message, data):
        for user in self.p2pclient:
            user.send(data.encode())

    def add_connected_user(self, sock, addr):
        print(sock, addr, )
        new_user = [sock, addr[0], addr[1]]
        self.users.append(new_user)
        th = threading.Thread(target=self.recv_handler, kwargs={'sock': sock})
        th.start()

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
    def destroy(self):
        print("destroy")
        self.s.close()
        self.su.close()
        pass
