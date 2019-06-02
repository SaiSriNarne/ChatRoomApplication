# -*- coding: utf-8 -*-
"""
Created on Tue Mar  15 08:56:04 2019

@author: Sai Sri Narne
"""

import socket
import os
import tkinter               #The python gui interface for Tk gui extension we 're using
from tkinter import *
import tkinter.filedialog
# or
from tkinter import filedialog
from tkinter import ttk                     #Module providing access to the Tk themed widget set
import threading                #Threading
import base64
from PIL import ImageTk, Image
import emoji


##########################Class Definitions################################

# Every object (representing a gui object..sort of) in the class has a style object associated with it for formatting, styling and beautification
# Entries are objects which appear like text boxes and we can take entries inside them,
# Labels are non modifiable objects that are just used to just mention or label other objects
# Buttons are objects that have a click functionaity which is on an event of a click can call some functions
# .grid functions are used to position the different objects that are created the before objects
#
class Application(tkinter.Tk):
    # Member functions definititons mostly used for GUI and the socket connections and messages are done inside

    def launch_app(self):  # default function always run to generate the main
        self.title('FunChat')  # Name of our Application
        path = "chatapp.png"
        img = ImageTk.PhotoImage(Image.open(path))

        # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        self.panel = Label(self, image=img,background="white")
        self.panel.pack(fill=tkinter.BOTH, expand=True, anchor=CENTER)
        self.frame = Frame(self, background="white")  # A default object frame of the Frame class of the ttk library

        # Initial frame contains two buttons: One for registration and one for Log In
        self.reg_btn = Button(self.frame, text='New user, register here!', command=self.reg_menu,width=25,height=3,foreground="black",background="yellow")
        self.reg_btn.grid(row=2, column=7, padx=200, pady=30)
        self.client_button = Button(self.frame, text='Launch Client', command=self.client_menu,width=25,height=3,foreground="black",background="yellow")
        self.client_button.grid(row=6, column=7, padx=200, pady=30)
        self.try_again_bool = False
        self.try_again_bool2 = False

        # Command that integrates different objects into a single parent object.
        self.frame.pack(fill=tkinter.BOTH, expand=True)

        # mailoop command keeps on running this for some time continuously, else it disappears.
        self.mainloop()

    # The Registration Menu
    def reg_menu(self):
        # Previous menu's buttons destroyed
        if self.try_again_bool2:
            self.try_again2.destroy()
            self.un_error.destroy()
            self.try_again_bool2 = False
        self.client_button.destroy()
        self.reg_btn.destroy()

        # Entries of this frame are host, port name and password and corresponding labels and entries are created
        self.host_entry_label = Label(self.frame, text='Server IP Address', anchor=tkinter.W, justify=tkinter.LEFT,width=25,height=2,foreground="black",background="yellow")
        self.host_entry = ttk.Entry(self.frame,font=0.005,foreground="black")
        self.port_entry_label = Label(self.frame, text='Port Number', anchor=tkinter.W, justify=tkinter.LEFT,width=25,height=2,foreground="black",background="yellow")
        self.port_entry = ttk.Entry(self.frame,font=0.005,foreground="black")
        self.reg_name_label = Label(self.frame, text='Your name', anchor=tkinter.W, justify=tkinter.LEFT,width=25,height=2,foreground="black",background="yellow")
        self.reg_name_entry = ttk.Entry(self.frame,font=0.005,foreground="black")
        self.reg_pwd_label = Label(self.frame, text='Your Password', anchor=tkinter.W, justify=tkinter.LEFT,width=25,height=2,foreground="black",background="yellow")
        self.reg_pwd_entry = ttk.Entry(self.frame, show='*',font=0.005,foreground="black")

        # Register Button
        self.register_btn = Button(self.frame, text='Register', command=self.reg_user, width=25,height=2,foreground="black",background="pink")

        # Forgetting the previous packed Buttons
        self.frame.pack_forget()

        self.title('FunChat registration')

        # Positioning the labels and text boxes appropriately
        self.host_entry_label.grid(row=0, column=0, pady=10, padx=5)
        self.host_entry.grid(row=0, column=1, pady=10, padx=5)
        self.port_entry_label.grid(row=1, column=0, pady=10, padx=5)
        self.port_entry.grid(row=1, column=1, pady=10, padx=5)
        self.reg_name_label.grid(row=2, column=0, pady=10, padx=5)
        self.reg_name_entry.grid(row=2, column=1, pady=10, padx=5)
        self.reg_pwd_label.grid(row=3, column=0, pady=10, padx=5)
        self.reg_pwd_entry.grid(row=3, column=1, pady=10, padx=5)
        self.register_btn.grid(row=5, column=1, pady=10, padx=5)

        self.host_entry.focus_set()  # to decide where the cursor is set

        self.frame.pack(fill=tkinter.BOTH, expand=True)

    # Registering a new user
    def reg_user(self):
        # get function is used to call
        self.host = self.host_entry.get()
        self.port = self.port_entry.get()
        self.port = int(self.port)
        self.username = self.reg_name_entry.get().rstrip()
        self.password = self.reg_pwd_entry.get().rstrip()

        ## delete the objects created in the frame that it was called into
        self.host_entry_label.destroy()
        self.host_entry.destroy()
        self.port_entry_label.destroy()
        self.port_entry.destroy()
        self.reg_name_label.destroy()
        self.reg_name_entry.destroy()
        self.reg_pwd_label.destroy()
        self.reg_pwd_entry.destroy()
        self.register_btn.destroy()
        self.frame.pack_forget()

        # creating socket for client and connecting with it the socket using the host IP and the host port

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.conn.settimeout(4)
        try:
            self.conn.connect((self.host, self.port))  # Connected with the host at port number 'port'
        except:
            self.reg_menu()  # create the previous window again since the connection was not successful

        try:
            self.conn.send((self.username + '/' + self.password).encode())  # Sending username and password for storing in the database
        except:
            self.reg_menu()  # Failing to send the username and password

        conf = self.conn.recv(1024).decode()
        if (conf == "Error"):

            self.un_error = ttk.Label(self.frame, text='Username already used', anchor=tkinter.CENTER,
                                      justify=tkinter.CENTER)
            self.try_again2 = ttk.Button(self.frame, text='Try again', command=self.reg_menu)
            self.un_error.grid(row=0, column=1, pady=10, padx=5)
            self.try_again2.grid(row=1, column=1, pady=10, padx=5)
            self.try_again_bool2 = True
            self.frame.pack(fill=tkinter.BOTH, expand=True)

        else:
            self.client_menu()


    # The Log in menu
    def client_menu(self):
        # Preious buttons destroyed
        self.client_button.destroy()
        self.reg_btn.destroy()
        if self.try_again_bool:
            self.try_again.destroy()
            self.wp_error.destroy()
            self.try_again_bool = False

        self.title('Log In')

        # Entries of this frame are host, port name and password and corresponding labels and entries are created
        self.host_entry_label = Label(self.frame, text='Server IP Address',anchor=tkinter.W, justify=tkinter.LEFT,width=25,height=2,foreground="black",background="yellow")
        self.host_entry = ttk.Entry(self.frame,font=0.005,foreground="black")
        self.port_entry_label = Label(self.frame, text='Port Number', anchor=tkinter.W, justify=tkinter.LEFT,width=25,height=2,foreground="black",background="yellow")
        self.port_entry = ttk.Entry(self.frame,font=0.005,foreground="black")
        self.name_entry_label = Label(self.frame, text='User name', anchor=tkinter.W, justify=tkinter.LEFT,width=25,height=2,foreground="black",background="yellow")
        self.name_entry = ttk.Entry(self.frame,font=0.005,foreground="black")
        self.pwd_entry_label = Label(self.frame, text='Password', anchor=tkinter.W, justify=tkinter.LEFT,width=25,height=2,foreground="black",background="yellow")
        self.pwd_entry = ttk.Entry(self.frame, show='*',font=0.005,foreground="black")

        # Attempt a Log in.
        self.launch_button = Button(self.frame, text='Log In', command=self.launch_client,width=25,height=2,foreground="black",background="yellow")

        # Positioning the labels and text boxes appropriately
        self.host_entry_label.grid(row=0, column=0, pady=10, padx=5)
        self.host_entry.grid(row=0, column=1, pady=10, padx=5)
        self.port_entry_label.grid(row=1, column=0, pady=10, padx=5)
        self.port_entry.grid(row=1, column=1, pady=10, padx=5)
        self.name_entry_label.grid(row=2, column=0, pady=10, padx=5)
        self.name_entry.grid(row=2, column=1, pady=10, padx=5)
        self.pwd_entry_label.grid(row=3, column=0, pady=10, padx=5)
        self.pwd_entry.grid(row=3, column=1, pady=10, padx=5)
        self.launch_button.grid(row=5, column=1, pady=10, padx=5)

        self.host_entry.focus_set()

        self.frame.pack(fill=tkinter.BOTH, expand=True)

    # Connecting to the server
    def launch_client(self):
        # Obtaining the host address and port number
        self.host = self.host_entry.get()
        self.port = self.port_entry.get()
        self.port = int(self.port)
        self.name = self.name_entry.get()
        self.pwd = self.pwd_entry.get()

        # Destroying the previous labels and entries
        self.host_entry_label.destroy()
        self.host_entry.destroy()
        self.port_entry_label.destroy()
        self.port_entry.destroy()
        self.name_entry_label.destroy()
        self.name_entry.destroy()
        self.pwd_entry_label.destroy()
        self.pwd_entry.destroy()

        self.launch_button.destroy()
        self.frame.pack_forget()

        # creating socket for client
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.conn.settimeout(2)
        try:
            self.conn.connect((self.host, self.port))  # Attempting to connect to the server
        except:
            self.client_menu()  # Authentication failure

        self.list_of_active_user = self.initial_setup()  # Obtaining the list of active users on successful connection to the user

        #########################layout details####################
        self.title('OptimumClient ' + self.name)  # Window title

        self.should_quit = False

        self.protocol('WM_DELETE_WINDOW', self.client_quit)  ###?????
        self.chat_frame = Frame(self.frame)  # for the actual display of chat
        self.clients_frame = Frame(self.frame,background="aqua")  # for radio buttons
        self.entry_frame = Frame(self.frame)  # for input text
        self.button_frame = Frame(self.entry_frame,bg="pink")

        # state indicates the chat history so far, and is uneditable
        self.chat_text = tkinter.Text(self.chat_frame, state=tkinter.DISABLED)

        # Adding a scroll bar to the text Area
        self.scroll = tkinter.Scrollbar(self.chat_frame)
        self.scroll.configure(command=self.chat_text.yview)
        self.chat_text.configure(yscrollcommand=self.scroll.set)

        # Chat entry area consists of Send Message, Send Multimedia and Chat entry
        self.chat_entry = ttk.Entry(self.entry_frame)  # Text box for sending messages
        self.send_button = Button(self.button_frame, text='Send Message',fg="blue")  # For actually sending the messages
        self.browsebutton = ttk.Button(self.button_frame, text='Send Multimedia', command=self.browse)


        self.send_button.bind('<Button-1>', self.send)  # press button-1 to send messages
        self.chat_entry.bind('<Return>', self.send)  # Alternate to sending messages, hitting the return button

        # Packing the above created objects and giving them positions while packing
        self.entry_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.frame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        self.clients_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH,expand=True)
        self.chat_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)

        self.chat_entry.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        self.send_button.grid(row=0, column=0)
        self.browsebutton.grid(row=2, column=0)
        self.button_frame.pack(side=tkinter.RIGHT)

        self.checks = []
        self.radio_label = ttk.Label(self.clients_frame,
                                     width=30,
                                     wraplength=125,
                                     anchor=tkinter.W,
                                     justify=tkinter.LEFT,
                                     text='Users Online',background="yellow"
                                     )
        self.disconnect_button=Button(self.clients_frame,text="Disconnect",command=self.client_quit)

        self.radio_label.pack()
        self.scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.chat_text.pack(fill=tkinter.BOTH, expand=True)

        ###### Emoticon function code section
        # Four buttons, using global variables for easy creation and destruction

        b1 = ''
        b2 = ''
        b3 = ''
        b4 = ''
        # Open the image and save it in the variable
        p1 = tkinter.PhotoImage(file='./emoticons/angry.png')
        p2 = tkinter.PhotoImage(file='./emoticons/cunning.png')
        p3 = tkinter.PhotoImage(file='./emoticons/laugh.png')
        p4 = tkinter.PhotoImage(file='./emoticons/sad.png')
        # Use a dictionary to match the mark with the expression picture one by one, for receiving the mark later to determine the expression map
        self.dic = {'aa**': p1, 'bb**': p2, 'cc**': p3, 'dd**': p4}
        ee = 0  # Judging the sign of the expression panel switch
        chat = '----------group chat----------'  # Chat object, default is group chat
        # a function that sends an emoticon tag, called in a button click event
        def mark(exp):  # The parameter is the emoticon tag sent, and the button is destroyed after being sent.
            global ee
            data = ""
            for client in self.list_of_active_user:
                if self.enable[client].get() == 1:
                    data = data + "@" + client + ' '
            data = data + ':'
            data = data + exp

            self.conn.send(data.encode())  # Sending the encoded data to the server
            ee = 0

        # Four corresponding functions
        def bb1():
            mark('aa**')

        def bb2():
            mark('bb**')

        def bb3():
            mark('cc**')

        def bb4():
            mark('dd**')

        def express():
            global b1, b2, b3, b4, ee
            ee=0
            if ee == 0:
                ee = 1
                b1 = Button(self, command=bb1, image=p1,
                                    relief=tkinter.FLAT)
                b2 = Button(self, command=bb2, image=p2,
                                    relief=tkinter.FLAT, bd=0)
                b3 = Button(self, command=bb3, image=p3,
                                    relief=tkinter.FLAT, bd=0)
                b4 = Button(self, command=bb4, image=p4,
                                    relief=tkinter.FLAT, bd=0)

                b1.place(x=405, y=550)
                b2.place(x=490, y=550)
                b3.place(x=570, y=550)
                b4.place(x=640, y=550)
            else:
                ee = 0
                b1.destroy()
                b2.destroy()
                b3.destroy()
                b4.destroy()

        # Create an emoticon button
        self.eBut = Button(self.button_frame, text='emoji', command=express)
        self.eBut.grid(row=1,column=0)

        #############################################################

        self.enable = dict()

        for client in self.list_of_active_user:
            self.enable[client] = tkinter.IntVar()
            l = ttk.Checkbutton(self.clients_frame, text=client, variable=self.enable[client])
            l.pack(anchor=tkinter.W)
            self.checks.append(l)

        self.chat_entry.focus_set()

        # for client we will intiate a thread to display chat
        self.clientchat_thread = threading.Thread(name='clientchat', target=self.clientchat)
        self.clientchat_thread.start()
        self.disconnect_button.pack()
        self.button_frame.pack(side=tkinter.RIGHT)



    def browse(self):
        # To browse a file to exchange with client
        self.mmfilename = filedialog.askopenfilename()
        self.multimedia_send()

    # Sending the message according to the format specified in server.py and updating the chat history area
    def send(self, event):
        message = self.chat_entry.get()
        # dest = self.dest.get()

        data = ""
        for client in self.list_of_active_user:
            if self.enable[client].get() == 1:
                data = data + "@" + client + ' '
        data = data + ':'
        data = data + message

        self.chat_entry.delete(0, tkinter.END)  # input box empty after send

        self.conn.send(data.encode())  # Sending the encoded data to the server

        self.chat_text.config(state=tkinter.NORMAL)
        for client in self.list_of_active_user:
            if self.enable[client].get() == 1:
                self.chat_text.insert(tkinter.END, client + ':' + message + '\n', ('tag{0}'.format(1)))
                self.chat_text.tag_config('tag{0}'.format(1), justify=tkinter.RIGHT, foreground='blue')
        self.chat_text.config(
            state=tkinter.DISABLED)  # Again Disabling the edit functionality so that the user cannot edit it
        self.chat_text.see(tkinter.END)  # Enables the user to see the edited chat history

    def multimedia_send(self):
        # Sends file to a client
        filename = self.mmfilename
        with open(filename, "rb") as file:
            encoded_string = base64.b64encode(file.read())
        data = "^"
        for client in self.list_of_active_user:
            if self.enable[client].get() == 1:
                data = data + "@" + client + ' '
        data = data + ':'
        data = data + filename + ':'
        data_to_send = data + encoded_string.decode()

        # data_to_display = '^@'+dest+':'+ filename
        # data_to_send = data_to_display + ':' + encoded_string

        self.chat_entry.delete(0, tkinter.END)  # input box empty after send
        self.conn.send(data_to_send.encode())

        self.chat_text.config(state=tkinter.NORMAL)
        for client in self.list_of_active_user:
            if self.enable[client].get() == 1:
                self.chat_text.insert(tkinter.END, client + ':' + filename + '\n', ('tag{0}'.format(1)))
                self.chat_text.tag_config('tag{0}'.format(1), justify=tkinter.RIGHT, foreground='blue')
        self.chat_text.config(
            state=tkinter.DISABLED)  # Again Disabling the edit functionality so that the user cannot edit it
        self.chat_text.see(tkinter.END)  # Enables the user to see the edited chat history

    # Chatting time!
    def clientchat(self):
        while not self.should_quit:  # If we are not in the 'quit' state then do :
            try:
                data = self.conn.recv(10000000)  # Receive and decode the data
                data = data.decode()
                data = data.rstrip()

                if len(data):  # If there is data
                    # if there is an active user message received then it means a new
                    # user has logged in and we need to update radios
                    if data[0] == "!":
                        self.list_of_active_user = data[1:].split(' ')

                        for l in self.checks:
                            l.destroy()

                        # Updating the new checkbox list
                        for client in self.list_of_active_user:
                            self.enable[client] = tkinter.IntVar()
                            l = ttk.Checkbutton(self.clients_frame, text=client, variable=self.enable[client])
                            l.pack(anchor=tkinter.W)
                            self.checks.append(l)

                    elif data[0] == "^":
                        data_recvd = data.split(':')
                        sendername = data_recvd[0][2:]
                        filename_process = data_recvd[1].split('/')
                        filename = filename_process[len(filename_process) - 1]
                        head, filename = os.path.split(data_recvd[2])
                        filename = os.getcwd() + '\\' + filename
                        print(sendername)
                        print('\n')
                        print(filename)
                        encoded_string = data_recvd[3]
                        decoded_string = base64.b64decode(encoded_string)

                        with open(filename, "wb") as file:
                            file.write(decoded_string)

                        print_data = sendername + ': ' + filename
                        self.chat_text.config(state=tkinter.NORMAL)
                        self.chat_text.insert(tkinter.END, print_data + '\n', ('tag{0}'.format(2)))
                        self.chat_text.tag_config('tag{0}'.format(2), justify=tkinter.LEFT, foreground="blue")
                        self.chat_text.config(state=tkinter.DISABLED)
                        self.chat_text.see(tkinter.END)
                    # it's not an activelist msg
                    else:
                        # Updating the chat history based on the new message received
                        self.chat_text.config(state=tkinter.NORMAL)
                        markk = data[1:].split(':')[1]
                        u1=data[1:].split(':')[0]
                        if markk in self.dic:
                            self.chat_text.insert(tkinter.END, u1 + ':', ('tag{0}'.format(2)))
                            self.chat_text.image_create(tkinter.END, image=self.dic[markk])
                            self.chat_text.insert(tkinter.END, '\n', ('tag{0}'.format(2)))
                            self.chat_text.tag_config('tag{0}'.format(2), justify=tkinter.LEFT, foreground='red')
                            self.chat_text.config(state=tkinter.DISABLED)
                            self.chat_text.see(tkinter.END)

                        else:
                            self.chat_text.insert(tkinter.END, data[1:] + '\n', ('tag{0}'.format(2)))
                            self.chat_text.tag_config('tag{0}'.format(2), justify=tkinter.LEFT, foreground='red')
                            self.chat_text.config(state=tkinter.DISABLED)
                            self.chat_text.see(tkinter.END)
                else:
                    break
            except:
                continue

    def initial_setup(self):
        # allow for it to communicate with server only once for
        # the first time  till it gets the list of active users
        got_list = False
        list_of_active_user = []

        try:
            self.conn.send('0'.encode())  # Sending 0 to indicate that it is a non-registration message
        except:
            # Closing the connection and giving an option to reattempt
            self.conn.close()
            self.wp_error = ttk.Label(self.frame, text='Cannot Connect to Server', anchor=tkinter.CENTER,
                                      justify=tkinter.CENTER)
            self.try_again = ttk.Button(self.frame, text='Try again', command=self.client_menu)
            self.wp_error.grid(row=0, column=1, pady=10, padx=5)
            self.try_again.grid(row=0, column=1, pady=10, padx=5)
            self.frame.pack(fill=tkinter.BOTH, expand=True)

        while 1:
            if not got_list:
                try:
                    data = self.conn.recv(10000000)  # Obtaining the list of all the active users
                    data = data.decode()
                    data = data.rstrip()
                except:
                    self.conn.close()
                    self.client_menu()

                if data == "What is your name?":  # Getting the first message from the server
                    try:
                        self.conn.send(
                            (self.name + '/' + self.pwd).encode())  # Sending the name and password to the server
                    except:
                        self.conn.close()
                        self.client_menu()
                    try:
                        list_of_active_user = self.conn.recv(
                            10000000).decode()  # this will be a string of name separated by spaces
                    except:
                        self.conn.close()
                        self.client_menu()
                    if list_of_active_user == 'authentication_error':
                        # Authentication error implies that user is either not registered or password is incorrect. Redirecting to the Client menu
                        self.wp_error = ttk.Label(self.frame, text='Authentication_Error', anchor=tkinter.CENTER,
                                                  justify=tkinter.CENTER)
                        self.try_again = ttk.Button(self.frame, text='Try again', command=self.client_menu)
                        self.wp_error.grid(row=0, column=1, pady=10, padx=5)
                        self.try_again.grid(row=1, column=1, pady=10, padx=5)
                        self.try_again_bool = True
                        self.frame.pack(fill=tkinter.BOTH, expand=True)

                    list_of_active_user = list_of_active_user[1:].split(
                        ' ')  # now it has all the names separately, its not a string
                    got_list = True
            else:
                return list_of_active_user

    # Closing down the thread and shutting down the connection
    def client_quit(self):
        self.should_quit = True
        self.conn.shutdown(socket.SHUT_WR)
        self.clientchat_thread.join()
        self.conn.close()
        self.destroy()


# main function
if __name__ == '__main__':
    app = Application()

app.launch_app()  # Launching the app
