from queue import Queue
from threading import Thread, Event
import time
import os

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        
        if 'TP_NUM_OF_THREADS' in os.environ:
            self.num_threads = int(os.environ['TP_NUM_OF_THREADS'])
        else:
            self.num_threads = os.cpu_count()
            
        self.task_queue = Queue()
        self.threads = []
        self.get_ids = []
        
        
    
    def start(self):
        for i in range(self.num_threads):
            thread = TaskRunner(self)
            self.threads.append(thread)
            thread.start()
        
    
    def submit(self, id, task):
        self.task_queue.put((task, id))
        self.get_ids.append(id)
        # with open(f"buna.txt","w") as f:
        #     f.write(str(id))
        
        

class TaskRunner(Thread):
    def __init__(self, tp):
        # self.thread_pool = tp
        super().__init__()
        self.task_queue = tp.task_queue
        
        
    
        
        
    def run(self):
        while True:
            if self.task_queue.empty():
                continue
            else:
                current_task = self.task_queue.get()
                result = current_task[0]()
                with open(f"./results/{current_task[1]}.json","w") as f:
                    f.write(str(result)+'\n')
                    
                
                
                
            
            
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            
