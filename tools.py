from datetime import datetime


def ask_for_path():
    # Use a breakpoint in the code line below to debug your script.
    # print('Please insert path to data: ', end="")
    # return input()
    return "C:\\Users\\Müller\\PycharmProjects\\Uebung3\\PfadZurDatei\\data.txt"
    # return "C:\\Users\\muell\\PycharmProjects\\Uebung1\\PfadZurDatei\\data.txt"


def get_anzahl_server_fuer_startnachricht():
    print("\n" + get_current_time() + '\t Du bist der Koordinator. Bitte gib die Sekunden an, in der du periodisch die Informationen welche Werte die Konten haben einsammelst: ', end="")
    return input()


def ask_for_id():
    print('Please insert ID: ', end="")
    return input()


def ask_for_p():
    print('Please insert number of neighbors(p): ', end="")
    return input()


def ask_for_counter_which_needs_for_believing():
    print('Please insert Anzahl an Server von denen man ein Gerücht hören muss um dieses zu glauben: ', end="")
    return input()


def ask_for_which_task():
    print('Please insert the task you want: ', end="")
    return input()


def get_m():
    print('Please insert max time m: ', end="")
    return input()


def get_a_max():
    print('Please insert maximal Abstimmungsrunden: ', end="")
    return input()


def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S:%f")
