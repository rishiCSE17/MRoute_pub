'''
    This code is Developed for teaching purpose
    @author : Saptarshi Ghosh
    All rights reserved : London South Bank University
'''

import socket
import matplotlib.pyplot as plt
from drawnow import *
import numpy as np
import time
import threading as th
import json
import os
import MT_Socket_Test.ksg_generate as ksp
import networkx as nx

print_lock = th.Lock()

window = 3
host_ip = '127.0.0.1'
host_port = int(input(r'Enter the port number : '))
buffer_size = 15000

# where there are many sources you've to isolate data by their port numbers
data_dict = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', host_port))
s.listen(1)

data_arr = []
thread_list = []


def plotme():
    for k in list(data_dict.keys()):
        if len(data_dict[k]) > 0:
            plt.grid()
            plt.plot(list(np.arange(len(data_dict[k]))),
                     data_dict[k],
                     label=k)
            plt.legend()

def receiver_loop(conn, addr):
    global data_dict
    global plt

    while True:

        data = conn.recv(buffer_size)
        if not data:
            print('no data')
            data_dict.pop(addr[1])
            break
        #print('received data : ', data)

        with print_lock:
            data=json.loads(data)
            # addr is touple and port number in inedex 1
            if addr[1] not in list(data_dict.keys()):
                data_dict[addr[1]] = [data]
            else:
                if len(data_dict[addr[1]]) > window:
                    data_dict[addr[1]].pop(0)
                data_dict[addr[1]].append(data)

                #drawnow(plotme)

            for k in data_dict:
                print(f'Source Port {k} : {data_dict[k][-1]}')


            reply_data=ksp.main_ksp_generate(rt_dict=data_dict)
            conn.send(str.encode(json.dumps(reply_data)))


while True:
    print('Listening...')
    conn, addr = s.accept()
    print('Connection Address :', addr)
    t = th.Thread(target=receiver_loop, args=(conn, addr))
    t.start()
    thread_list.append(t)
    os.system('clear')

    time.sleep(5)