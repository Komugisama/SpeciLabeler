'''
Author: chentx
Date: 2020-11-06 16:28:35
LastEditTime: 2020-11-18 17:05:40
LastEditors: chentx
Description: 植物标本照片条码识别工具，使用ZBAR解码（不支持PE等标本馆使用的CODABAR编码）
'''
import os, time
import tkinter as tk
from tkinter import filedialog
import pyzbar.pyzbar as pyzbar
from PIL import Image

def getBarcode(path):
    try:
        img = Image.open(path)
    except:
        return False, 'can not open image'
    barcodeInfoList = pyzbar.decode(img)
    if barcodeInfoList != []:
        barcodeInfo = barcodeInfoList[0]
        barcode = barcodeInfo.data.decode('utf-8').replace(' ','')
        return True, barcode
    else:
        return False, 'barcode not found'

print("植物标本照片条码识别工具 Beta 0.0.3")
print("作者：陈天翔 chentx@ibcas.ac.cn 2020-11-18\n")

print("选择待处理文件夹")
root = tk.Tk()
root.withdraw()

path = filedialog.askdirectory()
print("已选路径：", path)

successCount = 0
failedCount = 0

log = open(os.path.join(path, 'log.txt'), 'a')
log.write('selected folder: ' + path + '\n')
log.write('start at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n\n')
for root, directorys, files in os.walk(path):
    for file in files:
        allowedExtension = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG', '.gif', '.GIF']
        extension = os.path.splitext(file)[1]
        if extension in allowedExtension:
            imagePath = os.path.join(root, file)
            (status, info) = getBarcode(imagePath)
            if status:
                try:
                    os.rename(imagePath, os.path.join(root, info + extension))
                except Exception as e:
                    msg = file + ' : ' + str(e)
                    print(msg)
                    log.write(msg + '\n')
                    failedCount += 1
                else:
                    msg = file + ' : ' + info + extension
                    print(msg)
                    log.write(msg + '\n')
                    successCount += 1
            else:
                msg = file + ' : ' + info
                print(msg)
                log.write(msg + '\n')
                failedCount += 1

log.write('\nfinished at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ', ' + str(successCount) + ' success, ' + str(failedCount) + ' failed' + '\n\n\n\n\n')
log.close()

print ('\nfinished at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ', ' + str(successCount) + ' success, ' + str(failedCount) + ' failed')
input('按任意键退出')