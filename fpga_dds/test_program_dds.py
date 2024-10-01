import socket
from time import sleep

def trigger(sock, dest, print_only=False):
    tosend = bytearray.fromhex(f"A200")
    if print_only:
        print(tosend)
    else:
        sock.sendto(tosend, dest)

def turn_ch1_on(ftw, atw, ptw, sock, dest, print_only=False):
    ftw_hex = f"{ftw:09x}"  # 36-bit FTW
    atw_hex = f"{atw:02x}"  # 8-bit ATW
    ptw_hex = f"{ptw:04x}"  # 16-bit PTW

    messages = [
        f"a1000000 00000000",
        f"a1100000 00000000",
        f"a1200000 {ftw_hex[1:]}",
        #f"a1300000 00000{atw_hex}{ftw_hex[0]}",
        f"a1300000 0{ptw_hex}{atw_hex}{ftw_hex[0]}",
        f"a1000001 00000000",
        f"a1100001 00000000",
        f"a1200001 00000000",
        f"a1300001 00000000",
        f"a1010000 00000000",
        f"a1110000 00000000",
        f"a1210000 00000000",
        f"a1310000 00000000",
        f"a1020000 00000000",
        f"a1120000 00000000",
        f"a1220000 00000000",
        f"a1320000 00000000",
        f"a1030000 00000000",
        f"a1130000 00000000",
        f"a1230000 00000000",
        f"a1330000 00000000"
    ]

    for msg in messages:
        tosend = bytearray.fromhex(msg)
        if print_only:
            print(f"Message: {msg} -> Bytearray: {tosend.hex()}")
        else:
            sock.sendto(tosend, dest)

timeout = 1.02
port = 804
host = '192.168.1.110'
dest = (host, int(port))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.settimeout(timeout)

# constant output with the following parameters
#ftw = 0x155555555  # 36-bit FTW
ftw = 0x111111111  # 36-bit FTW
#ftw = 0x444444444  # 36-bit FTW
atw = 0xff  # 8-bit ATW
ptw = 0x0000 # 16-bit PTW

Nbits = 36
Fmax = 150e6
print(f'freq: {ftw/(2**Nbits)*Fmax}')

turn_ch1_on(ftw, atw, ptw, sock, dest,print_only=False)
sleep(0.1)
trigger(sock, dest)
