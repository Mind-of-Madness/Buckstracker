from tkinter import *
from tkinter import ttk
import mysql.connector as m
from tkinter import messagebox
from tkinter import ttk

conn=m.connect(host="localhost",user="root",passwd="mysql",database="buckstracker")
cur=conn.cursor()


Tree1_count=0
Tree2_count=0

def Income_Tree(Tree1_Username):
    #Income Tree
    Tree1=Tk()
    Tree1.title("Income Tree View")
    Tree1.geometry("720x675")

    #Tree view Scroll frame
    Tree1_ScrollFrame=Frame(Tree1)
    Tree1_ScrollFrame.pack(pady=20)

    #Tree View Scrollbar
    Tree1_Scroll=Scrollbar(Tree1_ScrollFrame)
    Tree1_Scroll.pack(side=RIGHT,fill=Y)
    inc_tree=ttk.Treeview(Tree1_ScrollFrame,yscrollcommand=Tree1_Scroll.set,selectmode="browse")
    Tree1_Scroll.config(command=inc_tree.yview)


    inc_tree['columns']=("SNo","Date","Name","Salary","Notes")

    #Column formating 
    inc_tree.column("#0",width=0,stretch=NO)
    inc_tree.column("SNo",anchor=CENTER,width=35,minwidth=20)
    inc_tree.column("Date",anchor=W,width=120,minwidth=20)
    inc_tree.column("Name",anchor=W,width=120,minwidth=20)
    inc_tree.column("Salary",anchor=W,width=120,minwidth=20)
    inc_tree.column("Notes",anchor=W,width=120,minwidth=20)
        
    #Column Headings
    inc_tree.heading("#0",text="", anchor=W)
    inc_tree.heading("SNo",text="SNo", anchor=CENTER)
    inc_tree.heading("Date",text="Date of Income(YYYY-MM-DD)", anchor=W)
    inc_tree.heading("Name",text="Name", anchor=W)
    inc_tree.heading("Salary",text="Salary", anchor=W)
    inc_tree.heading("Notes",text="Extra Info", anchor=W)

    
    inc_tree.pack()

    #Frame Creation MAIN PART 
    Tree1_frame = Frame(Tree1)
    Tree1_frame.pack(pady=20)

    #Labels
    
    Tree1_l0=Label(Tree1_frame,text="SNo")
    Tree1_l0.grid(row=0,column=0)


    Tree1_l1=Label(Tree1_frame,text="Date of Income(YYYY-MM-DD)")
    Tree1_l1.grid(row=0,column=1)

    Tree1_l2=Label(Tree1_frame,text="Name")
    Tree1_l2.grid(row=0,column=2)

    Tree1_l3=Label(Tree1_frame,text="Salary")
    Tree1_l3.grid(row=0,column=3)

    Tree1_l4=Label(Tree1_frame,text="Extra Info")
    Tree1_l4.grid(row=0,column=4)

    #Entry Box

    
    
    Tree1_e1=Entry(Tree1_frame)
    Tree1_e1.grid(row=1,column=1)

    Tree1_e2=Label(Tree1_frame,text=Tree1_Username)
    Tree1_e2.grid(row=1,column=2)

    Tree1_e3=Entry(Tree1_frame)
    Tree1_e3.grid(row=1,column=3)

    Tree1_e4=Entry(Tree1_frame)
    Tree1_e4.grid(row=1,column=4)


    #Showing Records
    def Tree1_Show():
        global Tree1_count
        cur.execute("select * from income where name='"+Tree1_Username+"'")
    
        Tree1_data=cur.fetchall()

        for x in Tree1_data:
            inc_tree.insert(parent='',index='end',iid=Tree1_count,text="",values=(x[0],x[1],x[2],x[3],x[4]))
            Tree1_count+=1
           
        
    Tree1_b5=Button(Tree1,text="Show existing table",command=Tree1_Show)
    Tree1_b5.pack(pady=10)

    #Showing SNo Req
    def Tree1_show_sno():
        global Tree1_sno,Tree1_f0
        Tree1_f0=Frame(Tree1_frame)
        Tree1_f0.grid(row=1,column=0)
        q_sno="select max(sno)+1 from income"
        cur.execute(q_sno)
        sno=cur.fetchall()
        Tree1_sno=str(sno[0][0])
        sno_Label=Label(Tree1_f0,text=Tree1_sno).pack()

        

    Tree1_b1_1=Button(Tree1,text="Display SNo for new record",command=Tree1_show_sno)
    Tree1_b1_1.pack(pady=20)

    #Adding record
    def add_Tree1():
        global Tree1_count
        
        Tree1_q2="insert into income values('"+Tree1_sno+"','"+Tree1_e1.get()+"','"+Tree1_Username+"','"+Tree1_e3.get()+"','"+Tree1_e4.get()+"')"
        cur.execute(Tree1_q2)
        conn.commit()
        inc_tree.insert(parent='',index='end',iid=Tree1_count,text="",values=(int(Tree1_sno),Tree1_e1.get(),Tree1_Username,Tree1_e3.get(),Tree1_e4.get()))
        Tree1_count+=1

       
        #Clearing data in the box and in frame Tree1_f0
        
        Tree1_e1.delete(0,END)
        Tree1_e3.delete(0,END)
        Tree1_e4.delete(0,END)
        Tree1_f0.destroy()

    Tree1_b1=Button(Tree1,text="Add record",command=add_Tree1)
    Tree1_b1.pack(pady=20)

    #Select Record
    def select_Tree1():

        #Clear entry boxes
        Tree1_e1.delete(0,END)
        Tree1_e3.delete(0,END)
        Tree1_e4.delete(0,END)

        #Getting Record Number
        Tree1_selected=inc_tree.focus()

        #Getting the values
        Tree1_values=inc_tree.item(Tree1_selected,'values')

        #Output to Entry boxes
        Tree1_e1.insert(0,Tree1_values[1])
        Tree1_e3.insert(0,Tree1_values[3])
        Tree1_e4.insert(0,Tree1_values[4])


    Tree1_b2=Button(Tree1,text="Select a record",command=select_Tree1)
    Tree1_b2.pack(pady=10)

    #Update Record
    def update_Tree1():

        
        #Getting Record Number
        Tree1_selected=inc_tree.focus()

        #Getting the values
        Tree1_values=inc_tree.item(Tree1_selected,'values')

        #Save the item    
        Tree1_q5="update income set Sno='"+Tree1_values[0]+"', date='"+Tree1_e1.get()+"', name = '"+Tree1_Username+"', sal='"+Tree1_e3.get()+"',notes='"+Tree1_e4.get()+"'where sno='"+Tree1_values[0]+"'"
        cur.execute(Tree1_q5)
        conn.commit()
        inc_tree.item(Tree1_selected,text='',values=(Tree1_values[0],Tree1_e1.get(),Tree1_Username,Tree1_e3.get(),Tree1_e4.get()))

        #Clear entry boxes
        Tree1_e1.delete(0,END)
        Tree1_e3.delete(0,END)
        Tree1_e4.delete(0,END)

    Tree1_b3=Button(Tree1,text="Update record",command=update_Tree1)
    Tree1_b3.pack(pady=10)

    #Remove 1 record
    def remove1_Tree1():

        #Getting Record Number
        Tree1_selected=inc_tree.focus()

        #Getting the values
        Tree1_values=inc_tree.item(Tree1_selected,'values')

        
        # Deletion in SQL
        Tree1_q3="delete from income where sno='"+Tree1_values[0]+"'"
        cur.execute(Tree1_q3)
        conn.commit()

        Tree1_q4="update income set sno=sno-1 where sno>= '"+Tree1_values[0]+"'"
        cur.execute(Tree1_q4)
        conn.commit()

        Tree1_d1=inc_tree.selection()
        inc_tree.delete(Tree1_d1)

        messagebox.showinfo("Refrsh","Refreshing data in the viewing table")

        for record in inc_tree.get_children():
            inc_tree.delete(record)

        Tree1_Show()


    Tree1_b4=Button(Tree1,text="Remove selected record",command=remove1_Tree1)
    Tree1_b4.pack(pady=10)

    Tree1.mainloop()





def Expense_Tree(Tree2_Username):

    #Expense Tree

    Tree2=Tk()
    Tree2.title("Expense Tree View")
    Tree2.geometry("975x675")

    #Tree view Scroll frame
    Tree2_ScrollFrame=Frame(Tree2)
    Tree2_ScrollFrame.pack(pady=20)

    #Tree View Scrollbar
    Tree2_Scroll=Scrollbar(Tree2_ScrollFrame)
    Tree2_Scroll.pack(side=RIGHT,fill=Y)
    exp_tree=ttk.Treeview(Tree2_ScrollFrame,yscrollcommand=Tree2_Scroll.set,selectmode="browse")
    Tree2_Scroll.config(command=exp_tree.yview)

    #Column Variables Required
    exp_tree['columns']=("SNo","Date","Name","Category","Payment Mode","Cost","Notes")

    #Column formating 
    exp_tree.column("#0",width=0,stretch=NO)
    exp_tree.column("SNo",anchor=CENTER,width=35,minwidth=20)
    exp_tree.column("Date",anchor=W,width=120,minwidth=20)
    exp_tree.column("Name",anchor=W,width=120,minwidth=20)
    exp_tree.column("Category",anchor=W,width=120,minwidth=20)
    exp_tree.column("Payment Mode",anchor=W,width=120,minwidth=20)
    exp_tree.column("Cost",anchor=W,width=120,minwidth=20)
    exp_tree.column("Notes",anchor=W,width=120,minwidth=20)
        
    #Column Headings
    exp_tree.heading("#0",text="", anchor=W)
    exp_tree.heading("SNo",text="SNo", anchor=CENTER)
    exp_tree.heading("Date",text="Date of Exp(YYYY-MM-DD)", anchor=W)
    exp_tree.heading("Name",text="Name", anchor=W)
    exp_tree.heading("Category",text="Category", anchor=W)
    exp_tree.heading("Payment Mode",text="Payment Mode", anchor=W)
    exp_tree.heading("Cost",text="Cost",anchor=W)
    exp_tree.heading("Notes",text="Extra Info", anchor=W)


    exp_tree.pack()

    #Frame Creation MAIN PART
    Tree2_frame = Frame(Tree2)
    Tree2_frame.pack(pady=20)

    #Labels

    Tree2_l0=Label(Tree2_frame,text="SNo")
    Tree2_l0.grid(row=0,column=0)


    Tree2_l1=Label(Tree2_frame,text="Date of Exp(YYYY-MM-DD)")
    Tree2_l1.grid(row=0,column=1)

    Tree2_l2=Label(Tree2_frame,text="Name")
    Tree2_l2.grid(row=0,column=2)

    Tree2_l3=Label(Tree2_frame,text="Category")
    Tree2_l3.grid(row=0,column=3)

    Tree2_l4=Label(Tree2_frame,text="Payment Mode")
    Tree2_l4.grid(row=0,column=4)

    Tree2_l5=Label(Tree2_frame,text="Cost")
    Tree2_l5.grid(row=0,column=5)

    Tree2_l6=Label(Tree2_frame,text="Extra Info")
    Tree2_l6.grid(row=0,column=6)

    #Entry Box
    

    Tree2_e1=Entry(Tree2_frame)
    Tree2_e1.grid(row=1,column=1)

    Tree2_e2=Label(Tree2_frame,text=Tree2_Username)
    Tree2_e2.grid(row=1,column=2)

    
    Tree2_e3=StringVar()
    Tree2_e3.set("Select a category")
    Tree2_Option1=["Provisions","Medicine","Taxes","Travel","Education","Miscellaneous"]
    Tree2_Menu=OptionMenu(Tree2_frame,Tree2_e3,*Tree2_Option1)
    Tree2_Menu.grid(row=1,column=3)

    Tree2_e4=StringVar()
    Tree2_e4.set("Select payment mode")
    Tree2_Option2=['Cash','Credit Card','Netbanking','Cheque','BHIM UPI','PayTM','PhonePe','Samsung Pay','Airtel Money']
    Tree2_Menu=OptionMenu(Tree2_frame,Tree2_e4,*Tree2_Option2)

    Tree2_Menu.grid(row=1,column=4)

    Tree2_e5=Entry(Tree2_frame)
    Tree2_e5.grid(row=1,column=5)

    Tree2_e6=Entry(Tree2_frame)
    Tree2_e6.grid(row=1,column=6)

    #Showing Records
    def Tree2_Show():
        global Tree2_count
        cur.execute("select * from expenditure where name='"+Tree2_Username+"'")
    
        Tree2_data=cur.fetchall()

        for x in Tree2_data:
            exp_tree.insert(parent='',index='end',iid=Tree2_count,text="",values=(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
            Tree2_count+=1
           
        
    Tree2_b5=Button(Tree2,text="Show existing table",command=Tree2_Show)
    Tree2_b5.pack(pady=10)

    #Showing Req SNo
    def Tree2_show_sno():
        global Tree2_sno,Tree2_f0
        #Frame for Sno
        Tree2_f0=Frame(Tree2_frame)
        Tree2_f0.grid(row=1,column=0)
        q_sno="select max(sno)+1 from expenditure"
        cur.execute(q_sno)
        sno_2=cur.fetchall()
        Tree2_sno=str(sno_2[0][0])
        sno_Label=Label(Tree2_f0,text=Tree2_sno).pack()

        

    Tree2_b2_1=Button(Tree2,text="Display SNo for new record",command=Tree2_show_sno)
    Tree2_b2_1.pack(pady=20)

    #Adding record
    def add_Tree2():
        global Tree2_count
        
        Tree2_q2="insert into expenditure values('"+Tree2_sno+"','"+Tree2_e1.get()+"','"+Tree2_Username+"','"+Tree2_e3.get()+"','"+Tree2_e4.get()+"','"+Tree2_e5.get()+"','"+Tree2_e6.get()+"')"
        cur.execute(Tree2_q2)
        conn.commit()
        exp_tree.insert(parent='',index='end',iid=Tree2_count,text="",values=(Tree2_sno,Tree2_e1.get(),Tree2_Username,Tree2_e3.get(),Tree2_e4.get(),Tree2_e5.get(),Tree2_e6.get()))
        Tree2_count+=1

        Tree2_e1.delete(0,END)
        Tree2_e5.delete(0,END)
        Tree2_e6.delete(0,END)
        Tree2_f0.destroy()

    Tree2_b1=Button(Tree2,text="Add record",command=add_Tree2)
    Tree2_b1.pack(pady=20)

    #Select Record
    def select_Tree2():

        #Clear entry boxes
        Tree2_e1.delete(0,END)
        Tree2_e5.delete(0,END)
        Tree2_e6.delete(0,END)

        #Getting Record Number
        Tree2_selected=exp_tree.focus()

        #Getting the values
        Tree2_values=exp_tree.item(Tree2_selected,'values')

        #Output to Entry boxes
        Tree2_e1.insert(0,Tree2_values[1])
        Tree2_e3.set(Tree2_values[3])
        Tree2_e4.set(Tree2_values[4])
        Tree2_e5.insert(0,Tree2_values[5])
        Tree2_e6.insert(0,Tree2_values[6])


    Tree2_b2=Button(Tree2,text="Select a record",command=select_Tree2)
    Tree2_b2.pack(pady=10)

    #Update Record
    def update_Tree2():

        #Getting Record Number
        Tree2_selected=exp_tree.focus()

        #Getting the values
        Tree2_values=exp_tree.item(Tree2_selected,'values')

        Tree2_q5="update expenditure set Sno='"+Tree2_values[0]+"', date='"+Tree2_e1.get()+"', name='"+Tree2_Username+"', category='"+Tree2_e3.get()+"', paymode='"+Tree2_e4.get()+"', cost='"+Tree2_e5.get()+"', notes='"+Tree2_e6.get()+"'where sno='"+Tree2_values[0]+"'"
        cur.execute(Tree2_q5)
        conn.commit()
        exp_tree.item(Tree2_selected,text='',values=(Tree2_values[0],Tree2_e1.get(),Tree2_Username,Tree2_e3.get(),Tree2_e4.get(),Tree2_e5.get(),Tree2_e6.get()))

        #Clear entry boxes
        Tree2_e1.delete(0,END)
        Tree2_e5.delete(0,END)
        Tree2_e6.delete(0,END)
        

    Tree2_b3=Button(Tree2,text="Update record",command=update_Tree2)
    Tree2_b3.pack(pady=10)


    #Remove 1 record
    def remove1_Tree2():

        #Getting Record Number
        Tree2_selected=exp_tree.focus()

        #Getting the values
        Tree2_values=exp_tree.item(Tree2_selected,'values')


        Tree2_d1=exp_tree.selection()
        exp_tree.delete(Tree2_d1)

        # Deletion in SQL
        Tree2_q3="delete from expenditure where sno= '"+Tree2_values[0]+"'"
        cur.execute(Tree2_q3)
        conn.commit()

        Tree2_q4="update expenditure set sno=sno-1 where sno>= '"+Tree2_values[0]+"'"
        cur.execute(Tree2_q4)
        conn.commit()

        messagebox.showinfo("Refresh","Refreshing data of viewing Table")

        for record in exp_tree.get_children():
            exp_tree.delete(record)

        Tree2_Show()


    Tree2_b4=Button(Tree2,text="Remove selected record",command=remove1_Tree2)
    Tree2_b4.pack(pady=10)

    Tree2.mainloop()
#Income_Tree("Deepak")
#Expense_Tree("Karan")
