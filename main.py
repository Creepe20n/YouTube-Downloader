print("Starting \\0u0/")
import threading
import pytube as pt
from moviepy.editor import *
import eyed3 as eye
import colorama as ca
import re
import os
import subprocess
ca.init()

SaveNaming = True
OnlySound = True
SoundFormat = ".mp3"
DeleteAfterConvert = True
SoundAuthor = "#"
SoundAlbum = "#"

user_path = os.path.expanduser("~")
SaveFileName = "YTD.sav"

user_path = os.path.join(user_path,SaveFileName)

def LoadSettings():
    if not os.path.exists(user_path):
        with open(user_path,"w") as File:
            pass
        SaveSettings()
    else:
        with open(user_path,"r") as File:
            try:
                LoadArray = []
                for x in File:
                    x = x.replace("\n","")
                    name,value = x.strip().split("=")
                    value = value.strip()
                    print(value)
                    LoadArray.append(value)

                global SaveNaming
                global OnlySound
                global SoundFormat
                global DeleteAfterConvert
                global  SoundAuthor
                global  SoundAlbum
                SaveNaming = LoadArray[0]
                OnlySound = LoadArray[1]
                SoundFormat = LoadArray[2]
                DeleteAfterConvert = LoadArray[3]
                SoundAuthor = LoadArray[4]
                SoundAlbum = LoadArray[5]

                print(ca.Fore.GREEN+"Finished Loading\n"+ca.Fore.RESET)
            except:
                print(ca.Fore.RED + "Couldn't load from Savefile\n" + ca.Fore.RESET)
def SaveSettings():
    try:
        with open(user_path,"w") as File:
            File.write(f"SaveNaming = {SaveNaming}\nOnlySound = {OnlySound}\nSoundFormat = {SoundFormat}\nDeleteAfterConvert = {DeleteAfterConvert}\nSoundAuthor = {SoundAuthor}\nAlbum = {SoundAlbum}")
    except:
        print(ca.Fore.RED+"Couldn't create Savefile"+ca.Fore.RED)
def MainMenu():
    print("__Downloader_2.0__\n1) Download\n2) Setup")
    Selection = input("Selection: ")
    Selection = Selection.replace(" ","")
    if str(Selection) == "1":
        PreDownloader()
    if str(Selection) == "2":
        Space()
        Setup()

def Setup():
    global SaveNaming
    global OnlySound
    global SoundFormat
    global DeleteAfterConvert
    global SoundAuthor
    global SoundAlbum
    print(f"__Setup_1.0__\n1)Save Naming = {SaveNaming}"+ca.Fore.RED+ " (This will delete all non Alphanumeric Simbols)"+ca.Fore.RESET+f"\n2)Only Download Sound = {OnlySound}\n3)Delete Mp4 after Downloading = {DeleteAfterConvert}\n4)Set Auther of Music = {SoundAuthor} (Will be ignored when value is #)\n5)Set Audio Album = {SoundAlbum} (Will be ignored when value is #)\n6)Back")
    Input = str(input("Selection: "))
    if Input == "1":
        if SaveNaming:
            SaveNaming = False
        else:
            SaveNaming = True
    elif Input == "2":
        if OnlySound:
            OnlySound = False
        else:
            OnlySound = True
    elif Input == "3":
        if DeleteAfterConvert:
                DeleteAfterConvert = False
        else:
            DeleteAfterConvert = True
    elif Input == "4":
        Input = input("Type Author name: ")
        Input = Input.replace(" ","")
        SoundAuthor = Input
    elif Input == "5":
        Input = input("Type Album title: ")
        Input = Input.replace(" ","")
        SoundAlbum = Input
    elif Input == "6":
        Space()
        MainMenu()
        return
    else:
        print(ca.Fore.RED+"Wrong Input"+ca.Fore.RESET)
    SaveSettings()
    Space()
    Setup()
def Space(Num = 10):
    while Num >0:
        Num -=1
        print("\n")
def PreDownloader():
    print(ca.Fore.RED+"Make sure that the Video/Playlist is not private!"+ca.Fore.RESET)
    URL = str(input("Enter Video or Playlist Url: "))
    DownloadList = Detect(URL)
    if len(DownloadList) <= 0:
        MainMenu()
    Path = AskForPath()
    print("Start Downloading \\0u0/")
    Downloader(Path,DownloadList)
ErrorList = []
threads = []
def Downloader(Path,URLs):
    for x in URLs:
        YTvid = pt.YouTube(x)
        VidTitle = YTvid.title
        if SaveNaming:
            pattern = r'[^a-zA-Z\s]'
            VidTitle = re.sub(pattern,'',YTvid.title)
        YTvid.title = LookForExistens(Path,VidTitle,".mp4")
        print(ca.Fore.GREEN+"Download "+ VidTitle+ca.Fore.RESET)

        try:
            print("Test")
            if OnlySound:
                Stream = YTvid.streams.get_lowest_resolution()
            else:
                Stream = YTvid.streams.get_highest_resolution()
            print("Test2")
            TempMp4Path = Stream.download(Path)
        except Exception as e:
            ErrorList.append("Download Failed for "+VidTitle)
            continue

        if OnlySound:
            th = threading.Thread(target=ConvertToMp3, args=(TempMp4Path,))
            threads.append(th)
            th.start()

    for x in threads:
        x.join()
    Space()
    for x in ErrorList:
        print(x)
    subprocess.Popen(["explorer",Path])
    MainMenu()

def LookForExistens(Path,title,Format):
    NewTitle = title
    Count = 0
    path = os.path.join(Path,NewTitle+Format)
    while os.path.exists(path):
        NewTitle = NewTitle+" ("+str(Count)+")"
        path = os.path.join(Path,NewTitle)
        Count +=1
    return NewTitle

def AskForPath():
    Path = ""
    while not os.path.exists(Path):
        Path = input("Where to Save your files?")
        if not os.path.exists(Path):
            print(ca.Fore.RED+"Path is not valid"+ca.Fore.RESET)
    return Path

def ConvertToMp3(VidPath):
    print(ca.Fore.GREEN+"Start Converting"+ca.Fore.RESET)
    try:
        NewPath = VidPath.replace(".mp4", SoundFormat)

        Audio = AudioFileClip(VidPath)
        Audio.write_audiofile(NewPath,verbose= False, logger= None)
        Audio.close()
        if SoundAuthor != "#":
            File = eye.load(NewPath)
            File.tag.artist = SoundAuthor
            File.tag.save()
        if SoundAlbum != "#":
            File = eye.load(NewPath)
            File.tag.album = SoundAlbum
            File.tag.save()
        print(ca.Fore.GREEN+"Finished Converting"+ca.Fore.RESET)
        if DeleteAfterConvert:
            os.remove(VidPath)
    except:
        ErrorList.append("Convert "+VidPath+" To"+SoundFormat+" Failed")

def Detect(URL):
    try:
        UrlList = []
        try:
            YTvid = pt.YouTube(URL)
            print(ca.Fore.GREEN+ YTvid.title+ca.Fore.RESET)
            UrlList.append(URL)
        except:
            YTlist = pt.Playlist(URL)
            print(ca.Fore.GREEN + YTlist.title+"\n"+YTlist.owner+"\n"+str(len(YTlist.videos))+ca.Fore.RESET)
            UrlList = YTlist.video_urls
        return UrlList
    except:
        print(ca.Fore.RED+"URL is not valid"+ca.Fore.RESET)
        return []

if __name__ == "__main__":
    LoadSettings()
    MainMenu()