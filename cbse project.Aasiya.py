import random
import sys
from datetime import *
import mysql.connector as sql
con=sql.connect(host='localhost',user='TP',password='17102005')
cursor=con.cursor()
cursor.execute("create database if not exists ebs")
con.commit()
cursor.close()
con.close()
con=sql.connect(host='localhost',user='TP',password='17102005',database='EBS')
if con.is_connected():
    print("successfully connected")
else:
    print('error')
cursor=con.cursor()
cursor.execute('create table if not exists sign_in(User_no VARCHAR(50) primary key, User_name VARCHAR(100) ,Password VARCHAR(100),Confirm_password VARCHAR(100))')
cursor.execute('create table if not exists acc_details(accountno bigint primary key,bankname VARCHAR(25),bankbranch VARCHAR(25),linked_name VARCHAR(25),address VARCHAR(100),areacode INT(6),phone_no INT(15),email VARCHAR(1000),boxid VARCHAR(25))')
cursor.execute('create table if not exists transaction(bank_acc_no bigint, unit INT(10),DAY VARCHAR(25),bill_amt INT(10),GST INT(10),totalamt INT(10))')

def func1():
    user_no=input("Enter your user number :")
    user_name=input("Enter your user name :")
    password=input("Enter your password:")
    confirm_password=input("Confirm your password:")
    if password==confirm_password:
        info1="insert into sign_in values('{}','{}','{}','{}')".format(user_no,user_name,password,confirm_password)
        cursor.execute(info1)
        con.commit()
        c=input("Do you want to continue?(yes or no)")
    else:
        print('your confirm password is incorrect')
        print('Try again')
        c=input("do you want to try again?(yes or no)")

def login():  # Log in the user
    user_no = input("Enter your username: ")
    password = input("Enter your password: ")
    cursor.execute("SELECT user_no, password FROM sign_in")
    rs = cursor.fetchall()

    if len(rs) == 0:
        sys.exit("Username doesn't exist!")
    while True:
        for i in rs:
            if i[0] == user_no and i[1] == password:               
                print("Login successful!")
                print("Hello,", user_no + "!" "\n")
                return True

            elif i[0] != user_no or i[1]  == password:
                sys.exit("Username or password is incorrect!")

            else:
                sys.exit("Unknown error occurred!")
        break
        
def func2():
    acc=input("ENTER YOUR ACCOUNT NUMBER:")
    use=input("ENTER YOUR USERNAME:")
    info6=cursor.execute("delete from transaction where bank_acc_no='{}'".format(acc))
    info7=cursor.execute("delete from acc_details where accountno='{}'".format(acc))
    info8=cursor.execute("delete from sign_in where user_name='{}'".format(use))
    cursor.execute(info6)
    con.commit()
    cursor.execute(info7)
    con.commit()
    cursor.execute(info8)
    con.commit()
    sys.exit("YOUR ACCOUNT IS SUCCESSFULLY DELETED")
  

def func3():
    accountno=6442837531
    print("your account no is : 644-283-753-1")
    boxid=input("Enter your meter box ID :")
    bankname=input('Enter your BANK NAME :')
    bankbranch=input('Enter your BANK BRANCH :')
    linked_name=input('Enter your linked name :')
    address=input('Enter your permanent address :')
    areacode=int(input('Enter your area PIN CODE  :'))
    phone_no=int(input('Enter your PHONE NUMBER  :'))
    email=input('Enter your valid email address :')
    info3="insert into acc_details values('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(accountno,bankname,bankbranch,linked_name,address,areacode,phone_no,email,boxid)
    cursor.execute(info3)
    con.commit()
 

def func4():
    accountno=int(input('Enter your account number :'))
    info4="select * from acc_details where accountno=" + str(accountno)
    cursor.execute(info4)
    data1=cursor.fetchall()
    for row in data1:
        print("Account Number: ", row[0])
        print("bankname:",row[1])
        print("bankbranch:",row[2])
        print("Linked name:",row[3])
        print("Your meter device ID=",row[8])
        print("Residential address:",row[4])
        print("area code:",row[5])
        print("phone number:",row[6])
        print("email:",row[7])
    info5="select * from Transaction where bank_acc_no=" + str(accountno)
    cursor.execute(info5)
    data2=cursor.fetchall()
    for row in data2:
        print("Unit : ",row[1])
        print("Paid on:",row[2])
        print("Amount to be paid without GST:",row[3])
        print("GST=",row[4])
        print("Amount to be paid including GST:",row[5])

while True:
    print('--------WELCOME TO ELECTRICITY BILLING SYSTEM !--------')
    print(datetime.now())
    print('1.NEW USER')
    print('2.EXISTING USER')
    print('3.EXIT')
    choice1=int(input('ENTER YOUR CHOICE:'))
    if choice1==1:
        func1()
    
    elif choice1==2:
        c = login()
        while c:
            print('----------WELCOME TO ELECTRICITY BILLING SYSTEM----------')
            print("1.ACCOUNT SETTINGS")
            print("2.TRANSACTION")
            print("3.VIEW CUSTOMER DETAILS")
            print('4.EXIT')
            choice=int(input('ENTER YOUR CHOICE:'))
            if choice==1:
                print('1.NEW CUSTOMER')
                print('2.DELETE EXISTING ACCOUNT')
                ch=int(input('ENTER YOUR CHOICE:'))
                while True:
                    if ch==1:
                        func3()
                        break

                    elif ch==2:
                        func2()
                 
            elif choice==2:
                accountno=int(input('Enter your account number :'))
                info10="select * from acc_details where accountno={}".format(accountno)
                cursor.execute(info10)
                data1=cursor.fetchall()
                for row in data1:
                    unit=random.randint(0,101)
                    print('Dear customer, you have used',unit,'units of electricity.')
                    print('One unit of current is AED 1')
                    amount=1*unit
                    today=date.today()
                    deadline=date(2022, 9, 30)
                    delay=(deadline - today).days
                    if int(delay) < 0:
                        fine=(int((today-deadline).days))*2
                        totamt=amount+fine
                        print('you have delayed for',int((today-deadline).days),'days.The fine per day is AED 2.')
                        GST=(10/100)*totamt
                        totalamt=totamt+GST
                        print('kindly pay AED',totalamt,' including GST')
                        p=input("Please Enter YES to transact: ")
                        if p.lower()=='yes':
                            print("Transaction successful")
                            print("You have paid the bill")
                        else:
                            print('Transaction incomplete/error')
                    else:
                        totamt=0
                        GST=(10/100)*amount
                        totalamt=amount+GST
                        print('kindly pay AED',totalamt,' including GST')
                        p=input("Please Enter YES to transact: ")
                        if p.upper()=="YES":
                            print("Transaction successful")
                            print("You have paid the bill")
                        else:
                            print('you have to pay the bill soon')
                    info3="insert into Transaction values('{}','{}','{}','{}','{}','{}')".format(accountno,unit,deadline,amount,GST,totalamt)
                    cursor.execute(info3)
                    con.commit()
                    V=input("do you want to continue?(yes or no)")
                    if V=='yes':
                        continue
                    else:
                        break
            elif choice==3:
                func4()
                V=input("do you want to continue?(yes or no)")
                if V=='yes':
                    continue
                else:
                    break
                  
            elif choice==4:
                sys.exit("THANK YOU FOR VISITING!")
                
    elif choice1==3:
        sys.exit("THANK YOU FOR VISITING!")
  
    else:
        sys.exit("Invalid Choice")
