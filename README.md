# 植物标本条形码重命名工具 | SpeciLabeler

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

通过 [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar/) 使用条形码重命名植物标本图像！

Rename plant specimens images with barcodes using [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar/).

## 概述 | Description

`SpeciLabeler` 是一个 Python 工具，通过从图像中提取条形码信息，简化了对植物标本图像文件的重命名过程。该工具利用 `pyzbar` 库来解码条形码，非常适合管理和组织植物标本图像的集合。

`SpeciLabeler` is a Python tool that simplifies the process of renaming image files of plant specimens by extracting barcode information from the images. This tool leverages the power of the `pyzbar` library to decode barcodes, making it ideal for managing and organizing collections of plant specimen images.

## 特性 | Features

- 从植物标本图像中提取条形码 | Extract barcodes from plant specimen images

- 基于提取的条形码重命名图像文件 | Rename image files based on the extracted barcodes

- 支持 CODE128、CODE39、CODE93 和 CODABAR 格式的条形码 | Support for various barcode formats, including CODE128, CODE39, CODE93, and CODABAR

## 使用方法 | Usage

1. 安装所需的依赖项 | Install the required dependencies:

```
pip install pyzbar
```

2. 运行 `SpeciLabeler.py` 脚本 | Run the `SpeciLabeler.py` script:

```
python SpeciLabeler.py
```

3. 选择包含您要处理的植物标本图像的文件夹 | Select the folder containing the plant specimen images you want to process.

4. 按照屏幕提示输入可选的正则表达式，并允许工具处理和重命名图像文件 | Follow the on-screen prompts to input optional regular expressions and allow the tool to process and rename the image files.

## 许可证 | License

本项目在 MIT 许可下发布 - 有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 贡献 | Contribution

如果您想为项目做出贡献，欢迎建立分支并提交拉取请求！

Contributions are welcome! If you would like to contribute to the project, please fork the repository and submit a pull request.

## 作者 | Author

- 陈天翔 Chen Tianxiang (国家植物标本资源库，National Plant Specimen Resource Center) [chentx@ibcas.ac.cn](mailto:chentx@ibcas.ac.cn)

## 致谢 | Acknowledgments

- [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar/): 用于条形码解码 | The library used for barcode decoding.
