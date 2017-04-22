import pickle
import socket
import threading
from Message import Message
from server.Channel import Channel
from server.Command import *

class ThreadedServer(object):
    def __init__(self, host, port):
        self.channels = [Channel("channel1"), Channel("channel2")]
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))


    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.send(pickle.dumps(self.channels))
            welcomeMessage = Message("SERVER",self.channels[0],"Bienvenue sur le serveur de chat !!")
            client.send(pickle.dumps(welcomeMessage))
            '''
            for channel in self.channels:
                channel.lock.acquire()
                try:
                    channel.clients.add(client)
                finally:
                    channel.lock.release()
            '''
            #client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        print("[+] listening to " + str(address))
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    messageReceived = pickle.loads(data)
                    for clientToSend in messageReceived.channel.clients:
                        clientToSend.send(pickle.dumps(messageReceived))

                else:
                    raise Exception('Client disconnected')
            except:
                client.close()
                return False

    @check_channel("channel1")
    def date(self):
        date = datetime.now()
        message = Message("SERVER",self.channels[0],date.strftime("Today is : %d/%m"))
        #Envoyer le message au channel

if __name__ == "__main__":
    port_num = 8080
    ThreadedServer('',port_num).listen()
