from bs4 import BeautifulSoup
import requests, urllib
import mysql.connector
import re
import time
import sys
import json
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import random
def mail_send(s):
    fromaddr = "anandn@fcsus.com"
    toaddr = "nishadaman4438@gmail.com"
    msg = MIMEMultipart()
    # storing the senders email address  
    msg['From'] = fromaddr
    # storing the receivers email address 
    msg['To'] = toaddr
    # storing the subject 
    msg['Subject'] = "gopet_op Differences between vnp & stock(qty) "
    # string to store the body of the mail
    body = s
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent 
    filename = "File_name_with_extension"
    attachment = open('./gopet_vnp.csv', "rb")
    
    parter1 = MIMEBase('application', 'octet-stream')
    parter1.set_payload((attachment).read())
    encoders.encode_base64(parter1)
    parter1.add_header('Content-Disposition', 'attachment', filename='gopet_vnp.csv')
    msg.attach(parter1)
    
    parter2 = MIMEBase('application', "octet-stream")
    parter2.set_payload(open('./gopet_stock.csv', "rb").read())
    encoders.encode_base64(parter2)
    parter2.add_header('Content-Disposition', 'attachment', filename='gopet_stock.csv')  
    msg.attach(parter2)

    parter3 = MIMEBase('application', "octet-stream")
    parter3.set_payload(open('./gopet_sku.csv', "rb").read())
    encoders.encode_base64(parter3)
    parter3.add_header('Content-Disposition', 'attachment', filename='gopet_sku.csv')  
    msg.attach(parter3)
    
    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()  
    # Authentication(password)
    s.login(fromaddr, 'Aman@123')
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
def anand():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Anishad@123",
        database="abc"
    )
    mycursor = mydb.cursor()
    mycursor.execute("""CREATE TABLE if not exists `gopet_op` (
        `id` int NOT NULL AUTO_INCREMENT,
        `Product_Title` mediumblob NOT NULL,
        `sku` varchar(200) NOT NULL,
        `parent_sku` varchar(200) DEFAULT NULL,
        `primary_sku` int DEFAULT '1',
        `UPC` varchar(15) DEFAULT NULL,
        `EAN` varchar(12) DEFAULT NULL,
        `LMP_SKU` varchar(200) DEFAULT NULL,
        `mfg_id` varchar(30) DEFAULT NULL,
        `FF_Latency` varchar(10) DEFAULT NULL,
        `Amazon_ASIN` varchar(10) DEFAULT NULL,
        `is_change` binary(1) DEFAULT NULL,
        `notions_unit_of_sale` int DEFAULT NULL,
        `previous_vnp` decimal(7,2) DEFAULT NULL,
        `fcsus_unit_of_sale` int DEFAULT NULL,
        `vnp` decimal(7,2) DEFAULT NULL,
        `inward_freight` decimal(7,2) DEFAULT '0.00',
        `Product_Net_Weight_Oz` decimal(7,2) DEFAULT NULL,
        `previous_shipping_weight` decimal(7,2) DEFAULT '0.00',
        `shipping_weight` decimal(7,2) DEFAULT NULL,
        `product_introduce_date` varchar(255) DEFAULT NULL,
        `length` decimal(7,2) DEFAULT NULL,
        `width` decimal(7,2) DEFAULT NULL,
        `height` decimal(7,2) DEFAULT NULL,
        `product_description` longblob,
        `additional_information` varchar(800) NOT NULL,
        `price_update_override` int DEFAULT '0',
        `wgt_update_override` int DEFAULT '0',
        `Minimum_Advertised_Price` decimal(7,2) DEFAULT NULL,
        `frt_collect` varchar(1) DEFAULT 'N',
        `image1` varchar(500) DEFAULT NULL,
        `image2` varchar(500) DEFAULT NULL,
        `image3` varchar(500) DEFAULT NULL,
        `image4` varchar(500) DEFAULT NULL,
        `image5` varchar(500) DEFAULT NULL,
        `previous_qty_avb` int DEFAULT '0',
        `qty_avb` int DEFAULT '0',
        `stock` int DEFAULT '0',
        `category` text,
        `Product_link` text,
        `discontinued` int DEFAULT '0',
        `last_updated` varchar(255) DEFAULT NULL,
        `doba_categories` varchar(255) DEFAULT NULL,
        `doba_allowed` int NOT NULL DEFAULT '1',
        KEY `id` (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1""")
    count=1

    new_prod = []
    mycursor = mydb.cursor()
    Query = ("select `id`,`category`,`product_url` from  `gopet_categories` where `processed` = 0 ")
    mycursor.execute(Query)
    records = mycursor.fetchall()
    if records != []:
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE `gopet_op`  SET previous_vnp = vnp")
        mycursor = mydb.cursor()
        mycursor.execute('UPDATE `gopet_op`  SET previous_qty_avb = qty_avb')
    for rows in records:
   
        category=rows[1]
        url=rows[2]
        # print(url)
        mycursor = mydb.cursor()
        query="UPDATE `gopet_categories` SET `processed` = '1' WHERE product_url = '"+url+"'"
        mycursor.execute(query)
        
        
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}   
        response = requests.get(url, headers = headers )
        html = response.text
        soup = BeautifulSoup(html,'lxml')
        #print(response)
        title=''
        title=soup.find('h1').text.lstrip().rstrip().replace('"','""').encode().decode('latin1').replace('Ã¢Â€Â²',"\\'").replace('Ã¢Â€Â³','\\"').replace('Ã¢Â€Â™',"\\'").replace('Ã¢Â€Â','\\"').replace('Ã¢Â€Â“','-').replace('â','-')
        #print(title)
        
        price=''
        price_val=soup.find_all('p',attrs = {'class':'price'})
        for val in price_val:
            price_data=val.text.lstrip().rstrip().replace('$','').replace(',','')
            decimal =re.findall("\d+\.\d+", price_data)
            price=str(decimal[-1])
            # print(price)
        sku_val=''
        sku_tag=soup.find('div',attrs = {'class':'product_meta'}).text.lstrip().rstrip()
        sku_val=sku_tag.replace('SKU:','')
        if sku_val=='':
            i=count
            c = 0
            while(i> 0):
                i = i // 10
                c = c + 1
                sku=('GP0100001'[:-c]+str(count)).replace(' ','').replace('-','')
            count+=1
        else:
            sku=('GP01'+sku_val).replace(' ','').replace('-','')
            
        if title=='' or price=='':
            discontinued='1'
        else:
            discontinued='0'
        image_tag=soup.find('div',attrs = {'class':'images'})
        img_tag=image_tag.find_all('a')
        for i in img_tag:
            img=i.get('href')
            #print(img)
        stock_data=''
        try:    
            stock_val=soup.find('div',attrs = {'class':'summary entry-summary column one-second'})
            stock_data=stock_val.find('p',attrs = {'class':'stock out-of-stock'}).text.lstrip().rstrip()
            # print(stock_data)
        except Exception as e:
            pass
            # print (e)
            
        if stock_data == 'Out of stock':
            stock='0'
        else:
            stock='5'
        desc=''
        try:
            desc_val=soup.find('div',attrs = {'id':'tab-description'})
            desc=desc_val.text.rstrip().lstrip().encode().decode('latin1').replace('Ã¢Â€Â²',"\\'").replace('Ã¢Â€Â³','\\"').replace('Ã¢Â€Â™',"\\'").replace('Ã¢Â€Â','\\"').replace('Ã¢Â€Âœ','\\"').replace('Ã¢Â€Â‹','').replace('â','')
        except Exception as e:
            pass
            # print (e)    
        # print(desc)
        #sys.exit(0)
        weight=''
        total_dimensions=''
        running_area=''
        unit_weight=''
        features=''
        shipping_dimensions=''
        warranty=''
        speed_range=''
        case_quantity=''
        door_dimensions=''
        opening_dimensions=''
        colors=''
        aDict = {}
        table=soup.find('div',attrs = {'id':'tab-additional_information'})
        try:
            tr_tag1=soup.find('tr',attrs = {'class':'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_max-weight'})
            weight=tr_tag1.find('td').text.replace('\n','').replace('\u2033','"').replace('\u2013','-')
            val=tr_tag1.find('th').text.replace('\n','')
            aDict[val] = weight
            
        except Exception as e:
            pass
            # print (e)
        try:
            tr_tag2=soup.find('tr',attrs = {'class':'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_running-area'})
            running_area=tr_tag2.find('td').text.replace('\n','').replace('\u2033','"').replace('\u2013','-')
            val=tr_tag2.find('th').text.replace('\n','')
            aDict[val] = running_area
        except Exception as e:
            pass
            # print (e)
        try:
            tr_tag3=soup.find('tr',attrs = {'class':'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_unit-weight'})
            unit_weight=tr_tag3.find('td').text.replace('\n','').replace('\u2033','"').replace('\u2013','-')
            val=tr_tag3.find('th').text.replace('\n','')
            aDict[val] = unit_weight
        except Exception as e:
            pass
            # print (e)
        try:
            tr_tag4 =soup.find('tr',attrs = {'class':'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_unit-total-dimensions'})
            total_dimensions= tr_tag4.find('td').text.replace('\n','').replace('\u2033','"').replace('\u2013','-')
            val=tr_tag4.find('th').text.replace('\n','')
            aDict[val] = total_dimensions
        except Exception as e:
            pass
            # print (e)
        try:
            tr_tag5=soup.find('tr',attrs = {'class':'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_features'})
            features=tr_tag5.find('td').text.replace('\n','').replace('\u2033','"').replace('\u2013','-')
            val=tr_tag5.find('th').text.replace('\n','')
            aDict[val] = features
        except Exception as e:
            pass
            # print (e)
        try:
            tr_tag6=soup.find('tr',attrs = {'class':'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_shipping-dimensions'})
            shipping_dimensions=tr_tag6.find('td').text.replace('\n','').replace('\u2033','"').replace('\u2013','-')
            val=tr_tag6.find('th').text.replace('\n','')
            aDict[val] = shipping_dimensions
        except Exception as e:
            pass
            # print (e)
        try:
            tr_tag7=soup.find('tr',attrs = {'class':'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_warranty'})
            warranty=tr_tag7.find('td').text.replace('\n','').replace('\u2033','"').replace('\u2013','-')
            val=tr_tag7.find('th').text.replace('\n','')
            aDict[val] = warranty
        except Exception as e:
            pass
            # print (e)
        try:
            tr_tag8=soup.find('tr',attrs = {'class':'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_speed-range'})
            speed_range=tr_tag8.find('td').text.replace('\n','').replace('\u2033','"').replace('\u2013','-')
            val=tr_tag8.find('th').text.replace('\n','')
            aDict[val] = speed_range
        except Exception as e:
            pass
            # print (e)
        try:
            tr_tag9=soup.find('tr',attrs = {'class':'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_case-quantity'})
            case_quantity=tr_tag9.find('td').text.replace('\n','').replace('\u2033','"').replace('\u2013','-')
            val=tr_tag9.find('th').text.replace('\n','')
            aDict[val] = case_quantity
        except Exception as e:
            pass
            # print (e)
        try:
            tr_tag10=soup.find('tr',attrs = {'class':'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_door-dimensions'})
            door_dimensions=tr_tag10.find('td').text.replace('\n','').replace('\u2033','"').replace('\u2013','-')
            val=tr_tag10.find('th').text.replace('\n','')
            aDict[val] = door_dimensions
        except Exception as e:
            pass
            # print (e)
        try:
            tr_tag11=soup.find('tr',attrs = {'class':'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_opening-dimensions'})
            opening_dimensions=tr_tag11.find('td').text.replace('\n','').replace('\u2033','"').replace('\u2013','-')
            val=tr_tag11.find('th').text.replace('\n','')
            aDict[val] = opening_dimensions
        except Exception as e:
            pass
            # print (e)
        try:
            tr_tag12=soup.find('tr',attrs = {'class':'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_colors'})
            colors=tr_tag12.find('td').text.replace('\n','').replace('\u2033','"').replace('\u2013','-')
            val=tr_tag12.find('th').text.replace('\n','')
            aDict[val] = colors
        except Exception as e:
            pass
            # print (e)
        json_object = json.dumps(aDict )
        # print(json_object) 

        myresult =''
        try:
            mycursor = mydb.cursor() 
            mycursor.execute("SELECT sku FROM `gopet_op` WHERE Product_link = '"+url+"'")
            myresult = mycursor.fetchall()
            # print(myresult)
        except Exception as e:
            pass
            # print (e)
        if myresult == []:
     
            mycursor = mydb.cursor() 
            mycursor = mydb.cursor()
            new_prod.append(sku)
            sql = "insert into `gopet_op`(`Product_Title`, `sku`, `parent_sku`,`vnp`,`product_description`,`additional_information`,`image1`,`stock`,`category`,`Product_link`,`discontinued`) values ('binary  "+(title)+"','"+sku+"','"+sku+"','"+price+"','binary  "+(desc)+"','"+json_object+"','"+img+"','"+stock+"','"+category+"','"+url+"','"+discontinued+"')" 
            # print(sql)
            # sys.exit(0)
            mycursor.execute(sql)
            mydb.commit()
        else:
            mycursor = mydb.cursor()
            mycursor.execute("UPDATE `gopet_op` SET `vnp`= '"+price+"',stock='"+stock+"' WHERE Product_link= '"+url+"'") 
            mydb.commit()
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE `gopet_op`  SET qty_avb = stock") 
    mydb.commit()

    mycursor = mydb.cursor()    
    mycursor.execute("select sku,vnp,previous_vnp,previous_qty_avb,qty_avb from gopet_op")
    result = mycursor.fetchall()
    with open('gopet_vnp.csv', 'w',  newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer = csv.DictWriter(outcsv, fieldnames = ["sku", "vnp", "previous_vnp"])
            writer.writeheader()
            
    with open('gopet_stock.csv', 'w',  newline='') as stcsv:
            writers = csv.writer(stcsv)
            writers = csv.DictWriter(stcsv, fieldnames = ["sku", "previous quantity", "quantity available"])
            writers.writeheader()
    with open('gopet_sku.csv', 'w',  newline='') as skucsv:
        writers = csv.writer(skucsv)
        writers = csv.DictWriter(skucsv, fieldnames = ["sku"])
        writers.writeheader()

    for x in result:
        sku=x[0]
        vnp= x[1]
        pvnp= x[2]
        pqty=x[3]
        qty=x[4]
        if vnp!=pvnp:
            # print(vnp)
            with open('gopet_vnp.csv', 'a', newline='') as vnpcsv:
                writer = csv.writer(vnpcsv)
                writer = csv.DictWriter(vnpcsv, fieldnames =[sku,vnp,pvnp])
                writer.writeheader()
        if pqty != qty:
            with open('gopet_stock.csv', 'a', newline='') as stockcsv:
                writers = csv.writer(stockcsv)
                writers = csv.DictWriter(stockcsv, fieldnames =[sku,pqty,qty])
                writers.writeheader()
    for i in new_prod:
        with open('gopet_sku.csv', 'a', newline='') as vnpcsv:
            writer = csv.writer(vnpcsv)
            writer = csv.DictWriter(vnpcsv, fieldnames =[i])
            writer.writeheader()

def main():
    try:
        anand()
        s = "Script Executed Successfully "
        mail_send(s)
        print(s)
    except:
        s = "Script Executed Unsuccessfully"
        print(s)

if __name__ == "__main__":
    main()
