from packaging.version import Version
from bs4 import BeautifulSoup
import requests
import keyboard
import time
import os
import re

versions = None

def main():
    reverse = True
    res = requests.get("https://www.python.org/ftp/python/")
    soup = BeautifulSoup(res.content,"html.parser")
    version_pattern = r"^3\.\d{1,}(\.\d{1,})?/$"
    versions = sorted([elm.text.replace("/","") for elm in soup.find_all("a",href=re.compile(version_pattern))], key=Version, reverse=reverse)
    os.system("cls")
    print("""
    [][][][][] [][][][][] [][][][][]            [][][][][] []      [] [][][][][]           [][][][][] []      []
    []         []             []                    []     []      [] []                   []      [] []      []
    []         []             []                    []     [][][][][] []                   [][][][][] [][][][][]
    []  [][][] [][][][][]     []                    []     []      [] [][][][][]           []                []
    []      [] []             []                    []     []      [] []                   []               []
    [][][][][] [][][][][]     []                    []     []      [] [][][][][]           []          [][][]
    """)
    time.sleep(1)
    os.system("cls")

    select = 0

    while True:
        os.system("cls")
        print("Get the py")
        print("上下キー:バージョン選択 3で検索モード Rキー:古い順/新しい順\n")
        
        for i,v in enumerate(versions[select:select+10]):
            if i == 0:
                print(f"\033[33m{v} <--\033[0m")
            else:
                print(v)
        
        key = keyboard.read_key()

        if key == "down":
            select+=1
        elif key == "up":
            select-=1
        elif key == "3":
            try:
                select = versions.index(input("バージョンを検索 >> "))
            except:
                print("存在しないバージョンです。")
                time.sleep(1)
            while True:
                if keyboard.read_key() == "enter":
                    break
        elif key == "r":
            if reverse:
                reverse = False
            else:
                reverse = True
            versions = sorted([elm.text.replace("/","") for elm in soup.find_all("a",href=re.compile(r"^3\.\d{1,}(\.\d{1,})?/"))], key=Version, reverse=reverse)
        elif key == "enter":
            break
        else:
            pass

        if select < 0:
            select = 0
        elif select > len(versions):
            select = len(versions)
        else:
            pass
    
    res2 = requests.get(f"https://www.python.org/ftp/python/{versions[select]}")
    soup2 = BeautifulSoup(res2.content,"html.parser")

    input()
    os.system("cls")

    installer_pattern = r"^python-\d\.\d{1,}(\.\d{1,})?(-arm64|-amd64)?\.exe$"
    filelist = soup2.find_all("a",string=re.compile(installer_pattern))

    for i,elm in enumerate(filelist):
        print(i,elm.text)

    file_number = int(input(f"インストーラーを選択 (0-{len(filelist)-1}) >> "))
    
    file = requests.get(f"https://www.python.org/ftp/python/{versions[select]}/{filelist[file_number].text}")

    with open(filelist[file_number].text,"wb+") as f:
        f.write(file.content)
    
    os.system(filelist[file_number].text)

if __name__ == "__main__":
    main()