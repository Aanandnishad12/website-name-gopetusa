
from bs4 import BeautifulSoup 
import re
import time
import requests
import sys
from time import sleep
import mysql.connector
import json
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Anishad@123",
  database="abc"
)
mycursor = mydb.cursor()
mycursor.execute("""CREATE TABLE if not exists `gopet_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(250) NOT NULL,
  `product_url` varchar(250) NOT NULL,
  `processed` int NOT NULL DEFAULT '0',
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1""")
def anand():
  headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}   
  response = requests.get('https://www.gopetusa.com/treadwheels/', headers = headers)
  # print(response)
  html = response.content
  soup = BeautifulSoup(html,'lxml')
  #print(soup)
  data_val= soup.find('div',attrs = {'class':'menu_wrapper'})
  item=data_val.find('li',attrs = {'id':'menu-item-12'})

  ul_tag=item.find_all('li')
  for li in ul_tag:
      cat1=li.text
      #print(cat1)
      if 'Dog Sizing' in cat1:
          break 
      link_val=li.find('a')
      link=link_val.get('href')
      #print(link)
      response2 = requests.get(link, headers = headers)
    #   print(response2)
      html2 = response2.content
      soup2 = BeautifulSoup(html2,'lxml')
      pro_main = soup2.find_all('div',attrs = {'class':'products_wrapper isotope_wrapper'})
      for main in pro_main:
          pro_tag=main.find_all('ul',attrs = {'class':'products'})
          for tag in pro_tag:
              pro_li=tag.find_all('li')
              for pro in pro_li:
                  a_tag_val=pro.find('a')
                  link=a_tag_val.get('href')
                #   print(link)
                  mycursor = mydb.cursor()
                  mycursor.execute("select id from gopet_categories where `product_url`=%s ",(link,))
                  result = mycursor.fetchall()
                #   print(result)
                  if result==[]:
                      mycursor = mydb.cursor()
                      #val=list(zip((cat1,),(link,)))
                      #print(val)
                      sql = "insert into gopet_categories(`category`,`product_url`) values ('"+cat1+"','"+link+"')" 
                    #   print(sql)
                      mycursor.execute(sql) 
                      mydb.commit()
def send_mail(s):
    fromaddr = "anandn@fcsus.com"
    toaddr = "nishadaman4438@gmail.com"
    msg = MIMEMultipart()
    # storing the senders email address  
    msg['From'] = fromaddr
    # storing the receivers email address 
    msg['To'] = toaddr
    # storing the subject 
    msg['Subject'] = "gopet catgory "
    # string to store the body of the mail
    body = s
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent 
    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()  
    # Authentication(password)
    s.login(fromaddr, 'Aman@123')
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

def main():
    try:
        anand()
        s = "Script Executed Successfully "
        # mail_send(s)
        print(s)

    except:
        s = "Script Executed Unsuccessfully "
        print(s)
    

if __name__ == "__main__":
    main()