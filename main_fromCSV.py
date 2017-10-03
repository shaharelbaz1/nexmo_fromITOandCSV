# -*- coding: utf-8 -*-
from Tkinter import *
import Tkinter as tk
import ttk
import csv
import IP_in_out
import organizationFile
import sys
import sendSMS
from tkFileDialog import askopenfilename, askdirectory
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def uplodeFile():
    global file, b_file
    filesName = askopenfilename()
    file_path = filesName
    if (file_path == ""):
        sys.exit(0)
    file = filesName
    b_file.config(text=file, width=40)
    T.insert(END,'file upload\n')

def selectAll(checkButtons):
    global x
    if x.get() == 1:
        for check in checkButtons:
            check.select()
    else:
        for check in checkButtons:
            check.deselect()
    countSelection()


def countSelection():
    global b_selectAll, count1, L_canvSelection
    i = 0
    count1 = 0
    count2 = len(users)
    for user in users:
            if arr[i].get() != 1:
                b_selectAll.deselect()
            if arr[i].get() == 1:
                count1 = count1 + 1
            i = i + 1
    if count1 == count2:
        b_selectAll.select()

    L_canvSelection.config(text="select %s/%s" % (count1, count2))

def orgLink(name):
    if name=='': return organizationFile.default
    if name == 'Hot': return organizationFile.Hot
    if name=='InstantTalk': return organizationFile.InstantTalk
    if name=='Claro': return organizationFile.Claro
    if name=='Instacom': return organizationFile.Instacom
    if name=='MTN': return organizationFile.MTN
    if name=='NexusTalk': return organizationFile.NexusTalk
    if name=='Redline': return organizationFile.Redline
    if name=='Teamvix': return organizationFile.Teamvix
    if name=='Telcel': return organizationFile.Telcel
    if name == 'Telus': return organizationFile.Telus
    if name == 'Vodacom': return organizationFile.Vodacom

def sendDetails():
    i=0
    j=0
    for user in users:
        if arr[i].get() == 1:
            PhoneNumber = user[0]
            userNameSIP = user[1]

            password = user[2]

            #IPserver=IP_in_out.options(user[3])
            IPserver = user[3]

            #TWOmsg = "Download from here: "  + org #+ "*userName: " + name1 + "\npassword: " + password + "\nserver:" +IPserver+ " "
            msg = 'getwml.aspx?uname=' + userNameSIP + '&pass=' + password + '&server=' +IPserver
            #msg2 = userName.decode('UTF-8') + userNameSIP + "\n"+passw.decode('UTF-8') + password + "\n"+server.decode('UTF-8') + IPserver + "\n end"
            sendSMS.send(api_key, api_secret, PhoneNumber, msg)
            #sendSMS.send(api_key, api_secret, PhoneNumber, TWOmsg)

            L_canvSend.config(text="send %s/%s" % (j + 1, count1))
            L_canvSend.update_idletasks()
            j = j + 1

        i=i+1

def sendLink():
    i=0
    j=0
    for user in users:
        if arr[i].get() == 1:
            PhoneNumber = user[0]
            org = orgLink(list.get())
            #IPserver=IP_in_out.options(getServers_id_ip(user))

            msg = "Download from here: "  + org
            sendSMS.send(api_key, api_secret, PhoneNumber, msg)

            L_canvSend.config(text = "send %s/%s" % (j+1, count1))
            L_canvSend.update_idletasks()
            j=j+1

        i=i+1

def sendBoth():
    i = 0
    j = 0
    for user in users:
        if arr[i].get() == 1:
            PhoneNumber = user[0]
            userNameSIP = user[1]

            password = user[2]

            #IPserver = IP_in_out.options(user[3])
            IPserver = user[3]
            org = orgLink(list.get())
            # IPserver=IP_in_out.options(getServers_id_ip(user))

            msg1 = "Download from here: " + org

            # TWOmsg = "Download from here: "  + org #+ "*userName: " + name1 + "\npassword: " + password + "\nserver:" +IPserver+ " "
            msg2 = 'getwml.aspx?uname=' + userNameSIP + '&pass=' + password + '&server=' + IPserver
            # msg2 = userName.decode('UTF-8') + userNameSIP + "\n"+passw.decode('UTF-8') + password + "\n"+server.decode('UTF-8') + IPserver + "\n end"
            sendSMS.send(api_key, api_secret, PhoneNumber, msg1)
            sendSMS.send(api_key, api_secret, PhoneNumber, msg2)
            # sendSMS.send(api_key, api_secret, PhoneNumber, TWOmsg)

            L_canvSend.config(text="send %s/%s" % (j + 1, count1))
            L_canvSend.update_idletasks()
            j = j + 1

        i = i + 1

class openNewWindow(tk.Toplevel):

    def __init__(self, parent):
        global arr, b_selectAll, x
        global users
        global L_canvSend, count1, L_canvSelection
        T.insert(END, "Please wait...\n")
        T.update_idletasks()

        progress['value'] = 20
        root_CSV.update_idletasks()
        arr = {}
        init()
        tk.Toplevel.__init__(self, parent)

        self.title('choose users')
        self.iconbitmap((resource_path("images\mobiletornado_icon.ico")))
        self.geometry('400x600')

        vscrollbar = tk.Scrollbar(self)

        c = tk.Canvas(self, background="gray94",width=100,height=50, yscrollcommand=vscrollbar.set,scrollregion=(0, 0, 100, 100))

        vscrollbar.config(command=c.yview)
        vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        c.bind_all('<MouseWheel>', lambda event: c.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        c.bind_all('<Next>',  lambda event: c.yview_scroll(4, 'units'));
        c.bind_all('<Prior>',  lambda event: c.yview_scroll(-4, 'units'));

        f = tk.Frame(c)  # Create the frame which will hold the widgets

        c.pack(side="left", fill="both", expand=True)

        c.create_window(0, 0, window=f, anchor='nw')

        wait = c.create_text(120, 90, anchor='nw', text="Please wait..." ,font = "Helvetica 12 bold italic")

        progress['value'] = 50
        root_CSV.update_idletasks()
        c.delete(wait)

        checkButtons = []
        x = tk.IntVar()
        b_selectAll = tk.Checkbutton(self, text='select all', variable=x, font="Helvetica 10 bold italic",
                                     command=lambda arr=checkButtons: selectAll(checkButtons))
        b_selectAll.pack(side="top", anchor="w")

        L_canvSelection = Label(self, bg="gray94", text="", font = "Helvetica 10 bold italic")
        L_canvSelection.pack(side="top",expand=True, anchor="w")

        L_canvSend = Label(self, bg="gray94", text="", font="Helvetica 10 bold italic")
        L_canvSend.pack(side="bottom", expand=True, anchor="w")


        try:
            with open(file, 'r') as fe:
                reader = csv.reader(fe)
                users = []
                i=0
                for row in reader:
                    if "Mobile" in row[2]:
                        arr[i] = tk.IntVar()
                        displayName = row[0]
                        check = tk.Checkbutton(f, text=displayName, variable=arr[i],command=lambda arr=users: countSelection())
                        check.pack(side="top", anchor="w")
                        checkButtons.append(check)
                        user=[]

                        prefix = row[4]
                        number = row[5]
                        user.append(prefix + number)

                        username = row[6]
                        user.append(username)
                        password = row[1]
                        user.append(password)
                        server = row[16]
                        user.append(server)

                        users.append(user)
                        i=i+1

                b_sendLink = Button(self, text='send SMS\nwith download link', height=3, width=15, bg="turquoise",
                                    command=sendLink)
                b_sendLink.pack(side="top", padx=0, pady=0, fill="none",anchor= "w", expand=True)

                b_sendDetails = Button(self, text='send SMS\nwith user details', height=3, width=15, bg="turquoise",
                                       command=sendDetails)
                b_sendDetails.pack(side="top", padx=0, pady=0, fill="none",anchor= "w", expand=True)

                b_both = Button(self, text='send Both', height=3, width=15, bg="turquoise",
                                command=sendBoth)
                b_both.pack(side="top", padx=0, pady=0, fill="none", anchor="w", expand=True)

                b_exit = Button(self, text='Quit', height=3, width=15, bg="turquoise", command=lambda:self.destroy())
                b_exit.pack(side="top", padx=0, pady=0, fill="none",anchor= "w", expand=True)


                self.update()
                c.config(scrollregion=c.bbox("all"))

        except:
            c.create_text(20, 90, anchor='nw', text='Error with CSV', font = "Helvetica 10 bold italic")
        progress['value'] = 100


def init():
    global api_key, api_secret
    api_key =ents[0][1].get()
    api_secret = ents[1][1].get()

fields = 'api_key', 'api_secret'

def makeform(root, fields):
    global ent_api_key, ent_api_secret
    entries = []

    for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      if field == 'api_key': ent.insert(0, "02d8fb3c")
      if field == 'api_secret': ent.insert(0, "06717f740e4cd864")
      entries.append((field, ent))
    return entries

def main(root):
   global list, ent, T, progress, ents, root_CSV, file,b_file
   root_CSV = Tk()

   root_CSV.wm_title("Mobile Tornado")
   root_CSV.iconbitmap((resource_path("images\mobiletornado_icon.ico")))

   ents = makeform(root_CSV, fields)

   root_CSV.bind('<Return>', (lambda event, arr=ents:makeform))

   mainframe = Frame(root_CSV)
   mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
   mainframe.columnconfigure(0, weight=1)
   mainframe.rowconfigure(0, weight=1)
   mainframe.pack(pady=5, padx=5)

   list = StringVar(root_CSV)
   list.set('Hot')
   choices = {'InstantTalk', 'Claro', 'Instacom', 'MTN', 'NexusTalk', 'Orange', 'Redline', 'Teamvix', 'Telcel', 'Telus', 'Vodacom', 'Hot'}
   popupMenu = OptionMenu(mainframe, list, *choices)
   Label(mainframe, text="Choose organization").grid(row=1, column=1)
   popupMenu.grid(row=2, column=1)

   b_file = Button(root_CSV, text='upload file', height=1, width=20, bg="turquoise", command=lambda :uplodeFile())
   b_file.pack(side="top", padx=5, pady=5, fill="none", expand=True)

   T = Text(root_CSV, height=10, width=80, bg="snow")
   T.pack( padx=5, pady=5, fill="none", expand=True)

   progress = ttk.Progressbar(root_CSV, orient=HORIZONTAL, length=100, mode='determinate')
   progress.pack()

   b_choose = Button(root_CSV, text='Login', height=3, width=15, bg="turquoise", command=(lambda arr=ents: openNewWindow(root)))
   b_choose.pack(side="left", padx=5, pady=5, fill="none", expand=True)

   b_exit = Button(root_CSV, text='Quit', height=3, width=15, bg="turquoise", command= lambda:root_CSV.destroy())
   b_exit.pack(side="left", padx=5, pady=5, fill="none", expand=True)

   init()
   root_CSV.mainloop()

if __name__ == '__main__':
     main()