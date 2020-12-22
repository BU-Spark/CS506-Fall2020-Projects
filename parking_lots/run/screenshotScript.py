from selenium import webdriver
import time
import urllib.request
import os
import numpy as np;
import cv2;

# def getHtml(url):
#     html = urllib.request.urlopen(url).read()
#     return html
 
# def saveHtml(file_name, file_content):
#     with open(file_name, "wb") as f:
#         f.write(file_content)

#crop the screenshotted image
def crop(img_path):
    img = cv2.imread(img_path,1)
    cutimg = img[16:-210,16:2020] # adject the crop range if it doesnt crop the image well
    cv2.imwrite(img_path,cutimg)


#CONSTANT FILE PATH


latlongpath = "./v1.csv"

indexHTMLpath = os.path.abspath(os.getcwd()) + "/index.html"

#directly save those screenshotted imaged into classifier folder
savedImgPath = os.path.abspath(os.getcwd()) + "/predict/img" 

chromeDriverPath = os.path.abspath(os.getcwd())+"/chromedriver" #remember to download chrome driver


f1 = open(latlongpath)
line = f1.readline()
count = 0
#can set a counter here if you want to test out a couple images first otherwise this will run thru the whole csv file
while line:

    line = f1.readline()

    cor = []
    tmp = line.split(",")

    cor.append(tmp[2]) # grab the latitude in the csv row. can change this base on your csv row format
    cor.append(tmp[3].strip()) # grab the longitude in the csv row. can change this base on your csv row format
    print("coord: ",cor)
    data = ''
    count+=1
    with open(indexHTMLpath, 'r+') as f:
        for line2 in f.readlines():
            if(line2.find('LatLng') >= 0):
                line2 = '                const c = new google.maps.LatLng(' + cor[0] + ',' + cor[1] + ');\n'
            data += line2
            
    with open(indexHTMLpath, 'r+') as f:
        f.writelines(data)

    driver = webdriver.Chrome(os.path.abspath(os.getcwd())+"/chromedriver")
    driver.get("file://" + indexHTMLpath)
    driver.maximize_window()
    time.sleep(2)
    print(count)

    try:
        picture_url = driver.get_screenshot_as_file(savedImgPath+"/" + str(count) + ".png")#screenshot the image
        print("Success", picture_url)
        crop(savedImgPath+"/" + str(count) + ".png")#crop the image
    except BaseException as msg:
        print(msg)

    driver.quit()
    line = f1.readline()
f1.close()


