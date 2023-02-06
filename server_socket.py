import os
import socket
import sys
import threading
import time
import graphviz

from graphviz import Source

import read_and_parse_datafile
import tools

already_known_rumor = ''
already_known_rumor_counter = 0
rumor_counter_to_believ = 0


def on_new_client(clientsocket, servers_you_wanna_connect, own_datas, serversocket, address):
    print("\n" + tools.get_current_time() + ' client connected', end="")
    msg = clientsocket.recv(1024)
    msg = msg.decode()

    print(msg, end="")

    if str(msg).startswith('Mein Konto: '):
        print("\n" + tools.get_current_time() + ' Konto: ' + "\"", end="")
    else:
        print("\n" + tools.get_current_time() + ' Message: ' + "\"" + msg + "\"", end="")

    clientsocket.close()
    print("\n" + tools.get_current_time() + ' client disconnected', end="")


def start_server_socket(own_datas, path_to_data):
    global rumor_counter_to_believ
    rumor_counter_to_believ = int(own_datas[3])
    try:
        just_send_your_id_once = False
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("\n" + tools.get_current_time() + ' My ID: ' + own_datas[0], end="")
        servers_you_wanna_connect = get_next_servers(own_datas, path_to_data)
        print("\n" + tools.get_current_time() + " Meine Nachbarn: " + str(servers_you_wanna_connect), end="")
        serversocket.bind(('', int(own_datas[2])))
        serversocket.listen(5)
        print("\n" + tools.get_current_time() + ' Waiting for client ...', end="")
        while True:
            (clientsocket, address) = serversocket.accept()

            start_new_thread = threading.Thread(target=on_new_client,
                                                args=(clientsocket, servers_you_wanna_connect, own_datas,
                                                      serversocket, address))
            start_new_thread.start()

            if just_send_your_id_once:
                if len(servers_you_wanna_connect) > 0:
                    for x in range(0, len(servers_you_wanna_connect)):
                        if servers_you_wanna_connect[x][0] != own_datas[0]:
                            print("\n" + tools.get_current_time() + servers_you_wanna_connect[x][1] + ":" +
                                  servers_you_wanna_connect[x][2], end="")
                            neighbor_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            neighbor_client_socket.connect(
                                (str(servers_you_wanna_connect[x][1]), int(servers_you_wanna_connect[x][2])))
                            id_in_message = 'Meine ID ist: ' + own_datas[0]
                            id_in_message = id_in_message.encode()
                            neighbor_client_socket.send(id_in_message)
                            neighbor_client_socket.close()
                just_send_your_id_once = False

        serversocket.close()
    except:
        print(sys.exc_info()[0])
        time.sleep(5)
        # start_server_socket(own_datas, path_to_data)


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
        print(sys.exc_info()[0])
        time.sleep(5)


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
        print(sys.exc_info()[0])
        time.sleep(5)
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


def kill_all_servers(msg, servers_you_wanna_connect, own_datas, address):
    tell_anything_to_neighbors(msg, servers_you_wanna_connect, own_datas, address)


def kill_yourself():
    print("\n" + tools.get_current_time() + ' This Server is shutting down ...', end="")
    time.sleep(10)
    os._exit(1)


def handle_rumor(msg, servers_you_wanna_connect, own_datas, address):
    try:
        global already_known_rumor_counter
        global already_known_rumor

        rumor = str(msg).split('rumor: ')[1]
        already_known_rumor_counter += 1
        if already_known_rumor != rumor:
            already_known_rumor = rumor
            tell_rumor(msg, servers_you_wanna_connect, own_datas, address)

        if already_known_rumor_counter == rumor_counter_to_believ:
            print("\n" + tools.get_current_time() + " I believing the rumor: " + "\"" +
                  already_known_rumor + "\"", end="")
            send_your_id_to_counter_server(own_datas[0])
    except:
        print(sys.exc_info()[0])
        time.sleep(50)


def tell_rumor(rumor, servers_you_wanna_connect, own_datas, address):
    tell_anything_to_neighbors(rumor, servers_you_wanna_connect, own_datas, address)


def tell_anything_to_neighbors(msg, servers_you_wanna_connect, own_datas, address):
    try:
        msg = msg.encode()
        if len(servers_you_wanna_connect) > 0:
            for x in range(0, len(servers_you_wanna_connect)):
                try:
                    if servers_you_wanna_connect[x][0] != own_datas[0] and \
                            (int(servers_you_wanna_connect[x][2]) != int(address[1])):
                        neighbor_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        neighbor_client_socket.connect((str(servers_you_wanna_connect[x][1]),
                                                       int(servers_you_wanna_connect[x][2])))
                        neighbor_client_socket.send(msg)
                        neighbor_client_socket.close()
                except ConnectionRefusedError:
                    pass

    except:
        print(sys.exc_info()[0])
        time.sleep(50)


def send_your_id_to_counter_server(own_id):
    socket_to_counter_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_to_counter_server.connect(('127.0.0.1', 5555))
    msg = str(own_id)
    msg = msg.encode()
    socket_to_counter_server.send(msg)
    socket_to_counter_server.close()

