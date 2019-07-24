from datetime import date
import calendar
import glob
import shutil
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def fetchRecipents():
    recipents_email = []
    with open('PATH_TO_RECIPENTS_FILE_TO_FETCH_BCC_EMAILS/recipents.txt') as input_file:
        for line in input_file:
            data = line.split(',')
            recipents_email = data
    return recipents_email

def sendEmail(ImgFileName,bccEmails):
    #Lets fetch the image from the temp folder
    temp_content = glob.glob("PATH_TO_IMAGES_FOLDER/*.jpeg")
    selected_image_path = temp_content[0]
    
    msg = MIMEMultipart()
    bcc = bccEmails
    fromaddr = 'PLEASE ENTER FROM ADDRESS HERE'
    msg['subject'] = "Good Morning Greeting"

    text = MIMEText('Hi, <br>Hope you are doing great.<br>This will be the last message for the day.<br><img src="cid:image1"><br> <br><br>Happy Coding!','html')
    msg.attach(text)
    
    img_data = open(selected_image_path, 'rb')
    image = MIMEImage(img_data.read())
    img_data.close()
    image.add_header('Content-ID', '<image1>')
    msg.attach(image)
    

    SENDER_EMAIL = 'PLEASE ENTER YOUR GMAIL ID HERE'
    SENDER_PASSWORD = 'PLEASE ENTER YOUR GMAIL PASSWORD HERE'

    s = smtplib.SMTP('smtp.gmail.com',587) #We are using GMAIL as our email client.
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(SENDER_EMAIL, SENDER_PASSWORD)
    s.sendmail(fromaddr, bcc, msg.as_string())
    
    #lets delete the file from the temp folder completely
    files = glob.glob('/temp/*')
    for f in files:
        os.remove(f)
    s.quit()

def prepareData():
    print("I am ready to send email")
    greetings_content = glob.glob("PATH_TO_IMAGES_FOLDER/*.jpeg")
    selected_image_path = greetings_content[0]
    image_name = os.path.basename(selected_image_path)
    #move the selected file to temp folder.
    shutil.move(selected_image_path,'/temp/'+image_name)

    #Lets fetch the recipents from the file.
    emailData = fetchRecipents()

    #Now lets call the sendEmail()
    sendEmail(image_name,emailData)

#Get today's Day Value in English
my_date = date.today()
todays_day = calendar.day_name[my_date.weekday()]

if todays_day == 'Sunday' or todays_day == 'Saturday':
    print("No Need to Send Greetings Today!")
else:
    prepareData()


