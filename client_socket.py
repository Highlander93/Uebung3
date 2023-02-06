import socket
from datetime import datetime

import read_and_parse_datafile
import tools


def start_client_socket():
    path_to_data = tools.ask_for_path()
    parsed_data = read_and_parse_datafile.parse_data(path_to_data)
    id_server = tools.ask_for_id()
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(parsed_data[int(id_server)-1][2])
    clientsocket.connect(('127.0.0.1', int(parsed_data[int(id_server)-1][2])))
    print('Bitte eine Message schreiben: ')
    msg = input()
    msg = msg.encode()
    clientsocket.send(msg)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S:%f")
    print("Current Time =", current_time)

    clientsocket.close()


if __name__ == '__main__':
    start_client_socket()
