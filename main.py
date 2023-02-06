import subprocess
import threading
import time
import socket
from sys import executable
import random

import read_and_parse_datafile
import tools


rumor_counter_to_believ = 0
m = 0
koordinator_mat = []
total_waehler = 0
already_did_waehler = 0


def start_all_servers(own_datas, path_to_data, which_task, m, a_max, waehler, total_wahlberechtigt, p):
    print("__________________________")
    print(own_datas)
    subprocess.Popen([executable, 'start_all_servers.py', own_datas[0], own_datas[1], own_datas[2], path_to_data,
                      str(rumor_counter_to_believ), which_task, str(m),
                      str(a_max), str(waehler), str(total_wahlberechtigt), str(p)]
                     , creationflags=subprocess.CREATE_NEW_CONSOLE)


def start_counting_server_for_servers_who_believe_rumor():
    subprocess.Popen([executable, 'server_count_servers_who_believe_rumor.py'],
                     creationflags=subprocess.CREATE_NEW_CONSOLE)


def start_program():
    global total_waehler
    path_to_data = tools.ask_for_path()
    parsed_data = read_and_parse_datafile.parse_data(path_to_data)
    #which_task = tools.ask_for_which_task()
    which_task = "2"
    #p = tools.ask_for_p()
    p = 3
    if which_task == 1:
        global rumor_counter_to_believ
        rumor_counter_to_believ = tools.ask_for_counter_which_needs_for_believing()
    else:
        global m
        global a_max
        #m = 2
        #a_max = 2
        m = 2
        a_max = 2

    for x in range(0, len(parsed_data)):
        waehler = random.randrange(0, 2)
        if waehler == 1:
            total_waehler += 1
        start_all_servers(parsed_data[x], path_to_data, which_task, m, a_max, waehler, len(parsed_data), p)
        time.sleep(0.1)

    start_counting_server(parsed_data)

    #start_counting_server_for_servers_who_believe_rumor()


def start_counting_server(parsed_data):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('', 6000))
    serversocket.listen(1)
    while already_did_waehler < total_waehler:
        (clientsocket, address) = serversocket.accept()
        start_new_thread = threading.Thread(target=on_new_client,
                                            args=(clientsocket, parsed_data))
        start_new_thread.start()

    if already_did_waehler == total_waehler:
        zaehl_gewaehltem(parsed_data)
        serversocket.close()


def on_new_client(clientsocket, parsed_data):
    global already_did_waehler
    global koordinator_mat
    already_did_waehler += 1
    msg = clientsocket.recv(1024)
    msg = msg.decode()
    already_gewaehlt = False
    koordinator_mat.append(msg)


def zaehl_gewaehltem(parsed_data):
    highest_id = 0
    meisten_waehler = 0
    tmp_id = 0
    for x in range(0, len(koordinator_mat)):
        if int(koordinator_mat[x]) > highest_id:
            highest_id = int(koordinator_mat[x])
    for i in range(0, highest_id):
        aktuelle_waehler = 0
        for x in range(0, len(koordinator_mat)):
            if int(koordinator_mat[x]) == i:
                aktuelle_waehler += 1
        if aktuelle_waehler > meisten_waehler:
            meisten_waehler = aktuelle_waehler
            tmp_id = i

    snd_gewaehltem(parsed_data, tmp_id)


def snd_gewaehltem(parsed_data, id_des_gewaehlten):
    print(id_des_gewaehlten)
    print(parsed_data[int(id_des_gewaehlten) - 1][2])
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('127.0.0.1', int(parsed_data[int(id_des_gewaehlten) - 1][2])))
    msg = "Du bist der Koordinator"
    msg = msg.encode()
    clientsocket.send(msg)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_program()
