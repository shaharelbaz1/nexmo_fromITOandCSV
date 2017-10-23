# -*- coding: utf-8 -*-
from Tkinter import *
import Tkinter as tk
import ttk
import IP_in_out
from suds.client import Client
import organizationFile
import sys
import sendSMS
import os
import base64
from tkFileDialog import askopenfilename, askdirectory
import datetime
import requests
import json

reload(sys)
sys.setdefaultencoding("ISO-8859-1")\

global long_suffix, short_suffix
global api_key, api_secret
global url,org_id ,username,password
global users
global list


fields = 'url','username', "password", 'api_key', 'api_secret'

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def GetAuthenticate(URL, username, password):
    global token
    url = URL+':8002/api/authenticate'
    payload = {'email': username, 'password': password}
    headers = {'content-type': 'application/json'}

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = json.loads(r.text)
    token = data["token"]

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

# def getServers_id_ip(user):
#     ans = []
#     ExportClient = GetClient(url, username, password)
#     ExportService = ExportClient.service
#     SiteRetrievalFilter = ExportClient.factory.create('SiteRetrievalFilter')
#
#     SiteRetrievalFilter.OrganizationId = org_id
#     SiteRetrievalFilter.IdFilter = False
#     SiteRetrievalFilter.TypeFilter=False
#     SiteRetrievalFilter.Type=False
#     SiteRetrievalFilter.NameFilter=False
#     SiteRetrievalFilter.HostFilter=False
#     SiteRetrievalFilter.StateFilter=False
#     res = ExportService.GetSite(SiteRetrievalFilter)
#     list = res.SiteList.Site
#     for site in list:
#         if user.Details.PrimarySiteId==site.Id :
#             return site.Details.Host
def getCountryCode(country):
    url_getCountry = url + ':8002/api/countries/list?api_key=' + token
    r = requests.get(url_getCountry)
    data = json.loads(r.text)

    for Country in data:
        if Country['name']== country:
            return Country['country_code']
    return os.error


def is_mobile(userId):
    url_getUser = url + ':8002/api/subscriber/' + userId + '?api_key=' + token
    r = requests.get(url_getUser)
    data = json.loads(r.text)

    if data['country_code']=='PC Client':
        return False
    else:
        return True

def getHostSite(site):
    url_getSite = url + ':8002/api/site/list?api_key=' + token
    r = requests.get(url_getSite)
    data = json.loads(r.text)

    for Site in data:
        if Site['_id']== site:
            return Site['host']
    return os.error

def getUserDetails(userId):
    url_getUser = url + ':8002/api/subscriber/'+userId+'?api_key=' + token
    r = requests.get(url_getUser)
    data = json.loads(r.text)

    user=[]
    countryCode=getCountryCode(data['country_code'])
    user.append(data['name'])
    user.append(countryCode+data['phone_number'])
    user.append(data['identifiers'][0]['value'])
    user.append(data['password'])
    user.append(getHostSite(data['primary_site_id']))

    return user

def selectAll(checkButtons, arr, x):
    if x.get() == 1:
        for check in checkButtons:
            check.select()
    else:
        for check in checkButtons:
            check.deselect()
    countSelection(checkButtons, arr)

def countSelection(checkButtons, arr):
    global b_selectAll, count1
    i = 0
    count1 = 0
    count2 = 0
    for check in checkButtons:
        if arr[i].get() != 1:
            b_selectAll.deselect()
        count2 = count2 + 1
        if arr[i].get() == 1:
            count1 = count1 + 1
        i = i + 1
    if count1 == count2:
        b_selectAll.select()
    L_canvSelection.config(text="select %s/%s" % (count1, count2))

def SelectOne(checkButtons, i):
    global arrOrg
    if arrOrg[i].get()==1:
        j=0
        for check in checkButtons:
            if j!=i:
                check.deselect()
            j=j+1

######send SMS function
def sendDetails():
    global encode
    i=0
    j=0
    send =0
    if count1==0:
        L_canvSend.config(text="please select users", fg='red')
        L_canvSend.update_idletasks()
    else:
        path = askdirectory()
        fd = open('%s/sendLog_%s' % (path, datetime.datetime.now().date()), "w")
        passEncode = encode.get()
        for check in checkButtonUser:
            if arrUser[i].get() == 1:
                user = getUserDetails(arrUserId[i])
                PhoneNumber = user[1]
                userNameSIP = user[2]

                password = user[3]
                #org = orgLink(list.get())
                IPserver=IP_in_out.options(user[4])

                if passEncode==1:
                    msg = 'getwml.aspx?uname=' + userNameSIP + '&passs=' + base64.b64encode(password) + '&server=' + IPserver
                else:
                    msg = 'getwml.aspx?uname=' + userNameSIP + '&pass=' + password + '&server=' + IPserver

                success= sendSMS.send(api_key, api_secret, PhoneNumber, msg)
                send= send+success
                if success==1:
                    fd.write(user[0].encode('utf-8') +'  yes\n')
                else:
                    fd.write(user[0].encode('utf-8') +'  no\n')



                L_canvSend.update_idletasks()
                j = j + 1

            i=i+1
        L_canvSend.config(text="success %s/%s               " % (send, count1),fg='black')
        L_canvSend.update_idletasks()
        fd.close()

def sendLink():
    i=0
    j=0
    send=0
    if count1 == 0:
        L_canvSend.config(text="please select users", fg='red')
        L_canvSend.update_idletasks()
    else:
        path = askdirectory()
        fd = open('%s/sendLog_%s' % (path, datetime.datetime.now().date()), "w")
        for check in checkButtonUser:
            if arrUser[i].get() == 1:
                user=getUserDetails(arrUserId[i])
                PhoneNumber = user[1]
                #userNameSIP = user + '@' + domain

                #password = user.Details.Password
                org = orgLink(list.get())
                #IPserver=IP_in_out.options(getServers_id_ip(user))

                msg = "Download from here: "  + org
                success = sendSMS.send(api_key, api_secret, PhoneNumber, msg)
                send = send + success
                if success==1:
                    fd.write(user[0].encode('utf-8')+'  yes\n')
                else:
                    fd.write(user[0].encode('utf-8') + '  no\n')

                L_canvSend.config(text="send %s/%s               " % (j + 1, count1), fg='black')
                L_canvSend.update_idletasks()
                j = j + 1

            i = i + 1
        L_canvSend.config(text="success %s/%s               " % (send, count1), fg='black')
        L_canvSend.update_idletasks()
        fd.close()

def sendBoth():
    global encode
    i = 0
    j = 0
    send=0
    if count1 == 0:
        L_canvSend.config(text="please select users", fg='red')
        L_canvSend.update_idletasks()
    else:
        path = askdirectory()
        fd = open('%s/sendLog_%s' % (path, datetime.datetime.now().date()), "w")
        passEncode = encode.get()
        for check in checkButtonUser:
            if arrUser[i].get() == 1:
                user = getUserDetails(arrUserId[i])
                PhoneNumber = user[1]
                userNameSIP = user[2]

                password = user[3]
                # org = orgLink(list.get())
                IPserver = IP_in_out.options(user[4])
                org = orgLink(list.get())


                if passEncode==1:
                    msg = 'getwml.aspx?uname=' + userNameSIP + '&passs=' + base64.b64encode(password) + '&server=' + IPserver +"&url=" +org
                else:
                    msg = 'getwml.aspx?uname=' + userNameSIP + '&pass=' + password + '&server=' + IPserver +"&url=" +org

                success = sendSMS.send(api_key, api_secret, PhoneNumber, msg)
                send = send + success
                if success==1:
                    fd.write(user[0].encode('utf-8')+'  yes\n')
                else:
                    fd.write(user[0].encode('utf-8') + '  no\n')

                L_canvSend.config(text="send %s/%s               " % (j + 1, count1), fg='black')
                L_canvSend.update_idletasks()
                j = j + 1

            i = i + 1
        L_canvSend.config(text="success %s/%s               " % (send, count1), fg='black')
        L_canvSend.update_idletasks()
        fd.close()

def init():
    global url, org_id, username, password, api_key, api_secret
    url =ents[0][1].get()
    username =ents[1][1].get()
    password =ents[2][1].get()
    api_key =ents[3][1].get()
    api_secret = ents[4][1].get()

def click_url(event):
    emptyUrl.pack_forget()
def click_username(event):
    emptyUsername.pack_forget()
def click_password(event):
    emptyPassword.pack_forget()
def click_apiKey(event):
    emptyApi_key.pack_forget()
def click_secretKey(event):
    emptyApi_secret.pack_forget()

def makeform(root, fields):
    global entUrl, ent_username, ent_password, ent_api_key, ent_api_secret, emptyUrl, emptyUsername, emptyPassword, emptyApi_key, emptyApi_secret
    entries = []

    for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)

      if field =='url':
          emptyUrl = Label(row, width=15, text="url is empty", anchor='w', fg='red')
          ent.bind("<Button-1>", click_url)
      if field == 'username':
          emptyUsername = Label(row, width=15, text="user name is empty", anchor='w', fg='red')
          ent.bind("<Button-1>", click_username)
      if field == 'password':
          emptyPassword = Label(row, width=15, text="password is empty", anchor='w', fg='red')
          ent.bind("<Button-1>", click_password)
      if field == 'api_key':
          emptyApi_key = Label(row, width=15, text="api key is empty", anchor='w', fg='red')
          ent.bind("<Button-1>", click_apiKey)
      if field == 'api_secret':
          emptyApi_secret = Label(row, width=15, text="api secret is empty", anchor='w', fg='red')
          ent.bind("<Button-1>", click_secretKey)

      row.pack(side='top', fill='x', padx=5, pady=5)
      lab.pack(side='left', fill='none')
      ent.pack(side='left', expand=YES, fill='both')
      if field =='url':
          ent.insert(0, "http://192.168.103.142")
      if field == 'username':
          ent.insert(0, "admin@ptx.com")
      if field == 'password':
          ent.insert(0, "admin")
      if field == 'api_key':
          ent.insert(0, "b3acf11d")
      if field == 'api_secret':
          ent.insert(0, "4ac296008dad0172")
      entries.append((field, ent))
    return entries

class openUsersWindow(tk.Toplevel):

    def __init__(self, parent):
        global arrUser, arrUserId, b_selectAll, encode, orgId, arrOrgId, checkButtonUser
        global userPhoneNumbers, domain
        global L_canvSelection, L_canvSend, count1, url, L_canvSendSuccess
        global emptyUrl, emptyOrgId, emptyUsername, emptyPassword, emptyApi_key, emptyApi_secret, details

        details={}
        T.insert(END, "Please wait...\n")
        T.update_idletasks()

        progressUser['value'] = 20
        root_ITO.update_idletasks()

        try:
                    count1 = 0
                    try:
                        tk.Toplevel.__init__(self, parent)

                        self.title('choose users')
                        self.iconbitmap((resource_path("images\MobilTornado_splash_image_icon.ico")))
                        self.geometry('400x600')

                        vscrollbar = tk.Scrollbar(self)

                        c = tk.Canvas(self, background="gray94", width=100, height=50, yscrollcommand=vscrollbar.set,scrollregion=(0, 0, 100, 100))

                        vscrollbar.config(command=c.yview)
                        vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                        c.bind_all('<MouseWheel>', lambda event: c.yview_scroll(int(-1 * (event.delta / 120)), "units"))
                        c.bind_all('<Next>', lambda event: c.yview_scroll(4, 'units'))
                        c.bind_all('<Prior>', lambda event: c.yview_scroll(-4, 'units'))

                        f = tk.Frame(c)  # Create the frame which will hold the widgets

                        c.pack(side="left", fill="both", expand=True)

                        c.create_window(0, 0, window=f, anchor='nw')

                        wait = c.create_text(120, 90, anchor='nw', text="Please wait...",
                                             font="Helvetica 12 bold italic")

                        progressUser['value'] = 50
                        root_ITO.update_idletasks()
                        c.delete(wait)

                        i = 0

                        progressUser['value'] = 80
                        root_ITO.update_idletasks()

                        checkButtonUser = []
                        try:
                            x = tk.IntVar()
                            encode = tk.IntVar()
                            b_selectAll = tk.Checkbutton(self, text='select all', variable=x,
                                                         font="Helvetica 10 bold italic",
                                                         command=lambda arr=checkButtonUser: selectAll(checkButtonUser, arrUser, x))
                            b_selectAll.pack(side="top", anchor="w")

                            L_canvSelection = Label(self, bg="gray94", text="", font="Helvetica 10 bold italic")
                            L_canvSelection.pack(side="top", expand=True, anchor="w")

                            b_encodePass = tk.Checkbutton(self, text='encode password', variable=encode,
                                                          font="Helvetica 10 bold italic")
                            b_encodePass.pack(side="top", anchor="w")

                            L_canvSend = Label(self, bg="gray94", text="", font="Helvetica 10 bold italic")
                            L_canvSend.pack(side="bottom", expand=True, anchor="w")

                            j = 0
                            arrUserId = {}
                            arrUser = {}
                            i = 0
                            for check in checkButtonsOrg:
                                if arrOrg[j].get() == 1:
                                    url_getUser = url + ':8002/api/subscriber/list/' + str(arrOrgId[j]) + '?api_key=' + token
                                    r = requests.get(url_getUser)
                                    data = json.loads(r.text)

                                    for user in data:
                                        if (is_mobile(user[u'_id'])):
                                            arrUser[i] = tk.IntVar()
                                            arrUserId[i] = user[u'_id']
                                            displayName = user[u'name']
                                            check = tk.Checkbutton(f, text=displayName, variable=arrUser[i],command=lambda arr=data: countSelection(checkButtonUser,arrUser))
                                            check.pack(side="top", anchor="w")
                                            checkButtonUser.append(check)

                                            i = i + 1
                                j = j + 1

                            b_sendLink = Button(self, text='send SMS\nwith download link', height=3, width=15,
                                                bg="turquoise",
                                                command=sendLink)
                            b_sendLink.pack(side="top", padx=0, pady=0, fill="none", anchor="w", expand=True)

                            b_sendDetails = Button(self, text='send SMS\nwith user credentials', height=3, width=15,
                                                   bg="turquoise",
                                                   command=sendDetails)
                            b_sendDetails.pack(side="top", padx=0, pady=0, fill="none", anchor="w", expand=True)

                            b_both = Button(self, text='send Both', height=3, width=15, bg="turquoise",
                                            command=sendBoth)
                            b_both.pack(side="top", padx=0, pady=0, fill="none", anchor="w", expand=True)

                            b_exit = Button(self, text='Quit', height=3, width=15, bg="turquoise",
                                            command=lambda: self.destroy())
                            b_exit.pack(side="top", padx=0, pady=0, fill="none", anchor="w", expand=True)

                            self.update()
                            c.config(scrollregion=c.bbox("all"))
                            progressUser['value'] = 100

                        except:
                            try:
                                c.create_text(20, 90, anchor='nw', text="ERROR! "+data["error"],
                                              font="Helvetica 10 bold italic")
                            except:
                                c.create_text(20, 90, anchor='nw', text='no users for this organization',
                                              font="Helvetica 16 bold italic")
                    except:
                        T.insert('end', "error: %s\n" %+data["error"])
                        T.update_idletasks()
                        progressUser['value'] = 0
                        root_ITO.update_idletasks()
                    progressUser['value'] = 0
        except:
                    T.insert('end', "error with url\n")
                    T.update_idletasks()
                    progressUser['value'] = 0
                    root_ITO.update_idletasks()





        root_ITO.mainloop()

class openOrgWindow(tk.Toplevel):

    def __init__(self, parent):
        global arrOrg, b_selectAll, encode, progressUser, arrOrgId,checkButtonsOrg
        global userPhoneNumbers, domain
        global L_canvSelection, L_canvSend, count1, url, L_canvSendSuccess
        global emptyUrl, emptyOrgId, emptyUsername, emptyPassword, emptyApi_key, emptyApi_secret, details

        details={}
        arrOrgId={}
        init()
        if url=='': emptyUrl.pack(side="right", expand=YES, fill='none')
        elif username =='': emptyUsername.pack(side="right", expand=YES, fill='none')
        elif password =='': emptyPassword.pack(side="right", expand=YES, fill='none')
        elif api_key =='': emptyApi_key.pack(side="right", expand=YES, fill='none')
        elif api_secret =='': emptyApi_secret.pack(side="right", expand=YES, fill='none')
        else:
            if 'http' not in url:
                url = 'http://' + url

            T.insert(END, "Please wait...\n")
            T.update_idletasks()

            progressOrg['value'] = 20
            root_ITO.update_idletasks()

            try:
                count1 = 0
                GetAuthenticate(url, username, password)
                url_getOrg = url + ':8002/api/organization/list?api_key=' + token
                r = requests.get(url_getOrg)
                data = json.loads(r.text)

                try:
                    arrOrg = {}
                    tk.Toplevel.__init__(self, parent)

                    self.title('choose organization')
                    self.iconbitmap((resource_path("images\MobilTornado_splash_image_icon.ico")))
                    self.geometry('400x600')

                    vscrollbar = tk.Scrollbar(self)

                    c = tk.Canvas(self, background="gray94",width=100,height=50, yscrollcommand=vscrollbar.set,scrollregion=(0, 0, 100, 100))

                    vscrollbar.config(command=c.yview)
                    vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                    c.bind_all('<MouseWheel>', lambda event: c.yview_scroll(int(-1 * (event.delta / 120)), "units"))
                    c.bind_all('<Next>',  lambda event: c.yview_scroll(4, 'units'))
                    c.bind_all('<Prior>',  lambda event: c.yview_scroll(-4, 'units'))

                    f = tk.Frame(c)  # Create the frame which will hold the widgets

                    c.pack(side="left", fill="both", expand=True)

                    c.create_window(0, 0, window=f, anchor='nw')

                    wait = c.create_text(120, 90, anchor='nw', text="Please wait..." ,font = "Helvetica 12 bold italic")

                    progressOrg['value'] = 50
                    root_ITO.update_idletasks()
                    c.delete(wait)


                    i = 0

                    progressOrg['value'] = 80
                    root_ITO.update_idletasks()

                    checkButtonsOrg = []
                    y = tk.IntVar()
                    b_selectAll = tk.Checkbutton(self, text='select all', variable=y, font="Helvetica 10 bold italic", command=lambda arr=checkButtonsOrg: selectAll(checkButtonsOrg, arrOrg, y))
                    b_selectAll.pack(side="top", anchor="w")

                    L_canvSelection = Label(self, bg="gray94", text="", font="Helvetica 10 bold italic")
                    L_canvSelection.pack(side="top", expand=True, anchor="w")
                    try:


                        for org in data:
                            arrOrg[i] = tk.IntVar()

                            displayName = org[u'name']

                            arrOrgId[i]=org[u'_id']
                            check = tk.Checkbutton(f, text=displayName, variable=arrOrg[i], command=lambda arr=data: countSelection(checkButtonsOrg,arrOrg))#, command=lambda j=i: SelectOne(checkButtonsOrg,j))
                            check.pack(side="top", anchor="w")
                            checkButtonsOrg.append(check)

                            i = i + 1

                        b_OK = Button(self, text='OK', height=3, width=15, bg="turquoise", command=lambda: openUsersWindow(parent))
                        b_OK.pack(side="top", padx=0, pady=0, fill="none",anchor= "w", expand=True)

                        b_exit = Button(self, text='Quit', height=3, width=15, bg="turquoise", command=lambda :self.destroy())
                        b_exit.pack(side="top", padx=0, pady=0, fill="none",anchor= "w", expand=True)

                        progressUser = ttk.Progressbar(self, orient=HORIZONTAL, length=100, mode='determinate')
                        progressUser.pack()


                        self.update()
                        c.config(scrollregion=c.bbox("all"))
                        progressOrg['value'] = 100

                    except:
                        try:
                            c.create_text(20, 90, anchor='nw', text=("ERROR! "+data["error"]), font = "Helvetica 10 bold italic")
                        except:
                            c.create_text(20, 90, anchor='nw', text='no users for this organization', font = "Helvetica 16 bold italic")
                except:
                    T.insert('end', "error: %s\n" % data["error"])
                    T.update_idletasks()
                    progressOrg['value'] = 0
                    root_ITO.update_idletasks()
                progressOrg['value'] = 0
            except:
                T.insert('end', "error with url\n")
                T.update_idletasks()
                progressOrg['value'] = 0
                root_ITO.update_idletasks()


        root_ITO.mainloop()

def main(root):
   global list, ent, T, progressOrg, ents, root_ITO
   global arrUser, b_selectAll, x, details
   global userPhoneNumbers
   global T_canvSelection, T_canvSend, count1
   root_ITO = Tk()

   root_ITO.wm_title("Mobile Tornado")
   root_ITO.iconbitmap(resource_path("images\MobilTornado_splash_image_icon.ico"))

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
   popupMenu.config(width=15)

   T = Text(root_ITO, height=10, width=80, bg="snow")
   T.pack( padx=5, pady=5, fill="none", expand=True)

   progressOrg = ttk.Progressbar(root_ITO, orient=HORIZONTAL, length=100, mode='determinate')
   progressOrg.pack()

   b_choose = Button(root_ITO, text='Login', height=3, width=15, bg="turquoise", command=(lambda arr=ents: openOrgWindow(root)))
   b_choose.pack(side="left", padx=5, pady=5, fill="none", expand=True)

   b_exit = Button(root_ITO, text='Quit', height=3, width=15, bg="turquoise", command= lambda:root_ITO.destroy())
   b_exit.pack(side="left", padx=5, pady=5, fill="none", expand=True)

   root_ITO.mainloop()

if __name__ == '__main__':
    main()