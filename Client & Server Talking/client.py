# Author Names: Isabella Stephens, Sosan Wahid, Andrew Kivrak
# Created: October 2022
# Updated: November 2022

import threading
import socket


# receive from server
# receive from other client
def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'NICK': # sends nickname in
                print("Username: ")
                username = input()
                client.send(username.encode())
            else:
                print(message)
        except socket.error as err:
            print("Server shut down")
            client.close()
            break
        except:
            client.close()
            break


# write to server
def write():
    while True:
        message = f'{input("")}'
        try:
            client.send(message.encode())  # send message
        except socket.error as err:
            client.close()
            break
        except:
            print("An error occurred")
            client.close()
            break


if __name__ == "__main__":
    # type in server host and port
    # host = '192.168.0.21'; port = 8000
    host = input("Host: ")
    port = int(input("Port: "))

    try:
        # connect to server socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        # starts receive thread
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        # starts write thread
        write_thread = threading.Thread(target=write)
        write_thread.start()
    except:
        print("Could not connect to server")
