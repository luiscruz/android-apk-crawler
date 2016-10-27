#!/bin/sh
type apktool >/dev/null 2>&1 || { echo >&2 "I require apktool but it's not installed.  Aborting."; exit 1; }
type manifest-reader >/dev/null 2>&1 || { echo >&2 "I require manifest-reader but it's not installed. Check https://github.com/luiscruz/manifest-reader/ for installation instructions. Aborting."; exit 1; }

APK_DIR="./apks/"
APK_FILES=$APK_DIR/*.apk
KEYWORDS=(
    "Landroid/app/job/JobInfo/Builder;->build"
    "Lcom/google/android/gms/gcm/PeriodicTask/Builder;->build"
    "Lcom/google/android/gms/gcm/OneoffTask/Builder;->build"
)

printf "App,Package,AndroidVersion,${KEYWORDS[*]}\n" | tr ' ' ','
for APK_PATH in $APK_DIR/*.apk; do
    APK_FILENAME="${APK_PATH##*/}"
    PROJECT="${APK_FILENAME%.*}"
    DECODED_APK="./tmp/$PROJECT"
    
    printf "$PROJECT"
    apktool d $APK_PATH -o $DECODED_APK &> /dev/null
    printf ",%s" "$(manifest-reader --package-name $DECODED_APK/AndroidManifest.xml)"
    printf ",%s" "$(manifest-reader --android-sdk-version $DECODED_APK/AndroidManifest.xml)"
    for KEYWORD in ${KEYWORDS[*]}; do
        printf ","
        grep -ri $KEYWORD $DECODED_APK | wc -l | tr -d '\n '
    done
    echo
done
