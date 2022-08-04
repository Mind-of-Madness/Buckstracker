from tkinter import *
from tkinter import messagebox
import sys
from Graphs import *
import mysql.connector as m
from treeview_sql import *

c=m.connect(host="localhost",user="root",passwd="mysql",database="buckstracker")
cur=c.cursor()

#Deletion of Account
def deleteaccfn():
    global username
    delete_win=Tk()
    delete_win.geometry('350x125')

    signdel=Label(delete_win,text="DELETE ACCOUNT",font=("Verdana",13,"bold"),fg="navy").grid(row=0,column=1,sticky="w")

    name=Label(delete_win,text="Enter username : ",font=("Verdana",10),fg="navy").grid(row=1,column=0)
    username=Entry(delete_win)
    username.grid(row=1,column=1)


    pswd=Label(delete_win,text="Enter password : ",font=("Verdana",10),fg="navy").grid(row=2,column=0)
    password=Entry(delete_win,show='*')
    password.grid(row=2,column=1)

    #Checking for correct username/password
    def checkdel():
        a=username.get()
        b=password.get()

        if a!="" and b!="":
            cur.execute("select * from login where username='"+ a +"'")
            data=cur.fetchall()

            # Verifying username, then password to delete acc
            if len(data)==0:
                messagebox.showerror("Notice","You have not entered a registered username")
            elif data[0][0]==a and data[0][1]==b:
                cur.execute("delete from login where username= '" +a+ "' and password= '" +b+ "'")
                c.commit()
                cur.execute("delete from income where name= '"+a+"'")
                c.commit()
                cur.execute("delete from expenditure where name= '" +a+"'")
                c.commit()
                messagebox.showinfo("Message","Successfully deleted account")
                delete_win.destroy()                
            else:
                messagebox.showerror("Notice","Your password or username is not entered correctly")
                
        elif a=="" and b=="":
            messagebox.showerror("Notice","You have not entered a username or password")

    label_dummy=Label(delete_win,text="").grid(row=4,column=0)

    button_del=Button(delete_win,text="DELETE ACCOUNT",font=("Calibre",12,"bold"),fg="navy",command= checkdel)
    button_del.grid(row=5,column=1,sticky="w")

#Login Screen
def loginwindow():
    global login,us
    login=Tk()
    login.geometry('400x175')
    login.title("LOGIN SCREEN")
    label1=Label(login,text="Do you want to login or signup or delete account ?",font=("Verdana",10)).place(x=50,y=0)
loginwindow()

#Login function
def signinfunc():
    global us,signin,login,mainname
    #us: String variable for username while mainame is value of us
    signin=Tk()
    signin.geometry("300x140")
    signin.title("SIGNIN SCREEN")

    sign=Label(signin,text="LOGIN",font=("Verdana",13,"bold"),fg="indian red").grid(row=0,column=1,sticky="w")

    name=Label(signin,text="Enter username : ",font=("Verdana",10),fg="indian red").grid(row=1,column=0)
    us=Entry(signin)
    us.grid(row=1,column=1)


    pswd=Label(signin,text="Enter password : ",font=("Verdana",10),fg="indian red").grid(row=2,column=0)
    password=Entry(signin,show='*')
    password.grid(row=2,column=1)

    empty=Label(signin,text="").grid(row=3,column=0)
    
    mainname=us.get()

    #Checking for correct username/password for login
    def checklogin():
        a=us.get()
        b=password.get()
        
        if a!="" and b!="":
            cur.execute("select * from login where username='"+ a +"'")
            data=cur.fetchall()
            
            if len(data)==0:
                messagebox.showerror("Notice","You have not entered a registered username")
            elif data[0][0]==a and data[0][1]==b:
                messagebox.showinfo("Message","Successfully logged into account")
                signin.destroy()
                loginin(a)
            else:
                messagebox.showerror("Notice","Your password or username is not entered correctly")
                
        elif a=="" and b=="":
            messagebox.showerror("Notice","You have not entered a username or password")



    button3=Button(signin,text="SIGN IN",font=("Calibre",12,"bold"),fg="indian red",command=checklogin)
    button3.grid(row=4,column=1,sticky="w")


#Sign up function
def signupfunc():
    global signup,login
    
    signup=Tk()
    signup.geometry("310x160")
    signup.title("SIGNUP SCREEN")
    
    sign=Label(signup,text="SIGN UP",font=("Verdana",13,"bold"),fg="steel blue").grid(row=0,column=1,sticky="w")


    name=Label(signup,text="Enter username : ",font=("Verdana",10),fg="steel blue").grid(row=1,column=0)
    user_signup=Entry(signup)
    user_signup.grid(row=1,column=1)

    pswd=Label(signup,text="Enter password : ",font=("Verdana",10),fg="steel blue").grid(row=2,column=0)
    password_signup=Entry(signup,show='*')
    password_signup.grid(row=2,column=1)

    cpswd=Label(signup,text="Confirm password : ",font=("Verdana",10),fg="steel blue").grid(row=3,column=0)
    cpass_signup=Entry(signup,show="*")
    cpass_signup.grid(row=3,column=1)
    
    empty=Label(signup,text="").grid(row=4,column=0)
   
    #Adding account to SQL
    def uploadsignup():
        A=user_signup.get()
        B=password_signup.get()
        C=cpass_signup.get()
        
        if B==C and C!=None and A!=None:
            cur.execute("select * from login where username='"+A+"'")
            d=cur.fetchall()

            if len(d)==0:
                messagebox.showinfo("Message","Successfully created an account. Please proceed to Login")
                cur.execute("insert into login values('"+ A +"','"+ B +"')")
                c.commit()
                signup.destroy()
            else:
                messagebox.showerror("Notice","This Username already exists")

        else:
            messagebox.showerror("Notice","Your password or username is not entered correctly")
    
    button3=Button(signup,text="SIGN UP",font=("Calibre",12,"bold"),fg="steel blue",command=uploadsignup)
    button3.grid(row=5,column=1,sticky="w")

# Final buttons performing given functions
button1=Button(login,text=" LOGIN  ",font=("Calibre",12,"bold"),fg="blue",command=signinfunc).pack(pady=22)
button2=Button(login,text="SIGNUP",font=("Calibre",12,"bold"),fg="green",command=signupfunc).pack(pady=4)
button3=Button(login,text="DELETE ACCOUNT",font=("Calibre",12,"bold"),fg="red",command=deleteaccfn).pack(pady=15)


#Information Options :  Graph Reports or Income or Expense Data or Logout
def loginin(mainname_1):
    global signin,signup,login
    root=Toplevel()
    root.geometry('450x100')
    root.title("Buckstracker")
    label=Label(root,text="Buckstracker",anchor=CENTER,font=("Calibre",15,"bold"),fg="magenta3").grid(row=0,column=2)


    b1=Button(root,text="Income",anchor=CENTER,font=("Calibre",12,"bold"),fg="green",command= lambda: Income_Tree(mainname_1))
    b1.grid(row=1,column=1)
    b2=Button(root,text="Expense",anchor=CENTER,font=("Calibre",12,"bold"),fg="red",command= lambda: Expense_Tree(mainname_1))
    b2.grid(row=1,column=2)
    b3=Button(root,text="Graph Reports",anchor=CENTER,font=("Calibre",12,"bold"),fg="blue",command= lambda : graphreports(mainname_1))
    b3.grid(row=1,column=3)

    
    def logout(root,win):
        root.destroy()
        # function to logout and open Buckstracker Login window if it had been closed previously
        if win.state()!="normal":
            loginwindow()
            
    Label_Space=Label(root,text="      ")
    Label_Space.grid(row=1,column=4)

    b4=Button(root,text="LOGOUT",anchor=CENTER,font=("Calibre",12,"bold"),fg="navy",command= lambda: logout(root,login))
    b4.grid(row=1,column=5)

    root.mainloop()

login.mainloop()




    
    

    

