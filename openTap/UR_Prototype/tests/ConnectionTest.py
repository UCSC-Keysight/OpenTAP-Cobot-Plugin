'''
This file runs a test that ensures there is a connection between the host system and the UR3e.
Before use, ensure that the UR3e is powered on.
Usage:
    python ConnectionTest.py -ip <UR3e IP address>
'''

import socket
import sys

def test_connection(address, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.settimeout(4)

        print(f"Connecting to {address}...")
        try:
            client_socket.connect((address, PORT))
        except socket.timeout as e:
            print("Timeout error:", e)
            return False
        except socket.error as e:
            print("Connection error:", e)
            return False
        print("Connection successful")

        print("Recieving data...")
        recieved = client_socket.recv(4096)
        if recieved is None:
            print("Failed to recieve data")
            return False
        print("Recieved data succeffuly")

    return True


if __name__=='__main__':
    # get address
    if "-ip" in sys.argv:
        address = sys.argv[sys.argv.index("-ip") + 1]
    else:
        print("Usage:\n\tpython ConnectionTest.py -ip <UR3e IP address>")
        quit()
        
    PORT = 30002
    result = test_connection(address, PORT)
    if result == False:
        print("Connection test failed")
    else:
        print("Connection test passed")




