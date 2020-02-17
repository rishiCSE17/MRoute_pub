import json
import socket
import time
import os
import networkx as nx

'''
* dict_rt is a dictionary representing the routing table (RT)
* the dictioary is encapsulated in JSON while transfering
* Transfer takes place in TCP for this Test Unit
* In actual implementation it would use MQTT and XMPP 
* the RT is taken as input in this test unit
* in Actual implementation the input will be replaced by
  a ShellScript that will fetch the routing table from Quagga
  software routers and populate the dictionary
* there are three keys
    1. proc : the port number at which the code is running
    2. alan : a list of neighbour networks' addresses 
    3. awan : Point to point link address is the neighbour routers' IPs
'''

dict_rt = {}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
timer = 10
buffer_size = 1500


def show_sp(topo, src, dst, plot=True):
    spath = nx.shortest_path(topo, src, dst)

    if plot:
        pos = nx.spring_layout(topo)
        nx.draw_networkx(topo, pos, node_color='w')
        nx.draw_networkx_nodes(topo,
                               pos,
                               nodelist=spath,
                               node_shape='d',
                               node_color='g',
                               axis=None
                               )
        plt.axis('off')
        plt.show()
    return spath


def populate_dict_rt():
    global dict_rt
    dict_rt['proc'] = int(input('Enter process id (10000 - 15000 )\t : '))
    dict_rt['alan'] = input('Enter LAN net ids \t : ').split(' ')
    dict_rt['awan'] = input('ENter WAN IPs \t : ').split(' ')


def init_socket():
    global s
    global buffer_size

    process_id = dict_rt['proc']
    cont_ip = input('Enter Server IP : ')
    cont_port = int(input('Enter Server Port : '))
    buffer_size = 1500  # input('Enter Buffer size : ')

    print('================= TRANSMISSION INITIATED ==============')
    # initiate socket
    s.bind((cont_ip, process_id))
    # only receives acknowledgement from the designated server
    s.connect((cont_ip, cont_port))


def client_loop():
    populate_dict_rt()  # populating the routing table

    datagram = json.dumps(dict_rt)  # file encapsulated in json

    # test
    print(type(datagram))
    print(datagram)

    init_socket()  # initiating socket
    try:
        while True:
            egress_data = str.encode(datagram)  # sending local routing table
            s.send(egress_data)
            print(f'[SENT] <-- {egress_data}')

            ingress_data = json.loads(s.recv(buffer_size))  # receiving all pair shorst paths
            print(f'[RCVD] --> ')
            for entry in ingress_data:
                print(f"{entry['src']} --> {entry['dst']}")
                print(f"\t{entry['ksp']}")

            print('------------------------------------------------------')

            time.sleep(timer)
            os.system('clear')
    except KeyboardInterrupt:
        s.close


client_loop()
