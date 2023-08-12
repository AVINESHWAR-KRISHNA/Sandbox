import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import subprocess
import sys

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = ''
    _svc_display_name_ = ''

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_running = True

    def SvcStop(self):
        """
        Stop the service.
        This function stops the service by reporting its status as "SERVICE_STOP_PENDING",
        setting an event to indicate that the service should stop, and updating the
        `is_running` flag to False.
        """
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False

    def SvcDoRun(self):
        """
        Run the main logic of the service.
        This function is the entry point of the service and is responsible for executing the main logic of the service.
        It calls the `main()` function, which contains the main logic of the service.
        If any exception occurs during the execution of the main logic, it is caught and logged using the `log_error()` function.
        The exception details are also logged using the `traceback.format_exc()` function.
        """
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        try:
            self.main()
        except Exception as e:
            self.log_error(f"Error occurred: {str(e)}")

    def main(self):
        """
        Runs the main function.
        This function executes the main logic of the program. It runs a Python script called 'Pubsub_V1.py' using the `subprocess.run()` method. 
        """
        pubsub_script = ''
        subprocess.run(['python', pubsub_script])

def run_service():
    """
    Run the service.
    This function checks if any command-line arguments are passed to the script. If no arguments are provided, 
    it initializes the service manager, prepares to host a single service (MyService), and starts the service control dispatcher. 
    If arguments are provided, it handles the command line using the win32serviceutil module.
    """
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyService)

if __name__ == '__main__':
    run_service()