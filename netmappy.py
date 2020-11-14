from colorama import Fore, Style            
print(Fore.CYAN + r"@@    @ @$$$$$$$ $$$$$$$ @@    @@     @@     @$$$$$$ @$$$$$$ @     @")
print(Fore.CYAN + r"@ @   @ @           @    @ @  @ @    @  @    @     $ @     $  @   @ ")
print(Fore.CYAN + r"@  @  @ @$$$$       @    @  @@  @   @$$$$@   @$$$$$$ @$$$$$$   @@@  ")
print(Fore.CYAN + r"@   @ @ @           @    @      @  @      @  @       @          @   ")
print(Fore.CYAN + r"@    @@ @$$$$$$$    @    @      @ @        @ @       @          @   ", end = "")
print(Style.RESET_ALL)

from queue import Queue
import socket, threading, sys
from datetime import datetime

t1 = datetime.now()			# starting time counting

# options available
print('=' * 82)
print("What do you want to do?")
print("1. Scan reserved ports")
print("2. Scan all ports")
print("3. Scan according to custom range")
print("4. Scan well-known ports")
print("5. Scan your chosen ports")
try:
	scan_mode = int(input("Choose option accordingly: "))
	if(scan_mode not in [1,2,3,4,5]):
		print("You have not choosen correct option")	# if choosen wrong option, program stops executing
		sys.exit()
except ValueError:
	print("You have not chosen any option")
	sys.exit()				

# defining the target
target = input("Enter your target: ")
if(len(target) == 0):		
	print("You didn't entered target")
	print("Again execute the script and enter target correctly!")
	sys.exit()				# if target is not entered, program stops executing
	
print('-' * 82)
print("Target:", target)	# printing target
print("Starting time:", t1)	# printing starting time of script execution
print('-' * 82)

def port_scan(port):
    try:
    	# create a socket object
    	# AF_INET = ipv4, port, SOCK_STREAM is the socket type for TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
        socket.setdefaulttimeout(1)		# attempt to connect to port, if not connectable, 
										# waits for 1 second to connect, move on
        s.connect((target, port))		# making connection to the target at specified port
        return True	
    
    except:
        return False

queue = Queue()									# initializing empty queue
        
def get_ports(mode):
    # deciding mode of scanning	
    if(mode == 1):
        for port in range(0, 1024):
            queue.put(port)						
    elif(mode == 2):
        for port in range(0, 65536):
            queue.put(port)
    elif(mode == 3):
        custom_range = input("Enter your custom range (seperate by blank): ") #["50", "60"]
        start, end = custom_range.split()
        for port in range(int(start), int(end)):
            queue.put(port)
    elif(mode == 4):
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 169, 443, 445]
        for port in ports:
            queue.put(port)
    elif(mode == 5):
        ports = input("Enter your ports (seperate by blank):")
        ports = ports.split()					# splitting the string containing ports using space delimiter
        ports = list(map(int, ports))			# converting ports from string to int
        for port in ports:
            queue.put(port)						# adding ports to the queue


open_ports = []									# creating a empty open_ports list

def worker():
	while not queue.empty():					# checking queue is empty or not 
		port = queue.get()						# getting ports from the queue
		if port_scan(port):						# checking open ports
		    #print(f"Port {port} is open!")		# printing open port using f-string (format string), works only with Python 3.6+
		    open_ports.append(port)				# adding open ports to list
            
def run_scanner(threads, mode):
    get_ports(mode)								# calling get ports function passing mode number
    thread_list = []							# creating a new empty list for our threads

    for t in range(threads):
        thread = threading.Thread(target=worker)# creating thread and assigning the worker function to threads
        thread_list.append(thread)				# adding threads to the list				

    for thread in thread_list:
        thread.start()							# starting all the threads and letting them scan all the ports

    for thread in thread_list:
        thread.join()							# tell one thread to wait for another thread to finish
    
    open_ports.sort()
    print("PORT    SERVICE")
    #print("Open ports are:", open_ports)		# printing open ports lists
    ports_service = open('my_ports.txt')
    ps = ports_service.readlines()
    for line in ps:	
    	line = line.split()
    	if int(line[1]) in open_ports:
    		print(f"{line[1]}	{line[0]}")
    ports_service.close()
    print('-' * 82)	

run_scanner(500, scan_mode)						# deciding the amount of threads we want to start and scan mode

t2 = datetime.now()								# ending time counting
print(f"Scanning completed in {t2-t1} seconds.")# printing total time required for execution of script
print('=' * 82)
