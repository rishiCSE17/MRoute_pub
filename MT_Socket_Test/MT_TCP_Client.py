'''
    This code is developped for teaching purpose
    @author : Saptarshi Ghosh
    All rights reserved : London Sounthbank University
'''


# this code sends data over TCP

import socket
import time
import random

client_port=int(input('Enter port number \t : '))
host_ip=input('Enter Server IP \t : ')
host_port=int(input('Enter Server Port \t : '))
buffer_size=int(input('Enter Buffer size \t : '))
print('================= TRANSMISSION INITIATED ==============')

#initiate socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0',client_port))
s.connect((host_ip, host_port))

while True:
    #msg=input('Enter a message : ')
    msg=str(random.randint(1,100))
    time.sleep(3)
    msg_byte=str.encode(msg)
    s.send(msg_byte)
    print(f'| sent     \t | {msg_byte} \t |')
    data = s.recv(buffer_size)
    print(f'| received \t | {data} \t |')
    print('------------------------------------------')

s.close()

#print('recv data : ',data)