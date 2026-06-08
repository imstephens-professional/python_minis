import threading
import socket
import sys
from threading import Thread, Lock, Timer


# after username login, ask for client to talk to
def handle(client):
    try:
        msg = 'Do you want to quit?'
        client.send(msg.encode())
        do_quit = client.recv(1024).decode()
        if do_quit == 'quit':
            print('A client is trying to quit')
    except:
        print("Error from client's side")
        client.close()

    loop = [True, 0]
    while (loop[0] != False) or (loop[1] == 1):
        try:
            msg = 'Username of recipient: '
            client.send(msg.encode())
            user_wanted = client.recv(1024).decode()
            loop = find_user_login(user_wanted)

            if loop[1] == 1:
                msg = '{} does not exist on the database'.format(user_wanted)
                client.send(msg.encode())
            elif loop[0] == True:
                msg = '{} is offline'.format(user_wanted)
                client.send(msg.encode())
        except:
            print("Error from client's side")
            client.close()
            break

    # in order to get this far, the client must be online and in the database
    # save information here
    recipient = client_info(user_wanted)
    index = clients.index(recipient)
    while True:
        try:  # constantly tries to get message from the client
            message = client.recv(1024)
            online_yes = online[index]  # checks if recipient is still online
            print('{} is online? {}'.format(user_wanted, online_yes))

            if online_yes:
                recipient.send(message)
            else:
                msg = '{} is offline'.format(user_wanted)
                client.send(msg.encode())
                break
        except socket.error as err:  # if you can no longer reach the client, say client is offline
            index = clients.index(client)
            online[index] = False  # set to offline
            client.close()
            break
        except Exception as err:
            print(err)
            print('An error occurred. Closing socket.')
            print('A client has disconnected')
            client.close()
            break

    print('A client has disconnected')
    client.close()
    sys.exit()


# user wants to contact someone so take the info here
def client_info(username):
    index = usernames.index(username)
    recipient = clients[index]
    return recipient


# checks to see if the user is present in "database" of clients
def find_user_login(username):
    arr = [True, 1]  # automatically assumes user is in db and needs to be added

    mutex.acquire()
    for i in usernames:
        if i == username:
            index = usernames.index(username)
            online_status = online[index]
            if online_status:
                arr = [False, 0]  # user is online
            else:
                arr = [True, 0]  # user is offline

    mutex.release()
    return arr


def user_login(client):
    loop = [False, 0]
    # WARNING: NO TRY-CATCH BLOCK HERE, SO IF THIS FAILS, CRASHES WHOLE SERVER
    while loop[0] != True:  # username check
        # gets username from server
        client.send('NICK'.encode())
        username = client.recv(1024).decode()
        loop = find_user_login(username)

        if loop[0] == False:  # user is present in db and still online
            msg = "Error: User is still online"
            client.send(msg.encode())

        if loop[1] == 1:  # if returns a 1, then user was not found in database
            usernames.append(username)
            clients.append(client)
            online.append(True)

    # if made it this far, make sure this user's status is set to online
    index = usernames.index(username)
    online[index] = True
    # refreshes the client in case the same person is logging into a new computer
    clients[index] = client

    try:
        client.send('Connected to the server!\n'.encode())  # tells client is in server

        client.send('Current users online: '.encode())
        # prepares to send client list of users that are online
        for username in usernames:
            index = usernames.index(username)
            if online[index] == True:
                msg = "{}, ".format(username)
                client.send(msg.encode())
        handle(client)
    except:
        print('Error on client side')
        client.close()


# receives/accepts clients
# starts a thread for every accepted client
def receive():
    while True:
        client, address = server.accept()  # accept clients all the time
        print(f'Connected with {str(address)}')  # server tells a person connected to them

        # you need to interpret them one at a time, so start thread
        thread = threading.Thread(target=user_login, args=(client,))
        thread.start()


if __name__ == "__main__":
    # put lines 4-10 into the main method
    host = '192.168.0.21'  # will need to change based on the IP of the machine-
    port = 8000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()  # starts listening for clients

    mutex = Lock()

    # list of clients and their nicknames
    # you need to put this in the database instead
    clients = []
    usernames = []
    online = []

    print("Server is listening...")
    receive()  # main method
