import socket
import sys
import threading
import time
import random

from graphviz import Source

import read_and_parse_datafile
import tools

lock = threading.Lock()
your_favorite_time = 0
m = 0
p = 0
a_max = 0
a_now = 0
s = 0
send_ones = True
koordinator = False
own_initiator = 0
random_money = random.randint(0, 100000)
send_konto = 5
gegenpart = 0
msg_response = ""
prozentsatz = 0


def on_new_client(clientsocket, own_datas, servers_you_wanna_connect, address, all_servers_in_list):
    lock.acquire()
    global koordinator
    global your_favorite_time
    global a_now
    global s
    global send_ones
    global own_initiator
    global random_money
    global gegenpart
    global msg_response
    global prozentsatz

    msg = clientsocket.recv(1024)
    msg = msg.decode()

    if msg == 'Du bist der Koordinator':
        koordinator = True
        start_new_thread = threading.Thread(target=periodic_ask_money,
                                            args=(tools.get_anzahl_server_fuer_startnachricht()))
        start_new_thread.start()
        #snd_random_server_your_time(s, all_servers_in_list)

    if str(msg).startswith("Kontostand wurde verarbeitet"):
        print("\n" + "Kontostand wurde von dem anderen Konto ueberarbeitet")
        kontostand_anderer = msg.split('::')[1]
        old_random_money = random_money
        if float(kontostand_anderer) >= float(random_money):
            random_money = random_money + float(kontostand_anderer)*(0+(prozentsatz / 100))
        else:
            random_money = random_money - float(kontostand_anderer) * (0 + (prozentsatz / 100))

        print("\nKontostand wurde vom Wert: " + str(old_random_money) + " mittels des Prozentsatzes: " + str(prozentsatz) + " zu dem neuen Wert: " + str(random_money) + " aktualisiert")


    if str(msg).startswith("Kontostand::"):
        msg1 = msg.split('::')[0]
        msg2 = msg.split('::')[1]
        msg3 = msg.split('::')[2]
        msg4 = msg.split('::')[3]

        prozentsatz = int(msg4)
        old_random_money = random_money
        if int(msg2) >= random_money:
            random_money = random_money + int(msg2)*(0+(prozentsatz / 100))
        else:
            random_money = random_money - int(msg2) * (0 + (prozentsatz / 100))

        gegenpart = int(msg3)

        msg_response = "Kontostand wurde verarbeitet" + "::" + str(old_random_money)
        msg_response = msg_response.encode()
        #print("\nKontostand wurde vom Wert: " + str(old_random_money) + " mittels des Prozentsatzes: " + str(prozentsatz) + " zu dem neuen Wert: " + str(random_money) + " aktualisiert")
        resend_your_konto()

    clientsocket.close()
    lock.release()


def periodic_ask_money(seconds):
    while True:
        time.sleep(int(seconds))
        #todo

def start_server_socket(own_datas, path_to_data):
    try:
        who_is_koordinator(own_datas[6], own_datas[7])
        global your_favorite_time
        global m
        global a_max
        global p
        global random_money
        global send_konto

        konto = random_money
        p = int(own_datas[8])
        a_max = int(own_datas[5])
        m = int(own_datas[4])
        your_favorite_time = random.randrange(1, m, 1)
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("\n" + tools.get_current_time() + '\t My ID: ' + own_datas[0], end="")
        servers_you_wanna_connect = get_next_servers(own_datas, path_to_data)
        print("\n" + tools.get_current_time() + '\t Meine Nachbarn: ' + str(servers_you_wanna_connect), end="")
        serversocket.bind(('', int(own_datas[2])))
        serversocket.listen(5)
        print("\n" + tools.get_current_time() + '\t Aktuelles Guthaben: ' + str(konto) + "€", end="")

        print("\n" + tools.get_current_time() + '\t Anzahl Knoten: ' + str(own_datas[7]), end="")

        for x in range(send_konto):
            send_your_konto(konto, own_datas[7], own_datas[2])
            time.sleep(random.randint(0, 1))

        print("\n" + tools.get_current_time() + '\t Waiting for client ...', end="")

        while True:
            (clientsocket, address) = serversocket.accept()

            start_new_thread = threading.Thread(target=on_new_client,
                                                args=(clientsocket, own_datas, servers_you_wanna_connect, address,
                                                      read_and_parse_datafile.parse_data(path_to_data)))
            start_new_thread.start()

        serversocket.close()
    except:
        time.sleep(1)


def resend_your_konto():
    try:
        global msg_response
        neighbor_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        neighbor_client_socket.connect(("127.0.0.1", gegenpart))
        neighbor_client_socket.send(msg_response)
        neighbor_client_socket.close()

    except:
        time.sleep(1)



def send_your_konto(konto, anzahl_knoten, own_port):
    try:
        global prozentsatz
        time.sleep(random.randint(0, 3))
        own_portt = int(own_port)
        random_port = int(own_port)
        prozentsatz = random.randint(0, 100)

        while random_port == own_portt:
            random_port = random.randint(0, int(anzahl_knoten)) + 5000

        neighbor_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        neighbor_client_socket.connect(("127.0.0.1", int(random_port)))
        msg = "Kontostand::" + str(konto) + "::" + str(own_port) + "::" + str(prozentsatz)
        msg = msg.encode()
        neighbor_client_socket.send(msg)
        neighbor_client_socket.close()

    except:
        time.sleep(1)


def get_next_servers(own_datas, path_to_data):
    try:
        all_servers_in_list = read_and_parse_datafile.parse_data(path_to_data)
        servers_you_wanna_connect = []
        i = 0
        nachbarknoten_aus_graphen = True
        if nachbarknoten_aus_graphen:
            edges = read_and_decode_graph()

            servers_you_wanna_connect_ids = get_ids_i_wanna_connect(edges, own_datas)
            if len(servers_you_wanna_connect_ids) > 0:
                servers_you_wanna_connect = get_servers_with_id(servers_you_wanna_connect_ids, all_servers_in_list)
        else:
            if len(all_servers_in_list) > 1:
                for x in range(int(own_datas[0][0]), int(own_datas[0][0]) + 3):
                    servers_you_wanna_connect.append(all_servers_in_list[(x % len(all_servers_in_list))])
                    i += 1
        return servers_you_wanna_connect
    except:
        time.sleep(1)


def get_servers_with_id(servers_you_wanna_connect_ids, all_servers_in_list):
    servers_you_wanna_connect = []
    for x in range(0, len(all_servers_in_list)):
        for y in range(0, len(servers_you_wanna_connect_ids)):
            if str(all_servers_in_list[x][0]) == str(servers_you_wanna_connect_ids[y]):
                servers_you_wanna_connect.append(all_servers_in_list[x])
    return servers_you_wanna_connect


def get_ids_i_wanna_connect(edges, own_datas):
    ids_i_wanna_connect_with = []
    for x in range(0, len(edges)):
        left_id = edges[x].split(" -- ")[0]
        right_id = edges[x].split(" -- ")[1]
        if str(left_id) == str(own_datas[0]):
            if already_exist(ids_i_wanna_connect_with, right_id):
                ids_i_wanna_connect_with.append(right_id)
        if str(right_id) == str(own_datas[0]):
            if already_exist(ids_i_wanna_connect_with, left_id):
                ids_i_wanna_connect_with.append(left_id)
    return ids_i_wanna_connect_with


def get_ids_for_connection(edges, own_datas):
    try:
        edges_with_my_id = []
        servers_you_wanna_connect_ids = []
        for x in range(0, len(edges)):
            if edges[x].find(str(own_datas[0])) >= 0:
                edges_with_my_id.append(edges[x])
        if len(edges_with_my_id) > 0:
            for y in range(0, len(edges_with_my_id)):
                left_id = edges_with_my_id[y].split(" -- ")[0]
                right_id = edges_with_my_id[y].split(" -- ")[1]
                if str(left_id) != str(own_datas[0]):
                    if already_exist(servers_you_wanna_connect_ids, left_id):
                        servers_you_wanna_connect_ids.append(left_id)
                else:
                    if not already_exist(servers_you_wanna_connect_ids, right_id):
                        servers_you_wanna_connect_ids.append(right_id)
    except:
        time.sleep(1)
    return servers_you_wanna_connect_ids


def already_exist(servers_you_wanna_connect_ids, check_this_id):
    for i in range (0, len(servers_you_wanna_connect_ids)):
        if str(servers_you_wanna_connect_ids[i]) == str(check_this_id):
            return False
    return True


def read_and_decode_graph():
    path = './graphen/Graph_Aus_graphgen.dot'
    s = Source.from_file(path)
    dirty_edges = s.source.split("\n\t")
    filtered_edges = []
    for x in range(0, len(dirty_edges)):
        if dirty_edges[x].find("--") >= 0:
            filtered_edges.append(dirty_edges[x])

    filtered_edges[len(filtered_edges) - 1] = \
        filtered_edges[len(filtered_edges) - 1].replace('\n}\n', '')
    return filtered_edges


def snd_your_favorite_time_to_neighbor(servers_you_wanna_connect, own_datas, address):
    try:
        if a_now <= a_max:
            your_favorite_time_msg = str(your_favorite_time).encode()
            if len(servers_you_wanna_connect) > 0:
                for x in range(0, len(servers_you_wanna_connect)):
                    try:
                        if servers_you_wanna_connect[x][0] != own_datas[0] and \
                                (int(servers_you_wanna_connect[x][2]) != int(address[1])):
                            neighbor_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            neighbor_client_socket.connect((str(servers_you_wanna_connect[x][1]),
                                                            int(servers_you_wanna_connect[x][2])))
                            neighbor_client_socket.send(your_favorite_time_msg)
                            neighbor_client_socket.close()
                    except ConnectionRefusedError:
                        pass
    except:
        time.sleep(1)


def who_is_koordinator(waehler, total_waehler):
    if int(waehler) == 1:
        socket_to_counter_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_to_counter_server.connect(('127.0.0.1', 6000))
        msg = str(random.randrange(1, int(total_waehler)+1))
        msg = msg.encode()
        socket_to_counter_server.send(msg)
        socket_to_counter_server.close()


def send_your_id_to_counter_server(own_id):
    socket_to_counter_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_to_counter_server.connect(('127.0.0.1', 5555))
    msg = "My ID: " + str(own_id) + "\t My favorite time: " + str(your_favorite_time)
    msg = msg.encode()
    socket_to_counter_server.send(msg)
    socket_to_counter_server.close()


def snd_random_server_your_time(s, all_servers_in_list):
    your_favorite_time_msg = str(your_favorite_time).encode()
    for x in range(0, int(s)-1):
        random_number = random.randrange(0, len(all_servers_in_list), 1)
        socket_to_start_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_to_start_server.connect(('127.0.0.1', int(all_servers_in_list[random_number][2])))
        socket_to_start_server.send(your_favorite_time_msg)
        print("\n" + tools.get_current_time() + '\t Sende Startnachricht an Server mit der ID: ' +
              str(random_number), end="")
