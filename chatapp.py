from tkinter import *
import threading,socket
import os
import re
from tkinter import messagebox

regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

root=Tk()
root.wm_geometry("950x600+100+100")
line=0
receiver=""
name=""
ipaddress=""
add_contacts_size=80
all_contacts=["Group",]

#on closing function
def on_closing():
        global client
        try:
            client.close()       
        except:
            pass
        root.destroy()
        os._exit(0)		
root.protocol("WM_DELETE_WINDOW", on_closing)
        

def to_connect():
    global client,name,ipaddress
    name=User_name_entry.get()
    ipaddress=ip_entry.get()
    # ipaddress="localhost"

    if name=="" or name==" " or ipaddress=="":
        return None
    client=socket.socket()
    client.connect((ipaddress,5555))
    client.sendall(name.encode("ascii"))

    common()
    print("Request sent to server for the connection..")


def common():
    global name,ipaddress
    User_name_entry.destroy()
    user_name_submit.destroy()
    ip_entry.destroy()
    User=Label(Nameframe,text=name)
    User.place(x=80,y=5)
    ip_address_label=Label(Nameframe,text=ipaddress)
    ip_address_label.place(x=60,y=36)
    t2=threading.Thread(target=receive,args=(client,))
    t2.start()
    return

def to_start_thread():
    global regex
    name=User_name_entry.get()
    ipaddress=ip_entry.get()
    if name=="" or name==" " or ipaddress=="" or ipaddress==" ":
        return None
    if(re.search(regex, ipaddress)):
        print("Valid Ip address")
    else:
        messagebox.showerror("Error","Please enter a valid ipaddress")
        return
    t3=threading.Thread(target=to_connect)
    t3.start()


#function to send
def send():
    global line,client,receiver
    textarea_text=input_text.get(1.0,"end-1c")
    if receiver=="":
        input_text.delete(1.0, END)
        return None
    text_sms=receiver+"+--"+textarea_text
    Label(myframe,text=textarea_text,anchor="e",width=85).grid(row=line,column=0)
    print("sent :"+text_sms)
    client.sendall(text_sms.encode("ascii"))
    line=line+1
    input_text.delete(1.0, END)

def receive(client):
    while True:
        global all_contacts,line,receiver
        try:
            textarea_text=client.recv(1024).decode("ascii")
            if textarea_text=="":
                continue
            print("received :"+textarea_text)
            
            textarea_text=textarea_text.split("+--")
            print("The receiver is ",textarea_text[0])
            if textarea_text[0] in all_contacts:
                if textarea_text[0]==receiver:
                    Label(myframe,text=textarea_text[1],anchor="w",width=85).grid(row=line,column=0)
                    line=line+1
            else:
                add_contacts2(textarea_text[0])
  
        except Exception as e:
            print("The exceptions is :",e)
            client.close()
            break

#command to change the value of the receiver
def to_change_receiver(event):
    global receiver,line
    a=receiver
    for i in listbox.curselection():
        print("selected_user is "+listbox.get(i))
        receiver=listbox.get(i)
        print(all_contacts)
    if a!=receiver:
        for widget in myframe.winfo_children():
            widget.destroy()

def add_contacts2(name1):
    global add_contacts_size,all_contacts,name
    if name1=="" or name1==name:
        return
    all_contacts.append(name1)    
    # Button(contactsframe,text=name1,font=5,height=1,width=27,command=lambda:to_change_receiver(f"{name1}")).place(x=0,y=add_contacts_size)
    listbox.insert(END,name1)
    # add_contacts_size+=40


#adding contacts
def add_contacts():
    global add_contacts_size,all_contacts
    name1=User_name_entry1.get()
    if name1=="" or name1==name:
        return
    if name1 not in all_contacts:
        all_contacts.append(name1)
    else:
        return
    # Button(add_contactsframe,text=name1,font=5,height=1,width=27,command=lambda:to_change_receiver(f"{name1}")).place(x=0,y=add_contacts_size)
    listbox.insert(END,name1)
    # add_contacts_size+=40
    print(name1," added")
    User_name_entry1.delete(0,END)

#scrollable frame

wrapper1=LabelFrame(root)

mycanvas=Canvas(wrapper1,relief=GROOVE,width=600,height=540,bd=2)

mycanvas.pack(side=LEFT,fill="both",expand="yes")

yscrollbar=Scrollbar(wrapper1,orient="vertical",command=mycanvas.yview)

yscrollbar.pack(side=RIGHT,fill="y")

mycanvas.config(yscrollcommand=yscrollbar.set)

mycanvas.bind('<Configure>',lambda e:mycanvas.configure(scrollregion=mycanvas.bbox('all')))

myframe=Frame(mycanvas)

mycanvas.create_window((0,0),window=myframe,anchor="nw")

wrapper1.place(x=320,y=0)




#frame of the name label or username
Nameframe=Frame(root,relief=GROOVE,width=320,height=70,bd=5)
Nameframe.place(x=0,y=0)

#label of the name 
user_name=Label(Nameframe,text="Username :")
user_name.place(x=0,y=5)

#user name entry
User_name_entry=Entry(Nameframe,width=37,background="red")
User_name_entry.place(x=80,y=5)

#ipaddrss entry
ip_label=Label(Nameframe,text="IP addr :")
ip_label.place(x=0,y=35)
#Button to submit username
user_name_submit=Button(Nameframe,text="submit",command=to_start_thread)
user_name_submit.place(x=250,y=30)

ip_entry=Entry(Nameframe,width=30,background="red")
ip_entry.place(x=50,y=37)

#add contacts frame
add_contactsframe=Frame(root,relief=GROOVE,width=320,height=50,bd=5)
add_contactsframe.place(x=0,y=70)

# frame of the contacts
contacts_frame=Frame(root,relief=GROOVE,width=320,height=200,bd=5)
contacts_frame.place(x=2,y=115)

#listbox 
listbox=Listbox(contacts_frame,border=2,font=5,height=20,width=26)
listbox.pack(side=LEFT,fill=BOTH)
scroll=Scrollbar(contacts_frame)
scroll.pack(side=RIGHT,fill=BOTH)
listbox.bind('<<ListboxSelect>>',to_change_receiver)

listbox.config(yscrollcommand=scroll.set)
scroll.config(command=listbox.yview)

listbox.insert(END,"Group")

User_name_entry1=Entry(add_contactsframe,width=30,background="red")
User_name_entry1.place(x=5,y=6)

Button(add_contactsframe,text="Add Contacts",width=11,height=1,command=add_contacts).place(x=210,y=2)

#send section
sendframe=Frame(root,relief=GROOVE,width=630,height=50,bd=5)
sendframe.place(x=320,y=550)

#textarea to input text to send
input_text=Text(sendframe,height=2,width=63)
input_text.place(x=0,y=1)

#send button to send the message
send_button=Button(sendframe,text="send",height=2,width=14,background="red",command=send)
send_button.place(x=513,y=1)


root.mainloop()