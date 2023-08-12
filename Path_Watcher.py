
import time
import os
import subprocess
import multiprocessing
from functools import partial
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor

def Main(FileProcess, event_queue):

    class EventHandler(FileSystemEventHandler):
        def on_created(self, event):
            event_queue.put(event)
            # FileProcess(os.path.basename(event.src_path))
            
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    while True:
        try:
            with ThreadPoolExecutor(max_workers=50) as executor:
                while True:
                    '''
                    Get the next file from the queue.
                    '''
                    event = event_queue.get()
                    # print(event.src_path)
                    executor.submit(FileProcess, os.path.basename(event.src_path))
            time.sleep(1)

        except KeyboardInterrupt:
            observer.stop()
        observer.join()

def FileProcess(__parm):

    print("File detected :: ", __parm ,"\nRunning batch file...\n")

    ''' 
     The subprocess module allows you to run commands in a non-blocking way,
     so that the process can continue to watch the directory for new files
    '''
    
    try:
        BatchProcess = subprocess.Popen(["Sample_batfile.bat"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = BatchProcess.communicate()

        if BatchProcess.returncode != 0:
            print(f"There was some error while running the batch file :: {stderr.decode()} ")
        else:
            print("Batch file completed.") #{stdout.decode()}
    except Exception as err:
        print(err)


path = ""

if __name__ == '__main__':
    ''' 
    multiprocessing.Queue() is a multi-producer, multi-consumer queue.
    that is thread-safe and can be used to pass data between processes.
    '''
    event_queue = multiprocessing.Queue()
    watch_process = multiprocessing.Process(target=Main, args=(partial(FileProcess), event_queue))
    watch_process.start()
    watch_process.join()
