import os
import glob
import os.path
import sys
import subprocess
import click
import yaml
import time

KEYWORDS = (
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


def printm(msg, file=sys.stdout):
    file.write(str(msg))


def get_version_name(apk):
    return subprocess.check_output([
        "manifest-reader",
        "--version-name",
        "--apk", apk
    ]).replace("\n", "")


def get_package_name(decoded_apk):
    return subprocess.check_output([
        "manifest-reader",
        "--package-name",
        decoded_apk + "/AndroidManifest.xml"
    ]).replace("\n", "")


def get_sdk_version(decoded_apk):
    return subprocess.check_output([
        "manifest-reader",
        "--android-sdk-version",
        decoded_apk + "/AndroidManifest.xml"
    ]).replace("\n", "")


def get_min_sdk_version(decoded_apk):
    apktool_yaml_path = decoded_apk + "/apktool.yml"
    with open(apktool_yaml_path, 'r') as yaml_file:
        try:
            apktool_yaml = yaml.load(yaml_file.read().replace('!!', '#!!'))
            sdkInfo = apktool_yaml.get("sdkInfo")
            if sdkInfo is not None:
                return sdkInfo.get("minSdkVersion")
        except yaml.YAMLError as exc:
            print exc
            click.secho(
                'get_min_sdk_version YAML {} file not vaild.'
                .format(apktool_yaml_path),
                err=True, fg='red')
    return None


def get_occurrences(decoded_apk, keywords):
    result = dict.fromkeys(keywords, 0)
    raw_output = subprocess.check_output(
        "grep -rhoE \"" +
        "|".join(keywords) + "\" " + decoded_apk +
        "| sort | awk '{ print $1 }' | uniq -c", shell=True)
    for line in raw_output.split(os.linesep):
        if line:
            count, key = line.strip().split(' ')
            result[key] = count
    return result


def decode_apk(apk, output_dir):
    subprocess.check_output(
        "apktool d {} -o {}".format(apk,output_dir),
        shell=True,
    )


@click.command()
@click.option(
    '--apks',
    default="./apks/",
    help='Path to directory with all apks. Defaults to "./apks"')
@click.option(
    '--output-file', '-o',
    prompt="Output CSV file",
    help='File to save the CSV output.')
@click.option(
    '--exectime', '-t', is_flag=True,
    help='print execution time')
def tool(apks, output_file, exectime):
    """Tool to analyze Android applications through their APKs."""

    if exectime:
        start_time = time.time()

    if not os.path.exists(output_file):
        with open(output_file, 'a') as f:
            print >> f, "App,Version,Package,AndroidVersion,minSdkVersion," \
                + ",".join(KEYWORDS)
    apk_files = glob.glob(apks + "/**.apk")

    with click.progressbar(
        apk_files,
        fill_char=click.style(">", fg='green'),
        empty_char=' ',
        show_percent=True,
        show_pos=True,
    ) as apk_files_bar:
        for file in apk_files_bar:
            filename = os.path.basename(file)
            project = os.path.splitext(filename)[0]
            decoded_apk = "./tmp/{}".format(project)
            if not os.path.exists(decoded_apk):
                decode_apk(file, decoded_apk)
            occurrences = get_occurrences(decoded_apk, KEYWORDS)
            line = ",".join([
                project,
                get_version_name(file),
                get_package_name(decoded_apk),
                get_sdk_version(decoded_apk),
                get_min_sdk_version(decoded_apk) or "NA",
            ] + [
                str(occurrences[key]) for key in KEYWORDS
            ])
            with open(output_file, 'a') as f:
                print >> f, line

    if exectime:
        click.secho(
            "Processed {} files in {:.1f} minutes.".format(
                len(apk_files),
                (time.time() - start_time) / 60),
            fg='blue'
        )


if __name__ == '__main__':
    tool()
