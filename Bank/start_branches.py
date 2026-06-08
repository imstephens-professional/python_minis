from subprocess import Popen, PIPE
from multiprocessing import Process
import multiprocessing
import run_branch
import time
import subprocess

if __name__ == "__main__":
    # empty list
    processes = []


 #   for i in range(2):
 #       proc = Popen(['python3', 'run_branch.py', str(i)], stderr=PIPE, stdout=PIPE)
 #       time.sleep(1)

  #      processes.append(proc)

    for i in range(2):
        proc = multiprocessing.Process(target=run_branch.Branch, args=(i,))
        processes.append(proc)
        proc.start()

