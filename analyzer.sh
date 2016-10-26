#!/bin/sh
APK_DIR="./apks/"
APK_FILES=$APK_DIR/*.apk
KEYWORDS=(
    "Landroid/app/job/JobInfo/Builder;->build"
    "Lcom/google/android/gms/gcm/PeriodicTask/Builder;->build"
    "Lcom/google/android/gms/gcm/OneoffTask/Builder;->build"
)

printf "App,${KEYWORDS[*]}\n" | tr ' ' ','
for APK_PATH in $APK_DIR/*.apk; do
    APK_FILENAME="${APK_PATH##*/}"
    PROJECT="${APK_FILENAME%.*}"
    DECODED_APK="./tmp/$PROJECT"
    
    printf "$PROJECT"
    for KEYWORD in ${KEYWORDS[*]}; do
        apktool d $APK_PATH -o $DECODED_APK &> /dev/null
        printf ","
        grep -ri $KEYWORD $DECODED_APK | wc -l | tr -d '\n '
    done
    echo
done
echo
