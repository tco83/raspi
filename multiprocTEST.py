import multiprocessing
import random
import time

def randomswitch(q):
    # Adding a new random to the queue every two seconds
    while True:
        if round(random.random()*100) % 5 == 0:
            q.put((True, time.time()))
            print("SUB: got one")
        time.sleep(0.2)


if __name__ == '__main__':
    print("at least the main was called")
    # Creating a Queue for the two subs to talk to each other
    queue = multiprocessing.Queue()

    # Creating first sub-process to run in background for 4 minutes,
    # creating a new random state every two seconds
    p1 = multiprocessing.Process(target=randomswitch, args=(queue,))
    p1.start()

    while True:
        # Doing it every half second to see the difference
        while not queue.empty():
            newQVal = queue.get()
            print("MAIN: True on %s" % newQVal[1])
            print("MAIN: --- FINISHED ONE LOOP at %f ---" % time.time())
        time.sleep(5)
