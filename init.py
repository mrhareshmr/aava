#!/usr/bin/python

import os
import sys
import urllib.request
import zipfile
import subprocess

global apk_file, apkpath, apkname, tools, apktooldir, cwd, dex2jardir
toolurl = "https://github.com/mrhareshmr/aava/releases/download/start/tools.zip"
cwd = os.path.dirname(os.path.realpath(sys.argv[0]))


def sysargv():
    if (len(sys.argv) < 2 or len(sys.argv) > 2):
        print("Provide APK path")
    else:
        apk_file = sys.argv[1]
        if (apk_file == '-h' or not apk_file.endswith('.apk')):
            print('\nUsage: AAVA.py ApkFileName or [options]\n\n Options:\n -h   show this help message and exit')
        dirmk(apk_file)


def report(blocknr, blocksize, size):
    current = blocknr * blocksize
    sys.stdout.write("\rProgress: {0:.2f}%".format(100.0 * current / size) + " - {0:.1f} MB".format(
        current / 1024 / 1024) + "/{0:.1f} MB".format(size / 1024 / 1024))


def tooldownload(toolurl, cwd, report):
    if not os.path.exists(cwd + '/tools'):
        os.mkdir(cwd + '/tools')
    print("\nDownloading tools... -> " + cwd + "/tools")
    name = os.path.join(cwd, 'temp.zip')
    try:
        name = urllib.request.urlretrieve(toolurl, name, report)
        pass
    except IOError as e:
        print("Can't retrieve %r to %r: %s" % (toolurl, cwd, e))
        return
    try:
        zip_ref = zipfile.ZipFile(cwd + '/temp.zip', 'r')
        zip_ref.extractall(cwd)
        zip_ref.close()
    except zipfile.error as e:
        print("Bad zipfile (from %r): %s" % (toolurl, e))
        return


def dirmk(apk_file):
    if apk_file.endswith('.apk'):
        apkpath = os.path.dirname(apk_file)
        apkname = os.path.basename(os.path.splitext(apk_file)[0])
        if not os.path.exists(apkpath + '/' + apkname):
            os.makedirs(apkpath + '/' + apkname)
    tooldownload(toolurl, cwd, report)


def apktool(apkfile):
    print("Using APKTOOL")
    apkpath = os.path.dirname(apkfile)
    apkname = os.path.basename(os.path.splitext(apkfile)[0])
    apktooldir = cwd + '/tools/apktool.jar'
    outputdir = apkpath + '/' + apkname + '_apktool'
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    if apkfile != '':
        cmd = ('java -jar ' + apktooldir + ' d ' + apkfile + ' -o ' + outputdir + ' -f')
        subprocess.call(cmd, shell=True)


def dexjar(apkfile):
    print('\nUsing Dex2Jar')
    apkpath = os.path.dirname(apkfile)
    apkname = os.path.basename(os.path.splitext(apkfile)[0])
    dex2jardir = cwd + '/tools/dex2jar-0.0.9.15/d2j-dex2jar.sh'
    outputdir = apkpath + '/' + apkname + '_dex2jar'
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    if apkfile != '':
        cmd = ('sh ' + dex2jardir + ' ' + apkfile + ' -o ' + outputdir + '/out.jar' + ' -f')
        subprocess.call(cmd, shell=True)


def main():
    sysargv()
    apk_file = sys.argv[1]
    try:
        apktool(apk_file)
    except IOError:
        print("Use Valid APK")
    try:
        dexjar(apk_file)
    except IOError:
        print("Use Valid APK")
    os.remove(cwd + '/temp.zip')
    print('\n\nCheck APK directory for decompiled files\n')
        

if __name__ == "__main__":
    main()
