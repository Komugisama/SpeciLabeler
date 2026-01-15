import os
import time
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageFile
from pyzbar.pyzbar import decode, ZBarSymbol
import re
from tqdm import tqdm

# 设置Image的配置
Image.MAX_IMAGE_PIXELS = 240000000
ImageFile.LOAD_TRUNCATED_IMAGES = True


def get_barcode(path, allowed_symbols, user_regex):
    try:
        img = Image.open(path)
        barcode_info_list = decode(img, symbols=allowed_symbols)
        if barcode_info_list:
            barcodes = [
                barcode_info.data.decode("utf-8").replace(" ", "")
                for barcode_info in barcode_info_list
            ]
            if user_regex:
                pattern = re.compile(user_regex)
                matched_barcodes = [
                    barcode for barcode in barcodes if pattern.match(barcode)
                ]
                if matched_barcodes:
                    return True, matched_barcodes[0]
            return True, barcodes[0]
        else:
            return False, "barcode not found"
    except Exception as err:
        return False, f"can not open image: {err}"


def process_images_in_folder(folder_path, user_regex):
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff"}
    allowed_symbols = [
        ZBarSymbol.CODE128,
        ZBarSymbol.CODE39,
        ZBarSymbol.CODE93,
        ZBarSymbol.CODABAR,
    ]

    success_count = 0
    failed_count = 0
    file_count = 0

    log_path = os.path.join(folder_path, "log.txt")

    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"selected folder: {folder_path}\n")
        log.write(
            f"start at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n\n"
        )

        for root, directories, files in os.walk(folder_path):
            for file in files:
                extension = os.path.splitext(file)[1]
                if extension.lower() in allowed_extensions:
                    file_count += 1

        with tqdm(total=file_count, ascii=True) as pbar:
            for root, directories, files in os.walk(folder_path):
                for file in files:
                    extension = os.path.splitext(file)[1]
                    if extension.lower() in allowed_extensions:
                        image_path = os.path.join(root, file)
                        status, info = get_barcode(
                            image_path, allowed_symbols, user_regex
                        )
                        if status:
                            try:
                                new_filename = info + extension
                                os.rename(image_path, os.path.join(
                                    root, new_filename))
                                log_msg = f"{file} : {new_filename}"
                                log.write(log_msg + "\n")
                                success_count += 1
                            except Exception as e:
                                log_msg = f"{file} : {str(e)}"
                                log.write(log_msg + "\n")
                                failed_count += 1
                        else:
                            log_msg = f"{file} : {info}"
                            log.write(log_msg + "\n")
                            failed_count += 1
                        pbar.update(1)

        log.write(
            f"\nfinished at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}, "
            f"{success_count} success, {failed_count} failed\n\n\n\n\n"
        )

    print(
        f"\nfinished at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}, "
        f"{success_count} success, {failed_count} failed"
    )


if __name__ == "__main__":
    print("SpeciLabeler | 植物标本条码重命名工具 v1.1.2")

    print("选择待处理文件夹")
    root = tk.Tk()
    root.withdraw()

    path = filedialog.askdirectory()
    print("已选路径：", path)

    user_regex = input(
        "输入正则表达式 (如一副图像含多个条形码/二维码时，使用正则表达式匹配特定条形码，如不使用请按Enter键跳过)：")

    process_images_in_folder(path, user_regex)

    input("按任意键退出")
