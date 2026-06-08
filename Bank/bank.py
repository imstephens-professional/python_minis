import time
import random
from datetime import datetime
import socket
import json
from TcpServer import TcpServer, IServerListener

from threading import Thread, Lock, Timer

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


# This is the TCP Client spawned from the server
class BranchClient(Thread):

    def __init__(self, connection, msg_callback):
        super().__init__()
        self._client = connection
        self._isOpen = True
        self._callback = msg_callback

    def sendResponse(self, msg):
        self._client.send(json.dumps(msg).encode('utf-8'))

    def closeUpShop(self):
        msg = {
            'from': 'bank',
            'msg': 'closed'
        }
        try:
            self._client.send(json.dumps(msg).encode('utf-8'))
            print('Closed Message Sent.')
            self._client.close()
        except:
            pass

    def run(self):
        while self._isOpen:
            try:
                data = self._client.recv(1024)    # 1024 og
                msg = json.loads(data)
                self._callback(self, msg)
            except socket.error as err:      # error occurs here
                print('Socket Error. Closing the branch client.')
                break
            except Exception as err:
                print(err)
                print('An error occurred. Closing the socket.')
                break

        self._client.close()
        print('Socket closed.')


class Bank(IServerListener):

    def __init__(self, startingMoney):
        super().__init__() # added this
        self._money = startingMoney
        self._isOpen = True  # always starts as open

        self.__mutex = Lock()

        self._branches = []  # no amount of branches
        self._listeners = []  # no amount of listeners
        self._server = TcpServer('127.0.0.1', 8000)  # IP address, port
        self._server.addListener(self)
        self._server.start()

        closingBell = Timer(30.0, self.close)
        closingBell.start()

    def handleBranchMessage(self, branch, msg):
        print('The bank received a branch message!!!!!')
        print(msg)

    def handleNewConnection(self, conn):
        print('New Connection')
        data = {
            'from': 'bank',
            'to': 'client',
            'msg': 'connected'
        }
        conn.sendall(json.dumps(data).encode('utf-8'))

        branchClient = BranchClient(conn, self.handleBranchMessage)
        branchClient.start()
        self._branches.append(branchClient)

    def money(self):
        self.__mutex.acquire()
        money = self._money
        self.__mutex.release()
        return money

    def deposit(self, depositAmnt):
        self._money += depositAmnt

        # Accounting for time to process transaction
        time.sleep(0.1)

        return True

    def withdraw(self, withdrawAmnt):


        if withdrawAmnt < self._money:
            self._money -= withdrawAmnt
            time.sleep(0.1)
            return True
        else:
            print('Withdraw unsuccessful. Amount not enough.')
            return False

    def close(self):
        for branch in self._branches:
            branch.closeUpShop()

    def addListener(self, listener):
        self._listeners.append(listener)


if __name__ == "__main__":
    bank = Bank(0)
