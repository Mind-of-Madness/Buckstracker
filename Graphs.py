from tkinter import *
from tkinter import messagebox,ttk
from matplotlib import pyplot as plt
from pymysql import *
from random import *
from datetime import *

# Function for Checking the min value of categories in piechart
def explodepie(slices_1):
    cat_min=min(slices_1)
    ind_min=slices_1.index(cat_min)
    t=()
    for e in range(len(slices_1)):
        if e==ind_min:
            t=t+(0.1,)
        else:
            t=t+(0,)
    return t
# Main function for this module
def graphreports(name_1):
    global enter_year,enter_month,options,options_var,cursor,username,frame_window
    #enter_month,enter_year is user input of month,yr respectively
    #options is the different graphs
    # options_var is tkinter variable for Menu
    #frame_window is extra pop up frame to input yr and month

    username=name_1
    root=Tk()
    root.title("Graph Reports")
    root.geometry("500x250")

    conn=connect(host='localhost',user='root',passwd='mysql',database='buckstracker')
    cursor=conn.cursor()

    options=[
    'Expenditure in different categories of a month as Piechart(use when month has required data)',#Piechart
    'Expenditure in different categories of a year as Piechart' ,#Piechart
    'Income levels in a year as bar graph and line graph',#Bar graph or line graph
    'Frequency of Payment mode in a year as Pie chart', # Pie chart
    'Frequency payment mode in a month as Bar graph', # Horizontal Bar graph
    'Frequency of expenditure in a month over a year as Scatter Plot',#Scatter plot
    'Comparison of income and expenditure in a year over various months', # Bar graph
    ]

 # Inserting above details into tkinter window
    LABEL=Label(root,text="Enter the graph required from below")
    LABEL.pack()

    options_var=StringVar()

    graphopt_menu=OptionMenu(root,options_var,*options)
    graphopt_menu.config(width=200)
    graphopt_menu.pack()

 #This function is to display required month or year options depending upon selected graph option

    def otheropt(root_window,var_graphopt,conn_1,cursor_1,opt):
        global enter_month,enter_year,graphopt_menu,month_dropmenu,year_dropmenu,frame_window
 # var_graphopt is the Tkinter variable of Graph Option menu

        frame_window=Frame(root_window)
        frame_window.pack(pady=20)

        resp_1=var_graphopt.get()
        
        enter_month=IntVar()
        enter_year=IntVar()
        enter_month.set(0)
        enter_year.set(2010)

        e1=[no1 for no1 in range(1,13)]
        e2=[no2 for no2 in range(2010,2031)]

        label_1=Label(frame_window,text="Enter the month and year required ")
        label_2=Label(frame_window,text="Enter year required")

        month_dropmenu=OptionMenu(frame_window,enter_month,*e1)

        if resp_1==opt[0] or resp_1==opt[4]:
            month_dropmenu.pack()
            label_1.pack()
        else:
            label_2.pack()
        
        year_dropmenu=OptionMenu(frame_window,enter_year,*e2)
        year_dropmenu.pack()
        
     # Checking for availability of data
        
        s3=''
        try:
            cursor_1.execute("select year(date) from expenditure group by year(date) having count(*)>=10 ")
            conn_1.commit()
            yr=cursor_1.fetchall()
            for i in yr:
                s3+=str(i[0])+','
        except:
            pass
        if s3=='':
            s3="NONE"
        s1="Note that we have constructive data for year"
        s2=" so please choose accordingly"
        
        lab=Label(frame_window,text=s1+s3+s2)
        lab.pack()    

     # Function which displays graphs based on selected option

        def graph(opt,var_1,c,cur,name,window,enter_2,enter_1=0):
            # name is username, c is the mysql connection, cur is the cursor,var_1 is the graph options
            window.destroy()
            
            response_graphopt=var_1.get()
            month_input=enter_1.get()
            year_input=enter_2.get()

            # Expenditure in different categories of a month as Piechart
            if response_graphopt==opt[0]:

                slices=[]
                category=[]
                query= "select sum(cost),category from expenditure where month(date) = '"+ str(month_input)+"' and year(date) = '" + str(year_input) + "'and name= '" +name+ "'group by category , month(date)"
                cur.execute(query)
                c.commit()
                data=cur.fetchall()
                sum=0

                if data!=():
                    for i in data:
                        slices.append(i[0])
                        category.append(i[1])
                        sum+=i[0]
                
                    
                    finalcol=['blue','cyan','green','yellow','red','orange','brown','magenta','white']
                    finalexp=explodepie(slices)
                    # Creating Piechart

                    plt.pie(slices,labels=category,colors=finalcol,startangle=0,shadow=True,radius=1.0,autopct='%1.1f%%',explode=finalexp)    
                    plt.title("Expenditure over different categories over a month with total expenditure = "+str(sum))
                    plt.show()
                else:
                    messagebox.showerror("ERROR","There is no data in the given year/month")
            
            #Expenditure in different categories of a year as Piechart
            elif response_graphopt==opt[1]:
                
                slices=[]
                category=[]
                
                query="select sum(cost), category from expenditure where year(date) = '"+ str(year_input)+ "'and name = '"+name+"'group by category,year(date)"
                cur.execute(query)
                c.commit()
                data=cur.fetchall()
                sum=0
                
                if data!=():

                    for i in data:
                        slices.append(i[0])
                        category.append(i[1])
                        sum+=i[0]
                

                    finalcol=['blue','cyan','green','yellow','red','orange','brown','magenta','white']
                    finalexp=explodepie(slices)
                    plt.pie(slices,labels=category,colors=finalcol,startangle=0,shadow=True,radius=1.0,autopct='%1.1f%%',explode=finalexp)
                    
                    plt.title("Expenditure over different categories over a year with total expenditure= "+str(sum))
                    plt.show()
                    
                else:
                    messagebox.showerror("ERROR","There is no data in the given year/month")

            #Income levels in a year as bar graph and line graph
            elif response_graphopt==opt[2]:
                query="select sum(sal),month(date) from income where year(date)= '"+str(year_input)+ "' and name = '"+name+"' group by month(date) order by month(date)"
                cur.execute(query)
                c.commit()
                data=cur.fetchall()

                x=['January','February','March','April','May','June','July','August','September','October','November','December']
                sal=[]

                if data!=():
                    for i in data:
                        sal.append(i[0]) 

                    plt.bar(x,sal,color='green',label='Income per month')
                    plt.plot(x,sal,color='black',label='Income trend')
        
                    plt.legend()
                    plt.title("Monthly income of "+str(year_input))
                
                    powr= str(len(str(data[0][0]//10)))
                    plt.xlabel("Months")
                    plt.ylabel("Monthly income in the power of "+powr)
                    plt.show()
                else:
                    messagebox.showerror("ERROR","There is no data in the given year/month")

            #Frequency of Payment mode in a year as Pie chart
            elif response_graphopt==opt[3]:
                slices=[]
                category=[]
                
                query="select count(paymode),paymode from expenditure where year(date) = '"+ str(year_input) + "' and name = '" +name+ "'group by paymode,year(date)"
                cur.execute(query)
                c.commit()
                data=cur.fetchall()
                sum1=0
                
                for i in data:
                    slices.append(i[0])
                    category.append(i[1])
                    sum1+=i[0]
                
                if data!=():
                    finalcol=['blue','cyan','green','yellow','red','orange','brown','magenta','white']
                    finalexp=explodepie(slices)
                    plt.pie(slices,labels=category,colors=finalcol,startangle=0,shadow=True,radius=1.0,autopct='%1.1f%%',explode=finalexp)   

                    plt.title("Expenditure by payment modes over a year of total="+str(sum1))
                    plt.show()
                else:
                    messagebox.showerror("ERROR","There is no data in the given year/month")
            
            # Frequency payment mode in a month as Bar graph
            elif response_graphopt==opt[4]:
                l=['BHIM UPI','PayTM','Airtel Money','PhonePe','Samsung Pay','Cash','Credit Card',
                'Netbanking','Cheque']
                x=[]
                y=[]
                
                query="select count(paymode) , paymode from expenditure where month(date)= '" + str(month_input) + "' and year(date)= '" + str(year_input) + "' and name = '" +name+ "'group by paymode, month(date) order by paymode asc"
                cur.execute(query)
                c.commit()
                data=cur.fetchall()
                sum=0
                
                for i in data:
                    y.append(i[0])
                    x.append(i[1])
                    sum+=i[0]
                    
                if data!=():
                    plt.barh(x,y,color='red',label='Payment modes')

                    plt.xlabel('Payment Modes')
                    plt.ylabel('Number of times of usage')

                    plt.title("Frequency of diffent payment modes from total="+str(sum))
                    plt.show()

                else:
                    messagebox.showerror("ERROR","There is no data in the given year/month")
            
            #Variation of frequency of expenditure in a month over a year as Scatter Plot
            elif response_graphopt==opt[5]:
                query="select sum(cost),week(date),month(date), category from expenditure where year(date)='" +str(year_input)+ "' and name = '" +name+ "' group by category,month(date),week(date);"
                cur.execute(query)
                c.commit()

                d1=cur.fetchall()
                
                cat1x=[]
                cat1y=[]
            
                cat2x=[]
                cat2y=[]

                cat3x=[]
                cat3y=[]

                cat4x=[]
                cat4y=[]

                cat5x=[]
                cat5y=[]

                cat6x=[]
                cat6y=[]
                sum=0

                for i in d1:
                    sum=sum+i[0]
                    date_2=date(int(year_input),int(i[2]),1) 
                    # Calculating week no of 1st of every month in Python
                    w1=date.isocalendar(date_2)      
                    # Calculating week no from beginning of month to check variation of payment in a month Since mysql counts weeks bit differently must add 2
                    week=int(i[1])-w1[1]+2
                    
                    if week==6:
                        week=5
                    
                    if i[3].lower()=='Provisions'.lower():
                        cat1x.append(week)
                        cat1y.append(i[0])

                    elif i[3].lower()=='Medicine'.lower():
                        cat2x.append(week)
                        cat2y.append(i[0])

                    elif i[3].lower()=='Taxes'.lower():
                        cat3x.append(week)
                        cat3y.append(i[0])

                    elif i[3].lower()=='Travel'.lower():
                        cat4x.append(week)
                        cat4y.append(i[0])

                    elif i[3].lower()=='Education'.lower():
                        cat5x.append(week)
                        cat5y.append(i[0])

                    elif i[3].lower()=='Miscellaneous'.lower():
                        cat6x.append(week)
                        cat6y.append(i[0])

                if d1!=():

                    plt.title("Frequency of expenditure in a category per week of total="+str(sum))

                    plt.scatter(cat1x,cat1y,label="Provisions",color='green')
                    plt.scatter(cat2x,cat2y,label="Medicine",color='cyan')
                    plt.scatter(cat3x,cat3y,label="Taxes",color='red')
                    plt.scatter(cat4x,cat4y,label="Travel",color='blue')
                    plt.scatter(cat5x,cat5y,label="Education",color='black')
                    plt.scatter(cat6x,cat6y,label="Miscellaneous",color='orange')

                    plt.legend()
                    plt.xlabel("Weeks of Month")
                    plt.ylabel("Expenditure in Rupees")

                    plt.show()

                else:
                    messagebox.showerror("ERROR","There is no data in the given year/month")

            #Comparison of income and expenditure in a year over various months()
            elif response_graphopt==opt[6]:
                query1= "select sum(sal),month(date) from income where year(date)='" +str(year_input)+ "' and name = '" +name+ "' group by month(date)"
                query2="select sum(cost),month(date) from expenditure where year(date)='" +str(year_input)+ "' and name = '" +name+ "' group by month(date)"
                
                cur.execute(query1)
                c.commit()
                data1=cur.fetchall()

                cur.execute(query2)
                c.commit()
                data2=cur.fetchall()

                x_axis=[]
                y_axis1=[]
                y_axis2=[]
                sum1=sum2=0
                
                if data1!=() and data2!=():

                    for i in data1:
                        x_axis.append(i[1])
                        y_axis1.append(i[0])
                        sum1+=i[0]

                    for j in data2:
                        y_axis2.append(j[0])
                        sum2+=j[0]


                    plt.bar(x_axis,y_axis1,color='red',label='Income in month of total ='+str(sum1))
                    plt.bar(x_axis,y_axis2,color='blue',label='Expenditure in month of total ='+str(sum2))

                    plt.title("Income and expenditure comparison")

                    plt.legend()
                    plt.xlabel("Month No")
                    plt.ylabel("Money in Rupees")

                    plt.show()
                else:
                    messagebox.showerror("ERROR","There is no data in the given year/month")
                    
        submit_b1=Button(frame_window,text='Submit',command= lambda: graph(options,var_graphopt,conn,cursor,username,frame_window,enter_year,enter_month) )
        submit_b1.pack()
   

    submit_b2=Button(root,text="Submit option",command= lambda: otheropt(root,options_var,conn,cursor,options))
    submit_b2.pack()
    
    root.mainloop()

#graphreports("Deepak")

