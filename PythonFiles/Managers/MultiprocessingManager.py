from multiprocessing import Process, Queue, Event

q = Queue()
mgr_processes = {}

def add_process(name, process):
    p = Process(target=process)
    #processes.append(p)
    tmp = {name : p}
    mgr_processes.update(tmp)
    q.put(p)

def terminate_process(name):
    mgr_processes[name].terminate()
    mgr_processes[name].join()
    print(f'Process: {name} terminated!')
    del mgr_processes[name]