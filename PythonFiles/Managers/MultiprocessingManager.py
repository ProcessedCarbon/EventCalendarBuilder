from multiprocessing import Process, Queue, Event

q = Queue()
processes = []

def add_process(process):
    p = Process(target=process)
    processes.append(p)
    q.put(p)