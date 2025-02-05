#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 13:37:22 2025

@author: lennart weinstock

This program receives an integer via UDP and displays a predefined image for each number.
"""
import socket
import threading
import os
from tkinter import Tk, Label, PhotoImage
import sys
import random

print('INFO: Starting program...')

# Setup of the UDP Receiver
master_dir = os.getcwd()
IP = "0.0.0.0"
PORT = 30_000
MAX_ACCEPTED_INT = 6
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((IP, PORT))
print(f'INFO: Socket to listen for integer data initialized. Listening to: {IP} via Port {PORT}.')

# Setup of the global flow variables
running = True
lock = threading.Lock()

# Method that closes threads and windows
def close_program(event):
    global running
    print("INFO: KeyboardInterrput detected. Stopping program.")
    running = False
    root.withdraw()
    root.destroy()
    sys.exit()

# This method gets used by the udp-receiver thread. It calls the update_image method, if an acceptable int was received
def listen_for_udp(update_image_callback):
    global running
    while running:
        data, addr = sock.recvfrom(1024)  # Empfang von Daten
        print(f'INFO: Received the data {data} from {addr[0]}.')
        try:
            int_received = int.from_bytes(data, byteorder='big')
            if int_received is not None:
                if int_received >= 0 and int_received <= MAX_ACCEPTED_INT:
                    update_image_callback(int_received)
                else:
                    print(f"WARNING: Received integer out of max range. Got {int_received} while only accepting up to {MAX_ACCEPTED_INT}.")
        except ValueError:
            print("WARNING: Data not compatible. Data received:", data)
        except KeyboardInterrupt:
            close_program()

# Method that changes the displayed image in regards to the received integer
def update_image(int_received):
    def update():
        next_image = PhotoImage(file=os.path.join(master_dir, f'images/tram_{int_received}.png'))
        label.config(image=next_image)
        label.image = next_image

    root.after(0, update)
    
# GUI Setup
root = Tk()
root.attributes('-fullscreen', True)
root.bind("<Escape>", close_program)
root.bind("<Button-1>", lambda event: update_image(random.randint(0, 2)))
label = Label(root)

# Set up a default image
default_image = PhotoImage(file=os.path.join(master_dir, 'images/tram_0.png'))
label.config(image=default_image)
label.image = default_image
label.pack()

# UDP listener in different thread -> parallel
udp_thread = threading.Thread(target=listen_for_udp, args=(update_image,))
udp_thread.daemon = True
udp_thread.start()

print('INFO: ... done!')

# Start of GUI
root.mainloop()

   


