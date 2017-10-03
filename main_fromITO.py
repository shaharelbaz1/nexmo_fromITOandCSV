# -*- coding: utf-8 -*-
from Tkinter import *
import Tkinter as tk
import ttk
import IP_in_out
from suds.client import Client
from smpplib import gsm
import organizationFile
import smpplib
import sys
import sendSMS
import os
reload(sys)
sys.setdefaultencoding("ISO-8859-1")


global long_suffix, short_suffix
global api_key, api_secret
global url,org_id ,username,password
global users
global list



long_suffix = ':8998/PTX/Provisioning?wsdl'
short_suffix = ':8080/MTWebShortProvisioning/MTSProvisioning.asmx?wsdl'

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def GetAuthenticationLong(URL,username,Password):
    clientShort = Client(URL + short_suffix)
    myWebsShort = clientShort.service
    response = myWebsShort.testHash(Password)
    clientLong = Client(URL+long_suffix)
    Authentication = clientLong.factory.create('AuthenticationHeader')
    Authentication.Created = response.created
    Authentication.Nonce = response.b64Nonce
    Authentication.Password = response.b64SHA1Hash
    Authentication.Username = username
    return Authentication


def GetClientLong(URL,username,Password):
    client = Client(URL+long_suffix)
    Authentication = GetAuthenticationLong(URL,username,Password)
    client.set_options(soapheaders=Authentication)
    return client

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
            PhoneNumber = user.UserPhoneDetails.PhoneNumber
            userNameSIP = user.ClientIdentifierList.ClientIdentifier[0].Details.Value

            password = user.Details.Password
            #org = orgLink(list.get())
            IPserver=IP_in_out.options(getServers_id_ip(user))

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
            PhoneNumber = user.UserPhoneDetails.PhoneNumber
            #userNameSIP = user.ClientIdentifierList.ClientIdentifier[0].Details.Value

            #password = user.Details.Password
            org = orgLink(list.get())
            #IPserver=IP_in_out.options(getServers_id_ip(user))

            msg = "Download from here: "  + org
            sendSMS.send(api_key, api_secret, PhoneNumber, msg)

            L_canvSend.config(text="send %s/%s" % (j + 1, count1))
            L_canvSend.update_idletasks()
            j=j+1

        i=i+1

def sendBoth():
    i = 0
    j = 0
    for user in users:
        if arr[i].get() == 1:
            PhoneNumber = user.UserPhoneDetails.PhoneNumber
            userNameSIP = user.ClientIdentifierList.ClientIdentifier[0].Details.Value

            password = user.Details.Password
            # org = orgLink(list.get())
            IPserver = IP_in_out.options(getServers_id_ip(user))
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

def getServers_id_ip(user):
    ans = []
    ExportClient = GetClientLong(url, username, password)
    ExportService = ExportClient.service
    SiteRetrievalFilter = ExportClient.factory.create('SiteRetrievalFilter')

    SiteRetrievalFilter.OrganizationId = org_id
    SiteRetrievalFilter.IdFilter = False
    SiteRetrievalFilter.TypeFilter=False
    SiteRetrievalFilter.Type=False
    SiteRetrievalFilter.NameFilter=False
    SiteRetrievalFilter.HostFilter=False
    SiteRetrievalFilter.StateFilter=False
    res = ExportService.GetSite(SiteRetrievalFilter)
    list = res.SiteList.Site
    for site in list:
        if user.Details.PrimarySiteId==site.Id :
            return site.Details.Host

def is_mobile(user):
    for i in range(0, len(user.ClientIdentifierList.ClientIdentifier)) :
        if user.ClientIdentifierList.ClientIdentifier[i].Details.Type != 'SIP':
            return 0
    return 1

def init():
    global url, org_id, username, password, api_key, api_secret
    url =ents[0][1].get()
    org_id =ents[1][1].get()
    username =ents[2][1].get()
    password =ents[3][1].get()
    api_key =ents[4][1].get()
    api_secret = ents[5][1].get()

fields = 'url','org id','username', "password", 'api_key', 'api_secret'

def makeform(root, fields):
    global entUrl, ent_orgId, ent_username, ent_password, ent_api_key, ent_api_secret
    entries = []

    for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      if field =='url': ent.insert(0, "http://192.168.103.165")
      if field == 'org id': ent.insert(0, "706")
      if field == 'username': ent.insert(0, "shahar@taxi.com")
      if field == 'password': ent.insert(0, "111111")
      if field == 'api_key': ent.insert(0, "02d8fb3c")
      if field == 'api_secret': ent.insert(0, "06717f740e4cd864")
      entries.append((field, ent))
    return entries

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
    global b_selectAll, count1
    i = 0
    count1 = 0
    count2 = 0
    for user in users:
        if is_mobile(user):
            if arr[i].get() != 1:
                b_selectAll.deselect()
            count2 = count2 + 1
            if arr[i].get() == 1:
                count1 = count1 + 1
        i = i + 1
    if count1 == count2:
        b_selectAll.select()
    L_canvSelection.config(text="select %s/%s" % (count1, count2))

class openNewWindow(tk.Toplevel):

    def __init__(self, parent):

        T.insert('1.0', "Please wait...\n")
        T.update_idletasks()

        progress['value'] = 20
        root_ITO.update_idletasks()

        global arr, b_selectAll, x
        global users
        global L_canvSelection, L_canvSend, count1
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


        ExportClient = GetClientLong(url, username, password)
        ExportService = ExportClient.service

        progress['value'] = 50
        root_ITO.update_idletasks()
        c.delete(wait)


        i = 0
        res_OrganisationUsers = ExportService.GetUser(SearchField='OrganisationId', SearchString=org_id)
        progress['value'] = 80
        root_ITO.update_idletasks()

        checkButtons = []
        try:
            x= tk.IntVar()
            b_selectAll = tk.Checkbutton(self, text='select all', variable=x,font = "Helvetica 10 bold italic",command=lambda arr=checkButtons: selectAll(checkButtons))
            b_selectAll.pack(side="top", anchor="w")

            L_canvSelection = Label(self, bg="gray94", text="", font="Helvetica 10 bold italic")
            L_canvSelection.pack(side="top", expand=True, anchor="w")

            L_canvSend = Label(self, bg="gray94", text="", font="Helvetica 10 bold italic")
            L_canvSend.pack(side="bottom", expand=True, anchor="w")

            users = res_OrganisationUsers.UserList.User
            for user in users:
                arr[i] = tk.IntVar()

                if is_mobile(user):

                    displayName = user.Details.DisplayName
                    check = tk.Checkbutton(f, text=displayName, variable=arr[i], command=lambda arr=users: countSelection())
                    check.pack(side="top", anchor="w")
                    checkButtons.append(check)

                i = i + 1

            b_sendLink = Button(self, text='send SMS\nwith download link', height=3, width=15, bg="turquoise",
                                command=sendLink)
            b_sendLink.pack(side="top", padx=0, pady=0, fill="none",anchor= "w", expand=True)

            b_sendDetails = Button(self, text='send SMS\nwith user details', height=3, width=15, bg="turquoise",
                                   command=sendDetails)
            b_sendDetails.pack(side="top", padx=0, pady=0, fill="none",anchor= "w", expand=True)

            b_both = Button(self, text='send Both', height=3, width=15, bg="turquoise",
                                   command=sendBoth)
            b_both.pack(side="top", padx=0, pady=0, fill="none", anchor="w", expand=True)

            b_exit = Button(self, text='Quit', height=3, width=15, bg="turquoise", command=lambda :self.destroy())
            b_exit.pack(side="top", padx=0, pady=0, fill="none",anchor= "w", expand=True)


            self.update()
            c.config(scrollregion=c.bbox("all"))

        except:
            try:
                c.create_text(20, 90, anchor='nw', text=res_OrganisationUsers.Response.ErrorMessage, font = "Helvetica 10 bold italic")
            except:
                c.create_text(20, 90, anchor='nw', text='no users for this organization', font = "Helvetica 16 bold italic")
        progress['value'] = 100




def main(root):
   global list, ent, T, progress, ents, root_ITO
   global arr, b_selectAll, x
   global users
   global T_canvSelection, T_canvSend, count1
   printToXml=False
   IsExportObj=False
   root_ITO = Tk()

   root_ITO.wm_title("Mobile Tornado")
   root_ITO.iconbitmap((resource_path("images\mobiletornado_icon.ico")))

   ents = makeform(root_ITO, fields)


   root_ITO.bind('<Return>', (lambda event, arr=ents:makeform))

   mainframe = Frame(root_ITO)
   mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
   mainframe.columnconfigure(0, weight=1)
   mainframe.rowconfigure(0, weight=1)
   mainframe.pack(pady=5, padx=5)

   list = StringVar(root_ITO)
   list.set('Hot')
   choices = {'InstantTalk', 'Claro', 'Instacom', 'MTN', 'NexusTalk', 'Orange', 'Redline', 'Teamvix', 'Telcel', 'Telus', 'Vodacom', 'Hot'}
   popupMenu = OptionMenu(mainframe, list, *choices)
   Label(mainframe, text="Choose organization").grid(row=1, column=1)
   popupMenu.grid(row=2, column=1)

   T = Text(root_ITO, height=10, width=80, bg="snow")
   T.pack( padx=5, pady=5, fill="none", expand=True)

   progress = ttk.Progressbar(root_ITO, orient=HORIZONTAL, length=100, mode='determinate')
   progress.pack()

   b_choose = Button(root_ITO, text='Login', height=3, width=15, bg="turquoise", command=(lambda arr=ents: openNewWindow(root)))
   b_choose.pack(side="left", padx=5, pady=5, fill="none", expand=True)

   b_exit = Button(root_ITO, text='Quit', height=3, width=15, bg="turquoise", command= lambda:root_ITO.destroy())
   b_exit.pack(side="left", padx=5, pady=5, fill="none", expand=True)

   init()
   root_ITO.mainloop()

if __name__ == '__main__':
    main()