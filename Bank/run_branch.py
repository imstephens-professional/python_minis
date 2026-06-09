# Author Names: Isabella Stephens, Sosan Wahid, Andrew Kivrak
# Created: November 2022
# Updated: November 2022

import sys
import socket
import json
from threading import Thread, Timer
from random import random, choice
import time
from datetime import datetime
from multiprocessing import Process

from TcpServer import BranchTcpClient, IClientListener


class Branch(IClientListener):

    def __init__(self, branch_id):
        self._branchId = branch_id
        self._client = BranchTcpClient('127.0.0.1', 8000, 2.0)
        self._client.addListener(self)
        self._client.start()

    def start(self):
        self._client.start()

    def sendMoneyRequest(self):

        data = {
            'from': self._branchId,
        }

        isWithdraw = choice([0, 1])
        if isWithdraw:
            data['msg'] = 'withdraw'
        else:
            data['msg'] = 'deposit'

        data['amount'] = random() * 100

        self._client.send(json.dumps(data).encode('utf-8'))
        print('Branch {} sending a money request.'.format(self._branchId))
        print(data)

    def handleConnected(self):
        print('Branch {} is connected'.format(self._branchId))
        data = {
            'from': self._branchId,
            'msg': 'acknowledge connection'
        }
        self._client.send(json.dumps(data).encode('utf-8'))
        print('sent response')

    def handleTcpMessage(self):
        print('Branch {} got a new message!'.format(self._branchId))

    def handleSocketClosed(self):
        print('Branch {} is now closed due to a socket error.'.format(self._branchId))

    def handleClosedMessage(self):
        print('Bank closed. Branch Closed.')

    def handleTimeout(self):
        self.sendMoneyRequest() # THE ERROR IS HERE


if __name__ == "__main__":
    print('Starting branch..')
    branchId = int(sys.argv[1])
    #branchId = [1]
    branch = Branch(branchId)
