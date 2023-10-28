from multiprocessing import Process, Queue, Event

q = Queue()
processes = []

process_events = {
    'outlook_auth_event' : Event()
}

def add_process(process):
    p = Process(target=process)
    processes.append(p)
    q.put(p)
