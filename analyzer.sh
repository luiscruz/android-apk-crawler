#!/bin/sh
type apktool >/dev/null 2>&1 || { echo >&2 "I require apktool but it's not installed.  Aborting."; exit 1; }
type manifest-reader >/dev/null 2>&1 || { echo >&2 "I require manifest-reader but it's not installed. Check https://github.com/luiscruz/manifest-reader/ for installation instructions. Aborting."; exit 1; }

APK_DIR="./apks/"
APK_FILES=$APK_DIR/*.apk
KEYWORDS=(
    "Landroid/app/job/JobInfo/Builder;->build"
    "Lcom/google/android/gms/gcm/PeriodicTask/Builder;->build"
    "Lcom/google/android/gms/gcm/OneoffTask/Builder;->build"
    "Landroid/app/AlarmManager;->setWindow"
    "Landroid/app/AlarmManager;->setExact"
    "Landroid/app/AlarmManager;->setExactAndAllowWhileIdle"
    "Landroid/app/AlarmManager;->setInexactRepeating"
    "Landroid/app/AlarmManager;->setRepeating"
    "Landroid/app/AlarmManager;->set"
    "Landroid/app/AlarmManager;->setAndAllowWhileIdle"
    "Landroid/app/AlarmManager;->setAlarmClock"
    "Landroid/os/Handler;->post"
    "Landroid/os/Handler;->postDelayed"
    "Landroid/os/Handler;->sendEmptyMessage"
    "Landroid/os/Handler;->sendMessage"
    "Landroid/os/Handler;->sendMessageAtTime"
    "Landroid/os/Handler;->sendMessageDelayed"
)
#FIXME: Handler send methods are probably used in a subclass -> not sure this works

printf "App,Version,Package,AndroidVersion,${KEYWORDS[*]}\n" | tr ' ' ','
for APK_PATH in $APK_DIR/*.apk; do
    APK_FILENAME="${APK_PATH##*/}"
    PROJECT="${APK_FILENAME%.*}"
    DECODED_APK="./tmp/$PROJECT"
    
    printf "$PROJECT"
    apktool d $APK_PATH -o $DECODED_APK &> /dev/null
    printf ",%s" "$(manifest-reader --version-name --apk $APK_PATH)"
    printf ",%s" "$(manifest-reader --package-name $DECODED_APK/AndroidManifest.xml)"
    printf ",%s" "$(manifest-reader --android-sdk-version $DECODED_APK/AndroidManifest.xml)"
    for KEYWORD in ${KEYWORDS[*]}; do
        printf ","
        grep -ri $KEYWORD $DECODED_APK | wc -l | tr -d '\n '
    done
    echo
done
