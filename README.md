# android-apk-crawler
Project to analyse real Android applications

## Usage

```bash
$ android-apk-crawler --help
Usage: android-apk-crawler [OPTIONS]

  Tool to analyze Android applications through their APKs.

Options:
  --apks TEXT         Path to directory with all apks. Defaults to "./apks"
  --output-file TEXT  File to save the CSV output.
  --help              Show this message and exit.
```
## Install

```bash
$git clone https://github.com/luiscruz/android-apk-crawler.git
$cd android-apk-crawler
$pip install .
```