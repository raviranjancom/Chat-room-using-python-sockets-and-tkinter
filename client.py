import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox


HOST="127.0.0.1"
PORT=6000

AQUA = "#00FFFF"
CHARTREUSE1 = "#7FFF00"
CHARTREUSE2 = "#76EE00"
CHARTREUSE3 = "#66CD00"
ORCHID2 = "#EE7AE9"
LIMEGREEN = "#32CD32"
YELLOW = "#FFFF00"
WHITE = "white"
GRAY ="#1F1F1F"
BLACK = "black"
BLUE="blue"
FONT = ("Helvetia", 17)
BUTTON_FONT = ("Helvetia",14)

c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def add_message(message):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, message + '\n')
    chat_box.config(state=tk.DISABLED)
    
def connect():
    try:
        c.connect((HOST,PORT))              # V-1
        print("connected to server")
        add_message("[SERVER] Successfully connected to server")
    except:
        messagebox.showerror("Unable to connect HOST = {HOST} PORT = {PORT}")
        exit(0)

    
    user = text_box.get()
    if(user!=''):
        c.sendall(user.encode())
    else:
        messagebox.showerror("Username is empty")
        exit(0)

    threading.Thread(target=scan_from_server,args=(c, )).start()

    #text_box.config(state=tk.DISABLED)
    #user_button.config(state=tk.DISABLED)

def send_message():
    response = tokan_box.get()
    if(response!=''):
        c.sendall(response.encode())
        #chat_box.delete(0,len(response))
    else:
        messagebox.showerror("Empty message!!!")
        exit(0)

obj=tk.Tk()        # tkinter window
obj.geometry("600x600")
obj.title("CHAT ROOM")
#obj.resizeable(False, False)
obj.grid_rowconfigure(0, weight=1)
obj.grid_rowconfigure(1,weight=4)
obj.grid_rowconfigure(2,weight=1)

# creating frames
top=tk.Frame(obj,width=600,height=100,bg=CHARTREUSE1)
#definging the position of top frame
top.grid(row=0, column=0,sticky=tk.NSEW)

middle=tk.Frame(obj,width=600,height=400,bg=AQUA)
middle.grid(rows=1,column=0,sticky=tk.NSEW)

bottom=tk.Frame(obj,width=600,height=100,bg=CHARTREUSE3)
bottom.grid(row=2,column=0,sticky=tk.NSEW)

text_label = tk.Label(top,text="ENTER USERNAME :",font= FONT,bg= BLACK,fg= AQUA)
text_label.pack(side=tk.LEFT, padx=8)        #(side for label , spaceing from that side)

text_box = tk.Entry(top, font=FONT,bg=WHITE,fg=BLACK,width=20)
text_box.pack(side=tk.LEFT, padx=8)

user_button = tk.Button(top,text="JOIN",font=FONT, bg=BLUE,fg=AQUA,command=connect)
user_button.pack(side=tk.LEFT,padx=8)

tokan_label=tk.Label(bottom,text="ENTER MESSAGE : ",font=FONT,bg=BLACK,fg=AQUA)
tokan_label.pack(side=tk.LEFT,padx=8)

tokan_box =tk.Entry(bottom,font=FONT,bg=WHITE,fg=BLACK,width=20)
tokan_box.pack(side=tk.LEFT, padx=8)

tokan_button =tk.Button(bottom,text="SEND",font=FONT,bg=BLUE,fg=AQUA,command=send_message)
tokan_button.pack(side=tk.LEFT,padx=8)

chat_box = scrolledtext.ScrolledText(middle,font=BUTTON_FONT,bg=BLACK,fg=WHITE,width=65,height=25)
chat_box.config(state=tk.DISABLED)          # To disable the text input at update box
chat_box.pack(side=tk.LEFT,padx=8)



#listen for message from user
def scan_from_server(c):
    while True:
        response=c.recv(500).decode('utf-8')
        if response!='':
            user = response.split(" # ")[0]
            tokan =response.split(" # ")[1]

            add_message(f"[{user}]    {tokan}")
        else:
            messagebox.showerror("Message is empty")

def main():

    obj.mainloop()     # rendering updated window every time to display

if(__name__=="__main__"):
    main()


#threading is used to send message 
