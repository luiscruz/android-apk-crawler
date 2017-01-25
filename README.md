# android-apk-crawler
Project to analyse real Android applications

## Usage

```bash
$ android-apk-crawler --help
Usage: android-apk-crawler [OPTIONS]

  Tool to analyze Android applications through their APKs.

Options:
  --apks TEXT             Path to directory with all apks. Defaults to
                          "./apks"
  -o, --output-file TEXT  File to save the CSV output.
  --help                  Show this message and exit.
```
## Install

1. Make sure you have [APKTool](https://ibotpeaches.github.io/Apktool/install/) installed
1. Run the following instructions on your terminal:
```bash
$pip install git+https://github.com/luiscruz/android-apk-crawler.git@master
```
