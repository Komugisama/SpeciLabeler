"""
Author: chentx
Date: 2020-11-06 16:28:35
LastEditTime: 2022-11-02 17:04:35
LastEditors: chentx
Description: 植物标本照片条码识别工具，使用ZXING解码（支持PE等标本馆使用的CODABAR编码）
"""
import os, time
import tkinter as tk
from tkinter import filedialog
from pyzxing import BarCodeReader

print("植物标本照片条码识别工具 for CODABAR Beta 0.0.1")
print("作者：陈天翔 chentx@ibcas.ac.cn 2020-11-12\n")

print("选择待处理文件夹")
root = tk.Tk()
root.withdraw()

path = filedialog.askdirectory()
print("已选路径：", path)

reader = BarCodeReader()

successCount = 0
failedCount = 0

log = open(os.path.join(path, "log.txt"), "a")
log.write("selected folder: " + path + "\n")
log.write("start at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n\n")
for root, directorys, files in os.walk(path):
    for file in files:
        allowedExtension = [
            ".jpg",
            ".JPG",
            ".jpeg",
            ".JPEG",
            ".png",
            ".PNG",
            ".gif",
            ".GIF",
        ]
        extension = os.path.splitext(file)[1]
        if extension in allowedExtension:
            imagePath = os.path.join(root, file)
            try:
                result = reader.decode(imagePath, True)
                decoded = result[0]
            except Exception as e:
                msg = file + " : " + str(e)
                print(msg)
                log.write(msg + "\n")
                failedCount += 1
            else:
                if decoded.get("parsed"):
                    try:
                        os.rename(
                            imagePath, os.path.join(root, decoded["parsed"] + extension)
                        )
                    except Exception as e:
                        msg = file + " : " + str(e)
                        print(msg)
                        log.write(msg + "\n")
                        failedCount += 1
                    else:
                        msg = file + " : " + decoded["parsed"] + extension
                        print(msg)
                        log.write(msg + "\n")
                        successCount += 1
                else:
                    msg = file + " : barcode not found"
                    print(msg)
                    log.write(msg + "\n")
                    failedCount += 1

log.write(
    "\nfinished at "
    + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    + ", "
    + str(successCount)
    + " success, "
    + str(failedCount)
    + " failed"
    + "\n\n\n\n\n"
)
log.close()

print(
    "\nfinished at "
    + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    + ", "
    + str(successCount)
    + " success, "
    + str(failedCount)
    + " failed"
)
input("press any button to exit")
