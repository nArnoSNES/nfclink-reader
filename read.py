import serial,re,time

try:
    ser = serial.Serial(port='COM6',baudrate=115200)
except:
    exit('Reader not detected')

def send(t,l=-1):
    # TODO: read payload length to avoid reading 2 RSP at the same time
    ser.write(t.replace(" ","").decode("hex"))
    time.sleep(0.2)
    if (l==-1):
        l = ser.inWaiting()
    r = ser.read(l)
    return ' '.join(re.findall('.{2}',r.encode("hex")))

def get():
    l = ser.inWaiting()
    r = ser.read(l)
    return ':'.join(re.findall('.{2}',r[11:19].encode("hex")))

def init():
    send("20 00 01 01") # CORE_RESET
    send("20 01 00") # CORE_INIT
    send("22 00 01 01") # NFCEE_DISCOVER
    send("21 00 19 08 01 01 01 02 01 01 03 01 01 04 01 02 05 01 03 05 02 03 04 02 02 86 01 01") # RF_DISCOVER_MAP
    send("20 02 0d 04 d0 01 81 11 01 01 81 01 01 80 01 00") # CORE_SET_CONFIG

def discover():
    send("21 03 03 01 06 01",4) # RF_DISCOVER (get only 4 bytes to avoid trapping RF_INTF_ACTIVATED_NTF at the same time)

def deactivate(t,l):
    send("21 06 01 %s" % t,l) # RF_DEACTIVATE (00 => go to idle state, 03 => go back to discover state)

init()
discover()

while True:
    while not ser.inWaiting():
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            deactivate("00",4)
            ser.close()
            exit('User exit!')
    
    print(get())
    time.sleep(2)
    deactivate("03",9) # (get only 9 bytes to avoid trapping RF_INTF_ACTIVATED_NTF at the same time)

