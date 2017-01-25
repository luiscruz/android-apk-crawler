# android-apk-crawler
Project to analyze Android APKs regarding their approach to schedule tasks.
It provides a complement to Android apps' energy efficiency studies.

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
$pip install git+https://github.com/luiscruz/manifest-reader.git@master
$pip install git+https://github.com/luiscruz/android-apk-crawler.git@master
```

## Use case

This tool was tested with the APKs available
[here](http://sccpu2.cse.ust.hk/elite/downloadApks.html). It provides a dataset
with 44,736 Android apps, and it was collected between March 2015 and January
2016.

