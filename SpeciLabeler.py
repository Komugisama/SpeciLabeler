import os
import time
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageFile
from pyzbar.pyzbar import decode, ZBarSymbol
import re
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

GREEN = "\033[92m"
RESET = "\033[0m"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff"}
ALLOWED_SYMBOLS = [
    ZBarSymbol.CODE128,
    ZBarSymbol.CODE39,
    ZBarSymbol.CODE93,
    ZBarSymbol.CODABAR,
]

Image.MAX_IMAGE_PIXELS = 240000000
ImageFile.LOAD_TRUNCATED_IMAGES = True


def parse_barcode_results(barcode_info_list, pattern):
    if not barcode_info_list:
        return False, "未找到条码 | barcode not found"

    barcodes = [
        barcode_info.data.decode("utf-8").replace(" ", "")
        for barcode_info in barcode_info_list
    ]

    if pattern:
        matched_barcodes = [
            barcode for barcode in barcodes if pattern.match(barcode)
        ]
        if matched_barcodes:
            return True, matched_barcodes[0]
        return False, "未找到条码 | barcode not found"

    return True, barcodes[0]


def get_barcode(path, allowed_symbols, pattern):
    try:
        img = Image.open(path)

        width, height = img.size
        if width > 2000 or height > 2000:
            try:
                img_small = img.copy()
                img_small.thumbnail((2048, 2048))
                img_small = img_small.convert('L')

                barcode_info_list = decode(img_small, symbols=allowed_symbols)
                success, result = parse_barcode_results(
                    barcode_info_list, pattern)
                if success:
                    return success, result
            except Exception:
                pass

        barcode_info_list = decode(img, symbols=allowed_symbols)
        return parse_barcode_results(barcode_info_list, pattern)

    except Exception as err:
        return False, f"无法打开图像 | can not open image: {err}"


def process_image_task(args):
    image_path, pattern, allowed_symbols = args
    status, info = get_barcode(image_path, allowed_symbols, pattern)
    return image_path, status, info


def process_images_in_folder(folder_path, user_regex, max_workers=None):
    success_count = 0
    failed_count = 0

    image_paths = []

    for root, directories, files in os.walk(folder_path):
        for file in files:
            extension = os.path.splitext(file)[1]
            if extension.lower() in ALLOWED_EXTENSIONS:
                image_paths.append(os.path.join(root, file))

    file_count = len(image_paths)

    log_path = os.path.join(folder_path, "log.txt")

    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"选择的文件夹 | Selected folder: {folder_path}\n")
        log.write(
            f"开始时间 | Start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n\n"
        )

        if file_count == 0:
            log.write("未找到图像文件 | No images found\n\n")
            print("未找到图像文件 | No images found")
            return

        pattern = re.compile(user_regex) if user_regex else None
        tasks = [(image_path, pattern, ALLOWED_SYMBOLS)
                 for image_path in image_paths]

        if max_workers is None:
            cpu_count = os.cpu_count() or 1
            if cpu_count <= 4:
                max_workers = max(1, cpu_count - 1)
            else:
                max_workers = min(cpu_count, 8)

        with tqdm(total=file_count, ascii=True) as pbar:
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                for image_path, status, info in executor.map(
                    process_image_task, tasks
                ):
                    root = os.path.dirname(image_path)
                    file = os.path.basename(image_path)
                    extension = os.path.splitext(file)[1]

                    if status:
                        try:
                            new_filename = info + extension
                            os.rename(
                                image_path, os.path.join(root, new_filename)
                            )
                            log_msg = (
                                f"SUCCESS 成功 | {file} -> {new_filename}"
                            )
                            log.write(log_msg + "\n")
                            success_count += 1
                        except Exception as e:
                            log_msg = (
                                f"ERROR 失败(重命名) | {file} : {str(e)}"
                            )
                            log.write(log_msg + "\n")
                            failed_count += 1
                    else:
                        log_msg = f"FAILED 失败(识别) | {file} : {info}"
                        log.write(log_msg + "\n")
                        failed_count += 1
                    pbar.update(1)

        finished_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime()
        )
        log.write(
            f"\n结束时间 | Finished: {finished_time}, "
            f"成功 | Success: {success_count}, 失败 | Failed: {failed_count}\n\n\n\n\n"
        )

    finished_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(
        f"\n结束时间 | Finished: {finished_time}, "
        f"成功 | Success: {success_count}, 失败 | Failed: {failed_count}"
    )


if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()
    print("=" * 60)
    print(" 🌿 SpeciLabeler | 植物标本条码重命名工具 v1.1.2")
    print(" -- Rename plant specimen images with barcodes --")
    print("=" * 60)
    print(GREEN + "\n📂 请选择待处理文件夹 / Select folder to process\n" + RESET)
    root = tk.Tk()
    root.withdraw()

    path = filedialog.askdirectory()
    if path:
        print(f"- 已选路径 / Selected: {path}")
    else:
        print("⚠️  未选择路径 / No folder selected")
    user_regex = input(
        GREEN
        + "\n输入正则表达式（可选） / Optional regex:\n"
        + RESET
        + "* 用于一张图包含多个条形码/二维码时匹配特定条码；不使用时可直接按回车跳过。\n"
        + "* When an image contains multiple barcodes, use a regex to select one; press Enter to skip.\n"
        + RESET
    )
    cpu_count = os.cpu_count() or 1
    if cpu_count <= 4:
        recommended_workers = max(1, cpu_count - 1)
    else:
        recommended_workers = min(cpu_count, 8)
    process_images_in_folder(
        path, user_regex, max_workers=recommended_workers
    )

    input(GREEN + "\n✅ 按任意键退出 / Press any key to exit" + RESET)
