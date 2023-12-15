from multiprocessing import Process, Queue, Event

#q = Queue()
process_dict = {}

def add_process(name, process):
    p = Process(target=process)
    process_dict[name] = p
    #q.put(p)

def terminate_process(name):
    process_dict[name].terminate()
    process_dict[name].join()
    print(f'Process: {name} terminated!')

def remove_from_process_dict(name):
    del process_dict[name]