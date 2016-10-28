import os
import glob
import os.path
import sys
from subprocess import check_output

APK_DIR="./apks/"
KEYWORDS=(
    "Landroid/app/job/JobInfo/Builder;->build",
    "Lcom/google/android/gms/gcm/PeriodicTask/Builder;->build",
    "Lcom/google/android/gms/gcm/OneoffTask/Builder;->build",
    "Landroid/app/AlarmManager;->setWindow",
    "Landroid/app/AlarmManager;->setExact",
    "Landroid/app/AlarmManager;->setExactAndAllowWhileIdle",
    "Landroid/app/AlarmManager;->setInexactRepeating",
    "Landroid/app/AlarmManager;->setRepeating",
    "Landroid/app/AlarmManager;->set",
    "Landroid/app/AlarmManager;->setAndAllowWhileIdle",
    "Landroid/app/AlarmManager;->setAlarmClock",
    "Landroid/os/Handler;->post",
    "Landroid/os/Handler;->postDelayed",
    "Landroid/os/Handler;->sendEmptyMessage",
    "Landroid/os/Handler;->sendMessage",
    "Landroid/os/Handler;->sendMessageAtTime",
    "Landroid/os/Handler;->sendMessageDelayed",
)

def printm(msg):
    sys.stdout.write(str(msg))
    
def get_version_name(apk):
    return check_output(["manifest-reader","--version-name","--apk",apk]).replace("\n","")

def get_package_name(decoded_apk):
    return check_output(["manifest-reader","--package-name",decoded_apk+"/AndroidManifest.xml"]).replace("\n","")
    
def get_sdk_version(decoded_apk):
    return check_output(["manifest-reader","--android-sdk-version",decoded_apk+"/AndroidManifest.xml"]).replace("\n","")
def get_occurrences(decoded_apk, keywords):
    result = dict.fromkeys(keywords, 0)
    raw_output = check_output("grep -rhoE \""+"|".join(keywords) +"\" "+decoded_apk+"| sort | awk '{ print $1 }' | uniq -c", shell=True)
    for line in raw_output.split(os.linesep):
        if line:
            count,key = line.strip().split(' ')
            result[key] = count
    return result 

    

print "App,Version,Package,AndroidVersion,"+",".join(KEYWORDS)
for file in glob.glob(APK_DIR+"*.apk"):
    filename=os.path.basename(file)
    project = os.path.splitext(filename)[0]
    decoded_apk = "./tmp/%s"%project
    printm(project)
    printm(',')
    printm(get_version_name(file))
    printm(',')
    printm(get_package_name(decoded_apk))
    printm(',')
    printm(get_sdk_version(decoded_apk))
    occurrences = get_occurrences(decoded_apk,KEYWORDS)
    for key in KEYWORDS:
        printm(',')
        printm(occurrences[key])
    print
    
