import os
import os.path
import sys
import click
import time
import pandas
import matplotlib.pyplot as plt

KEYWORDS = [
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
    "Lcom/firebase/jobdispatcher/FirebaseJobDispatcher;->newJobBuilder",
    "Lcom/evernote/android/job/JobRequest;->Builder",
]

@click.command()
@click.option(
    '--input', '-i',
    prompt="Input CSV files",
    help='CSV files to be used.')
@click.option(
    '--output-dir', '-o',
    prompt="Output directory",
    help='Directory where to store the reports.')
def tool(input, output_dir):
    """Tool to generate reports resulting from the android-apk-crawler analysis."""

    start_time = time.time()

    df = pandas.read_csv(input)
    print df[KEYWORDS].sum()
    
    plt.figure()
    df[KEYWORDS].sum().plot(kind="bar")
    plt.savefig(output_dir+'/plot_api_occurence.png')
    
    plt.figure()
    df['minSdkVersion'].hist()
    plt.savefig(output_dir+'/hist_minsdk.png')
    
    click.secho(
        "Generated reports in {:.1f} minutes.".format(
            (time.time() - start_time) / 60
        ),
        fg='blue'
    )

if __name__ == '__main__':
    tool()
