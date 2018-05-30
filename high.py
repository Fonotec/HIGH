#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
# HI Galaxy Hydrogen detector
# HIGH

live = True #False 
obstime = 1/60
if live:
    totaltime = obstime*60
    totalitt = int(totaltime*2136)

    # define the correct data format for the output of the telescope
    try:
        unsignint = np.dtype(np.uint32)

        # construct the socekt
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # get socket info
        sinfo = socket.getaddrinfo('0.0.0.0',22102)

        # bind with the backend
        s.bind(('0.0.0.0',22102))
        #s.connect(('10.1.2.3',22102))

        # receive one package
        a = s.recv(2048)
    except:
        print('This mode is not available when not using the telescope, please visit the telescope to use the live options of HIGH.')
        exit(0)

    onsource = np.zeros(512)
    for i in range(totalitt):
        a = s.recv(2048)
        for j in range(1,512):
            onsource[j-1] += int.from_bytes(a[4*(j-1):4*j],byteorder='big')

    input("Point the telescope off the source and press Enter to continue...")

    offsource = np.zeros(512)
    for i in range(totalitt):
        a = s.recv(2048)
        for j in range(1,512):
            offsource[j-1] += int.from_bytes(a[4*(j-1):4*j],byteorder='big')

    print('Completed observation')
    

    plt.plot(onsource/offsource)
    plt.show()

else:
    direct = './data/'
    file1 = 'X_CygA_L_000_u_+0.00_+0.00'
    file2 = 'X_CygA_L_000_r_+1.00_+0.00'

    freq = np.loadtxt(direct+file1,usecols=0)
    onsource = np.loadtxt(direct+file1,usecols=1)
    offsource = np.loadtxt(direct+file2,usecols=1)

    plt.plot(freq,onsource/offsource)
    plt.show()



