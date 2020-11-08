'''
Author: chentx
Date: 2020-11-06 16:28:35
LastEditTime: 2020-11-06 23:39:50
LastEditors: chentx
Description: 
'''
from pyzxing import BarCodeReader

reader = BarCodeReader()
results = reader.decode('C:\Komugi/Projects/python/barcode_reader/images/codabar.png')
print(results)