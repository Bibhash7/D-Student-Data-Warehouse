############   All Important Packages #############################################################

import os.path
import psycopg2
import time
from plyer import notification
from datetime import date
import cv2
import matplotlib.pyplot as plt
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

########### PostGres Connection and Global Variables ########################################

conn = psycopg2.connect(
   database="myDB", user='postgres', password='123456', host='127.0.0.1', port= '5432'
)
cursor = conn.cursor()
adminLoginCount = 0
noOfAttemptsToLogin = 3

################## ALL admin Operations ############################################################

def openAdminPage():
    print()
    print("Welcome Admin:")
    while(1):
        print()
        print("******************************************\n"
             +"* Press 1 for create tables              *\n"
             +"* Press 2 for Delete records             *\n"
             +"* Press 3 for truncate all User tables   *\n"
             +"* Press 4 to Publish Result              *\n"
             +"* Press 5 to exit                        *\n"
             +"******************************************\n")
        choice = input("Enter your Choice: ")
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
                notification.notify(title = "Table Created",message="Tables created by Admin" ,timeout=2)
                time.sleep(1)
            else:
                print("\nTable already created, Returning ...\n")
                
        elif choice == '2':
            idd = input('Enter sid: ')
            delete_query = "delete from student where sid = {}".format(idd)
            # isPresent = "select exists(select 1 from student where sid = {})".format(idd)
            # data = cursor.execute(isPresent)
            # print(data)
            cursor.execute(delete_query)
            conn.commit()
            notification.notify(title = "Row Removed",message="1 row deleted by Admin" ,timeout=2)
            time.sleep(1)
            

        elif choice == '3':
            truncate_query_stu = "TRUNCATE TABLE student;"
            cursor.execute(truncate_query_stu)
            conn.commit()
            truncate_query_gen = "TRUNCATE TABLE gen_details;"
            cursor.execute(truncate_query_gen)
            conn.commit()
            notification.notify(title = "User Tables Deleted",message="Tables are available for fresh Users" ,timeout=2)
            time.sleep(1)
            

        elif choice == '4':
            bulkInsert = "insert into result (sid,name,percentage,status,date_of_exam) select sid, name,percentage,status, date_of_exam from student;"
            cursor.execute(bulkInsert)
            conn.commit()
            notification.notify(title = "Result Published",message="Result has been published" ,timeout=2)
            time.sleep(1)
            
        elif choice == '5':
            notification.notify(title = "Logged Out",message="logout successfully" ,timeout=2)
            time.sleep(1)
            break

            
#################### Capture Image Through Camera #######################################  

def openCamera():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("test", frame)
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "C:/Users/Bibhash/PostGre/opencv_frame_{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            print("Image Clicked and Saved, Exiting ....")
            break

    cam.release()

    cv2.destroyAllWindows()

  
################################### Extract data from Image #####################################

def image2String(image = None):
    img = ""
    if image == None:
        img = cv2.imread('C:/Users/Bibhash/PostGre/opencv_frame_0.jpg')
    else:
        imgPath = "C:/Users/Bibhash/PostGre/"+image
        img = cv2.imread(imgPath)
            
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    plt.imshow(img,'gray')
    plt.show()
    bPix = img.max()
    sPix = img.min()
    low = (bPix+sPix)//2+20
    if bPix+10 < 255 and sPix < 255:
        bPix = bPix+10
    # print(bPix,sPix,low)
    ret,thresh = cv2.threshold(img,low,bPix,cv2.THRESH_BINARY_INV)
    blur = cv2.medianBlur(thresh,1)
    #cv2.imshow(blur,'gray')
    #cv2.imshow('image',blur)
    text = pytesseract.image_to_string(
        blur, config='-l eng --oem 1 --psm 4'
    )
    #print(text)
    text = text.split(" ")
    if text[0].strip().isalpha():
        print("Data Extracted from Image: ",text[0])
        print("No Worries. You can edit it, if not correct: ")
        return text[0]
    else:
        return None
 

######################### ALL Student Operations ####################################

def openStudentPage():
    print()
    print("Welcome New Member:")
    print()
    print("#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#\n"
         +"# prees I for Insert:              #\n"
         +"# Press U for Update records:      #\n"
         +"# Press R to View Result:          #\n"
         +"#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#\n"
         )
    choice = input("Enter your Choice: ")
    if choice.upper() == "I":
        idd = int(input('Enter Id: '))
        name = ""
        #name = input('Enter Name: ')
        print()
        print( "[ ----------------------------------------------------------------------  ]\n"
              +"[ Experiace AI:                                                           ]\n"
              +"[ Enter the Name through Image,(Experimental) or through Console:         ]\n"
              +"[ ----------------------------------------------------------------------  ]\n"
              +"[ Press I for Click Image (Press SPACEBAR for Capture, ESC for Exit):     ]\n"
              +"[ Press L for read Image from Local Storage:                              ]\n"
              +"[ Press any other for Console input:                                      ]\n"
              +"[ Note: For Local Storage file path must be C:/Users/Bibhash/PostGre/ :   ]\n"
              +"[ ----------------------------------------------------------------------  ]\n")
        choice = input("Enter your Choice: ")
        if choice.upper() == 'I':
            openCamera()
            name = image2String()
            if name == None:
                print("Image not extracted properly, Please, Input through Console: ")
                name = input("Enter Name: ")
            else:
                notification.notify(title = "Received Data",message="Data extracted through Image" ,timeout=2)
                time.sleep(1)
        elif choice.upper() == 'L':
            image = input("Enter Image name with proper extension: ")
            imgPath = "C:/Users/Bibhash/PostGre/"+image
            FilePresent = os.path.exists(imgPath)
            if(FilePresent):
                name = image2String(image)
            else:
                print("Image not found. Exiting...")
                name = None
            if name == None:
                print("Image not extracted properly, Please, Input through Console: ")
                name = input("Enter Name: ")
            else:
                notification.notify(title = "Received Data",message="Data extracted through Image" ,timeout=2)
                time.sleep(1)
        else:
            name = input("Enter Name: ")
            
            
        dept = input('Enter Department: ')
        n = int(input('Enter no of subject: '))
        lis = []
        total = 0
        print("Enter",n,"subject marks: ")
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
        #print(insertQuery)
        cursor.execute(insertQuery)
        conn.commit()
        notification.notify(title = "Row Inserted",message="1 row affected" ,timeout=2)
        time.sleep(1)
        
    if choice.upper() == 'U':
        idd = int(input('Enter Id: '))
        newName = input("Enter Name: ")
        updateQuery = "update student set name = '{}' where sid = {};".format(newName,idd)
        cursor.execute(updateQuery)
        conn.commit()
        notification.notify(title = "Row Updated Successfully",message="1 row affected" ,timeout=2)
        time.sleep(1)
    if choice.upper() == 'R':
        resultQuery = "select *from result"
        cursor.execute(resultQuery)
        data = cursor.fetchall()
        print()
        print("All Historic Results:   ")
        print("sid      name      total       RESULT    Date of Exam")
        for row in data:
            print(row[0],'       ',row[1],'   ', row[2], '      ', row[3], '    ',row[4])
        
 

################# Main Code ###############################################################

while(1):
    global adminLoginCount
    global noOfAttemptsToLogin
    print()
    print( "|---------------------------------------------------|\n"
          +"| Hi,There, Welcome to AI-Student Data Warehouse:   |\n"
          +"|---------------------------------------------------|\n"
          +"| Prees A for Admin Access:                         |\n"
          +"| Press S  for Student Access:                      |\n"
          +"| Press Q for Exit:                                 |\n"
          +"|---------------------------------------------------|\n")
    c = input("Enter your Choice: ")
    if(c.lower() == 'a'):
        print("\nYou have ",noOfAttemptsToLogin-adminLoginCount,"attempts, login carefully:\n")
        if adminLoginCount == 3:
            print()
            print("You have entered Wrong Password for 3 times. Try after 2 minutes ..")
            print()
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
