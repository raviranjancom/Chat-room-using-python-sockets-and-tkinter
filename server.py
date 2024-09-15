
#importing modules
import socket
import threading

HOST="127.0.0.1"
PORT=6000
MAX_USER = 10
online_c = [] # array of active c-object  tuple (user , c-object)   V-1
#function to send messages to all clients

#function to listen for upcomming messages from c-object

def recv_tokan(c,user):
    while True:
        response = c.recv(500).decode('utf-8')  # reciveing message from users
        if(response!=''):
            final_response = user + ' # ' + response
            echo_all(final_response)
        else:
            print("Message is empty")


# tokan to single user
def echo_to(c,final_response):
    print()
    c.sendall(final_response.encode())      # utf is default for encode()

# sends message to all
def echo_all(final_response):
    for i in online_c:
        echo_to(i[1],final_response)


#function to handle client 
def handler(c):

    #adding user name to online list
    while True:
        user = c.recv(500).decode('utf-8')  #reciving user name
        if(user!=''):
            online_c.append((user,c))       # V-1
            prompt = "[SERVER]"+ " # " + f"{user} added to chat"
            echo_all(prompt)
            break       # exiting the infinite loop
        else:
            print("username is empty")

    threading.Thread(target= recv_tokan,args=(c, user,)).start()        # starting to listen for client message

def main():
    #sockets(IPV4 , TCP)
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        s.bind((HOST,PORT))         #configure the host and port

    except:
        print(f"Error ! HOST = {HOST} PORT ={PORT}")
    
    s.listen(MAX_USER)

    while True:
        c,addr=s.accept()   # address = tuple (HOST  , PORT) of client socket object
        print("CONNECTED to client")

        threading.Thread(target=handler,args=(c, )).start()     #handling client function call
    
if(__name__=="__main__"):
    main()

