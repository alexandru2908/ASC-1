from queue import Queue
from threading import Thread, Lock
import os

class ThreadPool:
    def __init__(self):
        """
        You must implement a ThreadPool of TaskRunners
        Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        If the env var is defined, that is the number of threads to be used by the thread pool
        Otherwise, you are to use what the hardware concurrency allows
        You are free to write your implementation as you see fit, but
        You must NOT:
          * create more threads than the hardware concurrency allows
          * recreate threads for each task
        """
        if 'TP_NUM_OF_THREADS' in os.environ:
            self.num_threads = int(os.environ['TP_NUM_OF_THREADS'])
        else:
            self.num_threads = os.cpu_count()
        self.task_queue = Queue()
        self.threads = []
        self.get_ids = []
        self.tasks_done = []
        self.is_active = True
        self.my_lock = Lock()
    def start(self):
        """
        Start the thread pool
        """
        for _ in range(self.num_threads):
            thread = TaskRunner(self)
            self.threads.append(thread)
            thread.start()
    def submit(self, id_task, task):
        """
        Submit a task to the thread pool and associate it with an ID
        """
        self.task_queue.put((task, id_task))
        self.get_ids.append(id_task)
class TaskRunner(Thread):
    def __init__(self, tp):
        super().__init__()
        self.task_queue = tp.task_queue
        self.is_alive = tp.is_active
        self.lock = tp.my_lock
        self.tasks_done = tp.tasks_done
    def run(self):
        """
        Get pending job
        Execute the job and save the result to disk
        Repeat until graceful_shutdown
        """
        while True:
            if self.is_alive:
                if self.task_queue.empty():
                    continue
                else:
                    current_task = self.task_queue.get()
                    result = current_task[0]()
                    with open(f"./results/{current_task[1]}.json", "w") as file:
                        file.write(str(result)+'\n')
                    self.lock.acquire()
                    self.tasks_done.append(current_task[1])
                    self.lock.release()
            else:
                if self.task_queue.empty():
                    break
                else:
                    for _ in range(self.task_queue.qsize()):
                        current_task = self.task_queue.get()
                        result = current_task[0]()
                        with open(f"./results/{current_task[1]}.json", "w") as file:
                            file.write(str(result)+'\n')
                        self.lock.acquire()
                        self.tasks_done.append(current_task[1])
                        self.lock.release()
                    break
            