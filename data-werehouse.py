import psycopg2
import time
from plyer import notification
from datetime import date
#establishing the connection
conn = psycopg2.connect(
   database="myDB", user='postgres', password='123456', host='127.0.0.1', port= '5432'
)
cursor = conn.cursor()
adminLoginCount = 0
noOfAttemptsToLogin = 3


def openAdminPage():
    print("Welcome Admin")
    print("Press 1 for create tables \n"+"Press 2 for Delete records\n"+"Press 3 for truncate all User tables\n"+"Press 4 to Publish Result")
    choice = input()
    if choice == '1':
        isTableExists = """SELECT EXISTS (
                                   SELECT FROM pg_tables
                                   WHERE  schemaname = 'public'
                                   AND    tablename  = 'gen_details'
                                   );"""
        cursor.execute(isTableExists)
        data = cursor.fetchone()
        print(data[0])
        if data[0] == False:
            create_gen = "create table gen_details(sid bigserial,name text,dept text);"
            cursor.execute(create_gen)
            create_stu = "create table student(marks real[],total real,percentage real,status text, date_of_exam date) inherits(gen_details);"
            cursor.execute(create_stu);
            create_res = "create table result(sid bigserial,name text,percentage real,status text, date_of_exam date);"
            cursor.execute(create_res);
            conn.commit()
        else:
            print("\nTable already created, Returning ...\n")
    elif choice == '2':
        idd = input('Enter sid')
        delete_query = "delete from student where sid = {}".format(idd)
        # isPresent = "select exists(select 1 from student where sid = {})".format(idd)
        # data = cursor.execute(isPresent)
        # print(data)
        cursor.execute(delete_query)
        notification.notify(title = "Row Removed",message="1 row deleted by Admin" ,timeout=2)
        time.sleep(2)
        conn.commit()
        
    elif choice == '3':
        truncate_query_stu = "TRUNCATE TABLE student;"
        cursor.execute(truncate_query_stu)
        conn.commit()
        truncate_query_gen = "TRUNCATE TABLE gen_details;"
        cursor.execute(truncate_query_gen)
        conn.commit()
        
    elif choice == '4':
        bulkInsert = "insert into result (sid,name,percentage,status,date_of_exam) select sid, name,percentage,status, date_of_exam from student;"
        cursor.execute(bulkInsert)
        conn.commit()
        notification.notify(title = "Result Published",message="Result has been published" ,timeout=2)
        time.sleep(2)
 
 def openStudentPage():
    print("prees I for insert\n"+"Press U for update records\n"+"Press R to see result")
    choice = input()
    if choice.upper() == "I":
        idd = int(input('Enter Id'))
        name = input('Enter Name: ')
        dept = input('Enter Department: ')
        n = int(input('Enter no of subject'))
        lis = []
        total = 0
        print("Enter",n,"subject marks")
        for i in range(n):
            marks = float(input())
            total+=marks
            lis.append(marks)
        insertQuery = "insert into student values({},'{}','{}','".format(idd,name,dept)
        percentage = total/n
        status = ""
        if(percentage>40):
            status = "Pass"
        else:
            status = "Fail"
        marksString = "{"
        for i in range(n):
            marksString +="{},".format(str(lis[i]))
        marksString = marksString[:-1]
        marksString += "}',"
        
        insertQuery+=marksString
        insertQuery += "{},{},'{}','{}');".format(total,percentage,status,date.today())
        print(insertQuery)
        cursor.execute(insertQuery)
        conn.commit()
        notification.notify(title = "Row Inserted",message="1 row affected" ,timeout=2)
        time.sleep(5)
        
    if choice.upper() == 'U':
        idd = int(input('Enter Id'))
        newName = input("Enter Name")
        updateQuery = "update student set name = '{}' where sid = {};".format(newName,idd)
        cursor.execute(updateQuery)
        conn.commit()
        notification.notify(title = "Row Updated Successfully",message="1 row affected" ,timeout=2)
        time.sleep(5)
    if choice.upper() == 'R':
        resultQuery = "select *from result"
        cursor.execute(resultQuery)
        data = cursor.fetchall()
        print("sid      name      total       RESULT    Date of Exam")
        for row in data:
            print(row[0],'       ',row[1],'   ', row[2], '      ', row[3], '    ',row[4])
 
 #Main
 while(1):
    global adminLoginCount
    global noOfAttemptsToLogin
    print("Hi,There, Welcome to New Vision School\n"+"-----------------------------------\n"
          +"Prees A for Admin Access\n"
          +"Press S  for Student Access\n"+"Press Q for Exit\n")
    c = input()
    if(c.lower() == 'a'):
        print("You have ",noOfAttemptsToLogin-adminLoginCount,"attempts, login carefully:")
        if adminLoginCount == 3:
            print("You have entered Wrong Password for 3 times. Try after 2 minutes ..")
            noOfAttemptsToLogin = 3
            adminLoginCount = -1
            time.sleep(2*60)
        if adminLoginCount == 2:
            notification.notify(title = "Final Attempt",message="You have only 1 attempt left." ,timeout=2)
            time.sleep(5)
        aid = input("Enter admin ID:")
        pwd = input("Enter admin Password: ")
        query = """select * from admin"""
        cursor.execute(query)
        data = cursor.fetchone()
        #cursor.close()
        if(data[0] == aid and data[1] == pwd):
            noOfAttemptsToLogin = 3
            adminLoginCount = -1
            openAdminPage()
        else:
            print("\nYou are not an admin, Returning to main menu...\n")
        adminLoginCount+=1
    elif(c.lower() == 's'):
        noOfAttemptsToLogin = 3
        adminLoginCount = 0
        openStudentPage()
    elif(c.lower() == "q"):
        cursor.close()
        conn.close()
        print('Thank you, visit again')
        break
    else:
        continue
