#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import os
# HI Galaxy Hydrogen detector
# HIGH

def printFiles(direct):
    lsarray = os.listdir(direct)
    print('Choose an on source and off source file to calculate the spectrum:')
    for i in range(len(lsarray)):
        print(lsarray[i])

def askInputFiles():
    file1 = str(input('Name of file on source: '))
    file2 = str(input('Name of file off source: '))
    return file1, file2

live = False 
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
    print('The after processing pipline of HIGH is started')
    direct = './data/'
    printFiles(direct)
    
    file1, file2 = askInputFiles()
    #file1 = 'X_CygA_L_000_u_+0.00_+0.00'
    #file2 = 'X_CygA_L_000_r_+1.00_+0.00'

    freq = np.loadtxt(direct+file1,usecols=0)
    onsource = np.loadtxt(direct+file1,usecols=1)
    offsource = np.loadtxt(direct+file2,usecols=1)


    try:
        noline = str(input('Omit the central hydrogen line?'))
    except:
        noline = 'No'


    plt.plot(freq,onsource/offsource)
    if noline!='Yes':
        plt.axvline(x=1420.405,c='r')
    plt.show()

    while True:
        print('Do you want to do something else?')
        print('#'*60)
        print('1. I want to do a smoothing to the data (e.g. binning)!')
        print('2. I want to add more datasets of the same type!')
        print('3. I want to add a weighted average in the plot!')
        print('0. Nevermind, I want to quit!')
        print('#'*60)
        while True: 
            option = int(input('Which option do you want to do? '))
            if option == 1 or option==2 or option == 3 or option ==4:
                break
            else: 
                print('Specify a valid input!')
        if option == 1:
            smoothingfac = int(input('What is the smoothing factor? '))
            lensmooth = int(np.floor(len(onsource)/smoothingfac))
            #print(lensmooth)
            #print(np.zeros(lensmooth+1))
            onsourcesmooth = np.zeros(lensmooth+1)
            offsourcesmooth = np.zeros(lensmooth+1)
            freqsmooth = np.zeros(lensmooth+1)
            #onsourcesmooth = np.zeros((lensmooth+1.))
            #offsourcesmooth = np.zeros((lensmooth+1.))
            
            for i in range(lensmooth):
                onsourcesmooth[i] = np.sum(onsource[i*smoothingfac:(i+1)*smoothingfac])/smoothingfac
                offsourcesmooth[i] = np.sum(offsource[i*smoothingfac:(i+1)*smoothingfac])/smoothingfac
                freqsmooth[i] =np.sum(freq[i*smoothingfac:(i+1)*smoothingfac])/smoothingfac
            onsourcesmooth[-1]= np.sum(onsource[-1:-smoothingfac])/smoothingfac
            offsourcesmooth[-1]= np.sum(offsource[-1:-smoothingfac])/smoothingfac   
            freqsmooth[-1] = np.sum(freq[-1:-smoothingfac])/smoothingfac      
            plt.plot(freqsmooth,onsourcesmooth/offsourcesmooth)
            if noline!='Yes':
                plt.axvline(x=1420.405,c='r')
            plt.show()
            
            
        elif option==2:
            printFiles(direct)
            file1new, file2new = askInputFiles()
            onsource2 = np.loadtxt(direct+file1new,usecols=1)
            offsource2 = np.loadtxt(direct+file2new,usecols=1)
            try: 
                notequal = str(input('Is the integration time different? '))
            except:
                notequal = 'No' 
            if notequal == 'No':
                onsourcenew = (onsource+onsource2)/2
                offsourcenew = (offsource+offsource2)/2
            else:
                weight1 = int(input('Total time current measurement? '))
                weight2 = int(input('Total time new measurement? '))
                onsourcenew = (onsource*weight1 + onsource2*weight2)/(weight1+weight2)
                offsourcenew = (offsource*weight1 + offsource2*weight2)/(weight1+weight2)

            plt.plot(freq,onsourcenew/offsourcenew,label='Combined Measurement')
            plt.plot(freq,onsource/offsource,label='Old Measurement')
            if noline!='Yes':
                plt.axvline(x=1420.405,c='r')
            plt.legend()
            plt.show()
            
            try:
                usenewset = str(input('Press enter if you want to keep this set, otherwise type NO.'))
            except:
                usenewset = True

            if usenewset:
                onsource = onsourcenew
                offsource = offsourcenew
            del onsourcenew
            del offsourcenew
            del onsource2
            del offsource2

            

        elif option==3:
            print('test')
        elif option==0:
            print('Thanks for using HIGH! :-)')
            exit(0)




