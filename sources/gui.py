from packaging.version import Version
from bs4 import BeautifulSoup
import tkinter as tk
import tkinter.ttk as ttk
import requests
import os
import re

root = tk.Tk()
root.state("zoomed")
root.title("Get the py")

version = None

res = requests.get("https://www.python.org/ftp/python/")
soup = BeautifulSoup(res.content,"html.parser")
version_pattern = r"^3\.\d{1,}(\.\d{1,})?/$"
versions = sorted([elm.text.replace("/","") for elm in soup.find_all("a",href=re.compile(version_pattern))], key=Version)
version_comb=ttk.Combobox(root,values=tuple(versions))
select_python_version = tk.Label(text="Select python version",font=("メイリオ",10))

def download_and_run(event):
    file = requests.get(f"https://www.python.org/ftp/python/{version}/{file_comb.get()}")
    filepath = os.path.join(os.getenv("temp"),file_comb.get())

    with open(filepath,"wb+") as f:
        f.write(file.content)
    
    root.destroy()
    os.system(filepath)

def get_installers(event):
    global file_comb,version
    version = version_comb.get()
    loading = tk.Label(text="Loading...")
    loading.pack()
    res2 = requests.get(f"https://www.python.org/ftp/python/{version}")
    soup2 = BeautifulSoup(res2.content,"html.parser")

    installer_pattern = r"^python-\d\.\d{1,}(\.\d{1,})?.*(-arm64|-amd64)?(\.exe|\.msi)$"
    filelist = [elm.text for elm in soup2.find_all("a",string=re.compile(installer_pattern))]

    loading.destroy()
    version_comb.destroy()
    select_python_version.destroy()

    select_installer = tk.Label(text="Please select installer file",font=("メイリオ",10))
    select_installer.pack()

    file_comb = ttk.Combobox(root,values=tuple(filelist))
    file_comb.bind("<<ComboboxSelected>>",download_and_run)
    file_comb.pack()

def main():
    title = tk.Label(text="Get the py <GUI>",font=("メイリオ",32))
    title.pack()
    select_python_version.pack()
    
    version_comb.pack()
    version_comb.bind("<<ComboboxSelected>>",get_installers)
    root.mainloop()

if __name__ == "__main__":
    main()