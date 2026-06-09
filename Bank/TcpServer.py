# Author Names: Isabella Stephens, Sosan Wahid, Andrew Kivrak
# Created: November 2022
# Updated: November 2022

import os
import socket
import json
from datetime import datetime
from threading import Thread
import errno


class IServerListener():

    def __init__(self):
        pass

    def handleTcpMessage(self, conn, data):
        pass

    def handleNewConnection(self, conn):
        pass


class IClientListener():

    def __init__(self):
        pass

    def handleTcpMessage(self, data):
        pass

    def handleConnected(self, conn):
        pass

    def handleSocketClosed(self, conn):
        pass

    def handleClosedMessage(self, conn):
        pass

    def handleTimeout(self):
        pass


class BranchTcpClient(Thread):

    def __init__(self, ip, port, msgInterval):
        super().__init__()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._ip = ip
        self._port = port
        self._msgInterval = msgInterval
        self._startTime = datetime.now()
        self._listeners = []
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._client.connect((self._ip, self._port))
        self._client.settimeout(0)  # this makes the socket NON-BLOCKING

    def addListener(self, listener):
        self._listeners.append(listener)

    def notifyConnected(self):
        for listener in self._listeners:
            listener.handleConnected()

    def notifyTcpMessage(self):
        for listener in self._listeners:
            listener.handleTcpMessage()

    def notifySocketClosed(self):
        for listener in self._listeners:
            listener.handleSocketClosed()

    def notifyClosed(self):
        for listener in self._listeners:
            listener.handleClosedMessage()

    def notifyTimeout(self):
        for listener in self._listeners:
            listener.handleTimeout()

    def close(self):
        self._socket.close()
        print('TcpClient Closed.')

    def send(self, data):
        self._client.sendall(data)

    def run(self):

        while True:
            timeDelta = datetime.now().timestamp() - self._startTime.timestamp()  # .timestamp() gives us seconds
            if timeDelta >= self._msgInterval:
                self._startTime = datetime.now()
                self.notifyTimeout()
                print('Notified')

            try:
                data = self._client.recv(1024)
                if len(data) == 0:
                    continue  # nothing to parse

                msg = json.loads(data)
                print(msg)

                if msg['msg'] == 'connected':
                    self.notifyConnected()
                elif msg['msg'] == 'closed':
                    self.notifyClosed()
                    self._client.close()
                    break
                else:
                    self.notifyTcpMessage()
            except socket.timeout as timeout:
                # this is the expected error when nothing is in the
                # socket to receive. Catch it and move ons
                continue
            except socket.error as err:
                continue  # quick fix to error caused by windows
            except OSError as err:
                if err.errno == errno.EAGAIN:
                    continue  # socket has no data to handle. Just keep looping
                else:
                    print(err)
                    print('An error occured. Closing the socket.')
                    self._client.close()
                    self.notifySocketClosed()
                    break


class TcpServer(Thread):

    def __init__(self, ip, port):
        super().__init__()
        self._ip = ip
        self._port = port
        self._clientThreads = []
        self._listeners = []
        self._conns = []
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def addListener(self, listener):
        self._listeners.append(listener)

    def run(self):
        self._socket.bind((self._ip, self._port))
        print('Starting TCP Server')
        while True:
            self._socket.listen()
            conn, addr = self._socket.accept()

            print('New Client Connected..')
            self._conns.append(conn)
            for listener in self._listeners:
                listener.handleNewConnection(conn)
