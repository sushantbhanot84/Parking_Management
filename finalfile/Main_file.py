from tkinter import *
import re
from sqlite3 import Error
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

try:
    conn=sqlite3.connect('C:\\Users\\Rajan\Desktop\\finalfile-20181031T072626Z-001\\finalfile\\test.db')
except Error as e:
    print(e,'oops')


#-------------Declaration------------#

root=Tk()


def display():
    global regNocheck,s2,s3,root1
    a=s2.get()
    b=s3.get()
    variab=0
    if regNocheck==0:
        try:
            variab=regNoget.get()
        except Exception as e:
            print(e,'Please enter the normal value')
            Confirm_button["text"]="Check Availability"
            pass
            messagebox.showerror("OOPS!!","PLEASE ENTER AN INTEGER REG. NO")
        regNocheck=variab

    num = conn.execute("select "+ d2[b]+ " from Check_avail where Block=?", (d1[a],))   #CHECK PARKING AVAILABILITY FROM DATABASE
    for parking_left in num:
        print()
    parking_left = int(parking_left[0])
    print(parking_left,' parkings available')

    cur=conn.cursor()
    cur.execute("SELECT Reg_No FROM User_detail WHERE Reg_No = ?", (regNocheck,))
    data = cur.fetchall()
    cur.close()                                     #Code for varifying regNo before or after login
    if parking_left > 0:
        if Confirm_button["text"]== "Book parking":
            if len(data)!=0:

                Confirm_button["text"]= 'Check Availability'
                s2['state'] = 'readonly'
                s3["state"] = 'readonly'
                k=regNocheck

                if passlogin!='':
                    check_value('Confirmed',k,d1[a],parking_left)

                else:
                    check_value('not confirmed',k,d1[a],parking_left)

            else:
                Confirm_button["text"] = 'Check Availability'
                messagebox.showerror("Error!!", "Please Register before Booking parking")
                result=messagebox.askokcancel("Not registered","Do you want to register?")
                if result==1:
                    s2['state'] = 'readonly'
                    s3["state"] = 'readonly'
                    onRegister()
                else:
                    s2['state'] = 'readonly'
                    s3["state"] = 'readonly'
                    print('dont register')



        else:
            print(a, " parkings available")
            Confirm_button["text"] = "Book parking"
            print(d3[b])
            price['text']=d3[b]
            s2['state']='disabled'
            s3["state"]='disabled'
            Availdetail['text'] = str(parking_left)+ ' Parkings available.'
            Availdetail['fg']='green'
            messagebox.showinfo("Parking Available", str(parking_left)+' parkings available')

    else:
         print('sorry no parking available')
         Availdetail['text'] = 'No parkings available.'
         Availdetail['fg'] = 'red'


def check_value(val,reg_no,block_name,avail):
    global regNocheck,s2,s3

    cur=conn.cursor()
    cur.execute("SELECT Reg_No FROM parking_confirm WHERE Reg_No = ?", (reg_no,))
    data = cur.fetchall()
    cur.close()  # Code for varifying regNo if already exists and confirmation
    if len(data)!=0 and val=='not confirmed':
        messagebox.showerror("Sorry ", "You Have already booked a parking")
        regNocheck = 0
    elif len(data)!=0 and val=='Confirmed':
        conn.execute("update User_detail set Parking_Alloted=? where Reg_No=?", (block_name, regNocheck))
        conn.execute("update parking_confirm set block_name=? where Reg_No=?",(block_name,reg_no))
        messagebox.showinfo("Parking Updated", "Your parking detail has been updated and has been confirmed")


    elif len(data)==0 and val=='Confirmed':
        conn.execute("update User_detail set Parking_Alloted=? where Reg_No=?", (block_name, regNocheck))
        conn.execute("insert into parking_confirm values(?,?,?)",(reg_no,val,block_name))
        messagebox.showinfo("Parking Booked", "Your parking has been booked and has been confirmed")
        avail-=1

    else:
        conn.execute("update User_detail set Parking_Alloted=? where Reg_No=?", (block_name, regNocheck))
        conn.execute("insert into parking_confirm values(?,?,?)",(reg_no,val,block_name))
        regNocheck = 0
        messagebox.showinfo("Parking Booked", "Parking booked, please give the confirmation at Block 32-204")
        avail-=1

    sqlupdate = 'update Check_avail set %s = :1   where Block=:2' % (d2[s3.get()])
    conn.execute(sqlupdate, (avail, d1[s2.get()]))
    Availdetail['text'] = str(avail) + ' Parkings available.'
    Availdetail['fg'] = 'green'

def availability(regno,passwordlogin):    #METHOD RESPONSIBLE FOR PACKING AND PLACING ALL OBJECTS ON WINDOW
    global root1
    root1 = Tk()
    global window,var,var1,d1,d2,d3,regNoget,regNocheck,passlogin
    root1.title("Check availability")
    window = Frame(root1, height=400, width=400, bg='#FAEBD7')
    var = StringVar()
    var1 = StringVar()
    d1 = {'Block 30': 'block30', 'Block 57': 'block57', 'Hospital': 'Hospital'}
    d2 = {'Car': 'car_avail', 'Bike': 'Bike', 'Cycle': 'Cycle_avail'}
    d3 = {'Car': 2000, 'Bike': 1500, 'Cycle': 1200}
    regNoget = IntVar()
    regNocheck = 0

    passlogin = ''
    regNocheck=regno
    passlogin=passwordlogin
    root1.resizable(0, 0)
    root1.deiconify()
    root1.geometry('400x400')
    global s2,s3
    s2 = Spinbox(window, values=('Block 30', 'Block 57', 'Hospital'), state='readonly', activebackground='red',textvariable=var)
    s3 = Spinbox(window, values=('Car', 'Bike', 'Cycle'), activebackground='red', state='readonly', textvariable=var1)
    s2.place(x=160, y=120, height=30, width=120)
    s3.place(x=160, y=170, height=30, width=120)
    #global Confirm_button
    global Headlabel,price,Label1,Label2,Label3,Label4,RegEntry
    Headlabel = Label(window, text="Check Availability", height=3, width=15, font=('Calibri', 15, 'bold underline'),bg='#FAEBD7', fg='brown')
    price = Label(window, bg='white', relief=RIDGE, anchor=W)
    Label1 = Label(window, text="Select Block", bg='#FAEBD7', font=('Times New Roman', 10))
    Label2 = Label(window, text="Select Vehicle", bg='#FAEBD7', font=('Times New Roman', 10))
    Label3 = Label(window, text="Price ", bg='#FAEBD7', font=('Times New Roman', 10))
    Label4 = Label(window, text='Reg. No', bg='#FAEBD7', font=('Times New Roman', 10))

    Headlabel.place(x=110,y=10)
    price.place(x=160, y=220, height=20, width=120)
    Label1.place(x=70, y=125)
    Label2.place(x=70, y=175)
    Label3.place(x=70, y=225)
    # Label1234=Label(window,text="google").pack()
    global Confirm_button
    Confirm_button = Button(window, text="Check Availability", command=display, activebackground='grey',
                            font=('sans serif', 8, 'bold italic'), bd=4)
    Confirm_button.place(x=100, y=280, height=30, width=110)

    global QuitButton,Availdetail
    QuitButton = Button(window, text='Quit', command=quit)
    Availdetail = Label(window, text='', bg='#FAEBD7', font=('Calibri', 8))
    QuitButton.place(x=320,y=350)
    Availdetail.place(x=156,y=245)
    global RegEntry
    RegEntry = Entry(window, textvariable=regNoget)
    if regNocheck==0:
        Label4.place(x=70,y=95)
        RegEntry.place(x=160,y=90,height=20,width=120)
        RegEntry.insert(END,'')
    window.pack()

    # def on_closing():
    #     root1.withdraw()
    # root1.protocol("WM_DELETE_WINDOW", on_closing)
    # root1.mainloop()



#-----------------------------------------------
#-----------------------------------------------


def Database():
    global conn, cursor
    cursor = conn.cursor()


def Login(event=None):
    def Checkvalue():
        Database()
        print("Value",username.get(),password.get())
        if username.get() == "" or password.get() == "":
            lbl_text.config(text="Please complete the required field!", fg="red")
        else:
            cursor.execute("SELECT * FROM User_detail WHERE Reg_No = ? AND Password = ?", (username.get(), password.get()))
            if cursor.fetchone() is not None:
                # HomeWindow()
                regvalue=int(username.get())
                root2.withdraw()
                availability(regvalue,password.get())
                username.insert(END,'')
                password.insert(END,'')
                lbl_text.config(text="")
            else:
                lbl_text.config(text="Invalid username or password", fg="red")
                username.insert(END,'')
                password.insert(END,'')
        cursor.close()
    Database()

    root2 = Tk()
    root2.title("Python: Parking Management System")
    width = 400
    height = 280
    screen_width = root2.winfo_screenwidth()
    screen_height = root2.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root2.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root2.resizable(0, 0)

    Top = Frame(root2, bd=2, relief=RIDGE)
    Top.pack(side=TOP, fill=X)
    Form = Frame(root2, height=200)
    Form.pack(side=TOP, pady=20)

    lbl_title = Label(Top, text="Python: Simple Login Application", font=('arial', 15))
    lbl_title.pack(fill=X)
    lbl_username = Label(Form, text="Username:", font=('arial', 14), bd=15)
    lbl_username.grid(row=0, sticky="e")
    lbl_password = Label(Form, text="Password:", font=('arial', 14), bd=15)
    lbl_password.grid(row=1, sticky="e")
    lbl_text = Label(Form)
    lbl_text.grid(row=2, columnspan=2)

    username = Entry(Form, font=(14))
    username.grid(row=0, column=1)
    password = Entry(Form, show="*", font=(14))
    password.grid(row=1, column=1)

    btn_login = Button(Form, text="Login", width=45, command=Checkvalue)
    btn_login.grid(pady=25, row=3, columnspan=2)
    btn_login.bind('<Return>', Checkvalue)


    root2.mainloop()


# -------------------------------------------
#---------------PURUSHOTAM-------------------
def Home_page():

#    root1.withdraw()
    root.title('Parking Management System')  # title of window
    root.geometry("600x300")  # size of window
    root.configure(background="#f9d5d5")
    #root.wm_iconbitmap('iconn.ico')
    root.propagate()
    root.resizable(0, 0)

    # Label
    fnt = ('Times', 20, 'bold italic')
    Mylabel = Label(root, text="Welcome to Parking Management System", bg="#f9d5d5", fg="black",
                    font=fnt)  # simply shows the text
    Mylabel.grid(row=1, columnspan=5, padx=60, pady=40)  # making text stable
    # button
    logbutton = Button(root, text="Click here to login", relief=FLAT, bg="orange", fg="white", font="none 11 bold",
                       command=Login)
    regbutton = Button(root, text="New ? Register Here.", relief=FLAT, bg="green", fg="white", font="none 11 bold",
                       command=onRegister)
    chkbutton = Button(root, text="Check Availability for parking", relief=FLAT, bg="blue", fg="white",
                       font="none 11 bold", command=lambda: availability(0,''))
    qutbutton = Button(root, text="Quit", relief=GROOVE, bg="red", fg="white", font="none 11 bold", command=quit)

    # making button stable
    logbutton.grid(row=2, column=1, padx=5, pady=20)
    regbutton.grid(row=2, column=2, padx=5, pady=20)
    chkbutton.grid(row=2, column=3, padx=2, pady=20)
    qutbutton.grid(row=3, column=2)

    # making window stable
    root.mainloop()
#-------------------------------------------------------------------
#------------------------Functions----------------------------------
def test_email(your_pattern):
    pattern = re.compile(your_pattern)
    ans1=0
    email = your_pattern
    match = re.search(r'[\w.-]+@[\w.-]+.\w+', email)
    if match:
        ans1=1
        print(        "valid email :::", match.group())
    else:
        ans1=0
        print(        "not valid:::")
    return ans1
def checkUser(regNo):
     var=1
     cur = conn.cursor()
     cur.execute("SELECT * FROM User_detail")
     rows = cur.fetchall()
     for t in rows:
         print(t[2],"ref",regNo)
         if(int(t[2])==int(regNo)):
             var=0
             break
     #conn.close()
     return var
def onSubmition(password,cPassword, userName,regNo, choice,hostelVar, MobileVar, MailAddressVar):
    print(password,cPassword, userName,regNo, choice,hostelVar, MobileVar, MailAddressVar)
    p=0
    cp=0
    n=0
    id = 0
    hostel=0
    gender=0
    mobile=0
    email=0
    re = str(regNo)
    length = 8
    if (re.isdigit() and len(re) == length):
        id = 1
        RegNoError.config(bg="green")
    else:
        id = 0
        RegNoError.config(bg="red")
        messagebox.showerror("Error Occured", "Invalid Reg.no./UID")
    if(userName=="" or userName==None):
        n=0
        nameError.config(bg="red")
        messagebox.showerror("Error Occured at Name ","Please Enter Your Name.!")
    else:
        n=1
        nameError.config(bg="green")
    if(password!=cPassword):
        cp=0
        CPasswordError.config(bg="red")
        messagebox.showerror("Error Occured at Password ", "Confirm Password and Password is not Same.!")
    else:
        cp=1
        CPasswordError.config(bg="green")

    if(len(password)<6):
        p=0
        passwordError.config(bg="red")
        messagebox.showwarning("Password Length","Password Must be Greater than equal to 6 Digits.")
    else:
        p=1
        passwordError.config(bg="green")
    if(cPassword==""):
        cp=0
        CPasswordError.config(bg="red")
    if(choice==""):
        gender=0
        GenderError.config(bg="red")
        messagebox.showerror("Gender not Selected ", "Please Select your Gender!")
    else:
        gender=1
        GenderError.config(bg="green")
    if(hostelVar=="" or hostelVar.isdigit()==False):
        hostel=0
        HostelError.config(bg="red")
        messagebox.showerror("Not a Valid Hostel.", "Enter Your Hostel Details!")
    else:
        hostel=1
        HostelError.config(bg="green")
        mlen=MobileVar.__len__()
    if(MobileVar=="" or MobileVar.isdigit()==False or mlen!=10):
        mobile=0
        MobileNumberError.config(bg="red")
        messagebox.showerror("Not a Valid Mobile Number", "Enter your Valid Mobile Number.!")
    else:
        mobile=1
        MobileNumberError.config(bg="green")
    if(MailAddressVar==""):
        email=0
        EmailError.config(bg="red")
        messagebox.showerror("Email id is Missing.", "Please Input A Valid Email id")
    else:
        ans=test_email(MailAddressVar)
        if(ans==0):
            email=0
            EmailError.config(bg="red")
            messagebox.showerror("Not Valid.", "Not A Valid Email id")
        else:
            email=1
            EmailError.config(bg="green")
    if(id and cp and p and n and email and hostel and gender and mobile):
        # r=int(regNo.get())
        # u=str(userName.get())
        # ps=str(password.get())
        # vt=str(vehicalType.get())
        val=checkUser(regNo)
        if(val==1):
            messagebox.showinfo("Operation Succesfull","User Created Succesfully.")
            conn = sqlite3.connect('C:\\Users\\Rajan\Desktop\\finalfile-20181031T072626Z-001\\finalfile\\test.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO User_detail VALUES (?,?,?,?,?,?,?)", (userName, password, regNo,hostelVar,MobileVar,MailAddressVar,0))
            conn.commit()
            messagebox.showinfo("Registered Successfully.", "Please login to Continue.!")
            Login()

        else:
            messagebox.showerror("Already Exist","User Already Exist")
            print("User Already Exist.")
    else:
        messagebox.showerror("Fill the form First.!","Enter your Details to complete the registeration")

#----------------------End Of Function-----------------------------
def onRegister():
    global root12
    root12=Tk()
    root12.geometry("556x508")
    root12.resizable(0, 0)
    root12.title("Register Here")
    TopFrame=Frame(root12, height=100, width=556, bg="red")
    TopFrame.pack()
    BottomFrame=Frame(root12, height=408, width=556)
    BottomFrame.pack()
    DisplayLabel=Label(TopFrame,text='Register Here', width=20, height=2,font=('courier', -30, 'bold underline'), fg='blue', bg='yellow')
    DisplayLabel.place(x=100,y=10)
    #
    # photo = PhotoImage(file = "giphy.gif")
    # w = Label(BottomFrame, image=photo)
    # w.pack()
    BottomFrame.propagate(0)
    choice=IntVar()
    Name=Label(BottomFrame, text="Name").place(x=100, y=10)
    NameInput=Entry(BottomFrame)
    NameInput.place(x=300, y=10)
    global nameError
    nameError=Label(BottomFrame, text="", bg="green")
    nameError.place(x=440,y=10)

    RegNo=Label(BottomFrame, text="Reg.No.")
    RegNo.place(x=100,y=50)
    RegNoInput=Entry(BottomFrame)
    RegNoInput.place(x=300,y=50)
    global RegNoError
    RegNoError=Label(BottomFrame, text=None, bg="green")
    RegNoError.place(x=440,y=50)

    Password=Label(BottomFrame, text="Password").place(x=100, y=90)
    PasswordInput=Entry(BottomFrame, show="*")
    PasswordInput.place(x=300, y=90)
    global passwordError
    passwordError=Label(BottomFrame, text="", bg="green")
    passwordError.place(x=440,y=90)
    CPassword=Label(BottomFrame, text="Confirm Password").place(x=100, y=130)
    CPasswordInput=Entry(BottomFrame, show="*")
    CPasswordInput.place(x=300, y=130)
    global CPasswordError
    CPasswordError=Label(BottomFrame, bg="green", text="")
    CPasswordError.place(x=440,y=130)

    Hostel=Label(BottomFrame,text="Hostel/Block")
    Hostel.place(x=100,y=170)
    HostelInput=Entry(BottomFrame)
    HostelInput.place(x=300,y=170)
    global HostelError
    HostelError=Label(BottomFrame, text="", bg="green")
    HostelError.place(x=440,y=170)

    Gender=Label(BottomFrame,text="Gender")
    Gender.place(x=100,y=210)
    Radiobutton(BottomFrame,variable = choice,text="Male",value=1,padx=20,indicatoron = 0).place(x=230,y=210)
    Radiobutton(BottomFrame,variable = choice,text="Female",value=2,padx=20,indicatoron = 0).place(x=330,y=210)
    global GenderError
    GenderError=Label(BottomFrame, text="", bg="green")
    GenderError.place(x=440,y=210)

    MobileNumber=Label(BottomFrame,text="Mobile Number")
    MobileNumber.place(x=100,y=250)
    MobileNumberInput=Entry(BottomFrame)
    MobileNumberInput.place(x=300,y=250)
    global MobileNumberError
    MobileNumberError=Label(BottomFrame, text="", bg="green")
    MobileNumberError.place(x=440,y=250)

    Emailid=Label(BottomFrame,text="Email Id")
    Emailid.place(x=100,y=290)
    EmailidInput=Entry(BottomFrame,width=30)
    EmailidInput.place(x=250,y=290)
    global EmailError
    EmailError=Label(BottomFrame, text="", bg="green")
    EmailError.place(x=440,y=290)
    RegisterButton=Button(BottomFrame,text="Register",font=('mono space',10, 'bold'), fg='black', bg='grey',command=lambda :onSubmition(PasswordInput.get(),CPasswordInput.get(),NameInput.get(),RegNoInput.get(),1,HostelInput.get(),MobileNumberInput.get(),EmailidInput.get()))
    RegisterButton.place(x=230,y=350)
    country=Label(BottomFrame,text="in",width=3,bg="orange").place(x=260,y=250)
    root12.mainloop()



Home_page()



