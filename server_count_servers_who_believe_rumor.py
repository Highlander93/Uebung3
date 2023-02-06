# Press the green button in the gutter to run the script.
import sys
import threading
import time
import socket

counter_server_who_believe_rumor = 0
list_server_who_believe = []

def start_program():
    try:
        start_server()
    except:
        print(sys.exc_info()[0])
        time.sleep(50)


def start_server():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('', 5555))
    serversocket.listen(1)
    print('Waiting for client ...')
    while True:

        (clientsocket, address) = serversocket.accept()

        start_new_thread = threading.Thread(target=on_new_client, args=(clientsocket, "hi"))
        start_new_thread.start()

    serversocket.close()


def on_new_client(clientsocket, hi):
    msg = clientsocket.recv(1024)
    msg = msg.decode()
    global list_server_who_believe
    global counter_server_who_believe_rumor
    believe_already = False
    for x in range(0, len(list_server_who_believe)):
        if list_server_who_believe[x] == msg:
            believe_already = True
    if not believe_already:
        list_server_who_believe.append(msg)
        counter_server_who_believe_rumor += 1
        #print('ID von Server: ' + str(msg))
        print(msg)
    clientsocket.close()


if __name__ == '__main__':
    start_program()

