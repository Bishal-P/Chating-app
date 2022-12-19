

import socket
import sys
from threading import Thread

all_clients={}

def client_thread(client,username):
    global all_clients
    flag1=0
    friend=""
    try:
        while True:
            data=client.recv(1024).decode("ascii")
            data=data.split("+--")
            print("data recived in server =",data)
            friend=data[0]
            print("server seceived the friend name is :",friend)
            data_received=data[1]
            if data_received=="" or data_received==" ":
                continue
            if friend in all_clients:
                data_received2=username+"+--"+data_received
                print("Message sent by server :",data_received2)
                data_received2=data_received2.encode("ascii")
                all_clients[friend].sendall(data_received2)
    except:
        try:
            if friend in all_clients:
                msg1=f"{username}+--{username} is Offline now"
                msg1=msg1.encode("ascii")
                all_clients[friend].send(msg1)
                print("Error 1 handled properly")
            client.close()
        except:
            print("Error 2 handled properly")


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server:
    server.bind(("192.168.29.86",5555))
    server.listen()
    while True:
        try:
            client,addr=server.accept()
            print("Client attached successfully...")
            username=client.recv(2024).decode("ascii")
            all_clients[username]=client
            t1=Thread(target=client_thread,args=(client,username))
            t1.start()
        except Exception as e:
            print("The error is :",e)













