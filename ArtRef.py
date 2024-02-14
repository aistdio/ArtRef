# Basics
import webbrowser
import csv
import ctypes
from sys import exit
from os import listdir, remove
from os.path import isfile, join
import threading
import random
import time
# GUI
import customtkinter as ctk
from screeninfo import get_monitors
# Icons and img reader
from PIL import Image

# Get the wallpaper
SPI_GETDESKWALLPAPER = 0x0073
MAX_P = 260
wallpaper_p = ctypes.create_unicode_buffer(MAX_P)
ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, MAX_P, wallpaper_p, 0)

def main():
    get_folder.path = ""

    # Get monitor width and height
    monitor()

    # GUI with action buttons
    gui()
    
    # Concept
    # Get Directory from user (v1 = dir) (v2 = web api(gdisk)) (v3 = default image/ folder in root)
    # Check for extensions (.jpg, .png, etc.)
    
    # Read all files names in directory
    # (to remember which files were already shown)
    # assign numbers to each name and keep track of them in other file


    # Pick a random file from toshow.txt
    # Show it to user and remove number from toshow.txt, save them to hidden.txt
    # Display it to user

    print("0")
    exit


# Get current display width and height
def monitor():
    monitors = get_monitors()
    for item in monitors:
            a = str(item)
            if a.find("is_primary=True") != -1:
                b = str(a.split("width=", 1)[1]).partition(",")
                monitor.width = int(b[0])
                c = str(a.split("height=", 1)[1]).partition(",")
                monitor.height = int(c[0])
            else:
                 monitor.width = None
                 monitor.height = None
                 return


def get_folder():
    # Can also set starting dir via initialdir="C:\\Dir\\Dir2"
    get_folder.path = ctk.filedialog.askdirectory(title="Choose folder, artist")
    get_names(get_folder.path)
    select1.configure(values=[get_folder.path])
    select1.set(get_folder.path)


def select11(value):
    value = select1.get()
    get_folder.path = value


def angle_check():
    global Angle
    Angle = select_angle_var.get()


def draw_press():
    global timer
    timer = int(entry_var.get())
    if timer < 1:
        timer = 5
    if get_folder.path != "":
        gui.window.iconify()
        # Endless loop here
        new_gui(timer)


def destroy():
    image1_label.destroy()
    time.sleep(0.1)
    image2()


def get_image():
    # tmp = []
    # with open("images.csv") as f:
    #     reader = csv.DictReader(f)
    #     for item in reader:
    #         tmp.append(item["Path"])
    if not get_names.path:
        get_names(get_folder.path)
    imagep = random.choice(get_names.path)
    global im
    im = Image.open(imagep).rotate(angle=int(Angle))
    print(get_names.path)
    get_names.path.remove(imagep)
    print(get_names.path)


def new_gui(timer):
    global Angle
    Angle = select_angle_var.get()
    get_image()
    new_gui.width, new_gui.height = im.size
    mwidth = monitor.width
    mheight = monitor.height
    # imageopen = Image.open(images)
    global toplevel
    toplevel = ctk.CTkToplevel(gui.window)
    toplevel.title(f"Timer: {timer} sec")
    toplevel.grid()
    # Default size to first image size, then resize all other images to default
    if int(Angle) == 90:
        a = new_gui.height
        new_gui.height = new_gui.width
        new_gui.width = a
        b = mheight
        mheight = mwidth
        mwidth = b
    while new_gui.width > mwidth / 2 or new_gui.height > mheight:
                new_gui.width *= 0.99
                new_gui.height *= 0.99
    toplevel.geometry(f"{int(new_gui.width)}x{int(new_gui.height)}")
    image2()


def image2():
    get_image()

    width, height = im.size
    mwidth = monitor.width
    mheight = monitor.height    
    if int(Angle) == 90:
        a = height
        height = width
        width = a
        b = mheight
        mheight = mwidth
        mwidth = b
    while width > mwidth / 2 or height > mheight:
                width *= 0.99
                height *= 0.99
    
    global image1_label
    image1 = ctk.CTkImage(dark_image=im, size=(int(width),int(height)))
    image1_label = ctk.CTkLabel(toplevel, image=image1, text="")
    image1_label.place(relx=0.5,rely=0.5,anchor="center")
    t = threading.Timer(timer, destroy)
    t.start()


# Set up window
def gui():
    ctk.set_appearance_mode("dark")
    gui.window = ctk.CTk()
    gui.window.title("ArtRef")

    width = int(monitor.width*0.3)
    height = int(monitor.height*0.4)

    if monitor.width != None or monitor.height != None:
        gui.window.geometry(f"{width}x{height}")
    else:
        gui.window.geometry("500x550")

    my_font = ctk.CTkFont(family="Timew New Roman", weight="bold", size=12)

    # Wallpaper image
    walp = Image.open(wallpaper_p.value)
    walp.putalpha(150)
    wallpaper = ctk.CTkImage(dark_image=walp, size=(width, height))
    OnScreen = ctk.CTkLabel(master=gui.window, image=wallpaper, text="")
    OnScreen.place(relx=0.5, rely=0.5, anchor="center")

    btn = ctk.CTkButton(master=gui.window, text="Draw", command=draw_press, fg_color="#7d6f8a", hover_color="#de425d", font=my_font)
    btn.place(relx=0.5, rely=0.63, anchor="center")

    select = ctk.CTkComboBox(master=gui.window, values=["Your Folder", "Google Disk (doesn't work)", "Multiple Folders (doesn't work)"], fg_color="#7d6f8a", font=my_font)
    select.place(relx=0.23, rely=0.77, anchor="center")

    global select1
    select1 = ctk.CTkComboBox(master=gui.window, values=[get_folder.path], command=select11, fg_color="#7d6f8a", font=my_font)
    select1.place(relx=0.77, rely=0.86, anchor="center")
    
    path_select = ctk.CTkButton(gui.window, text="Choose folder\nwith references", command=get_folder, fg_color="#7d6f8a", hover_color="#de425d", font=my_font)
    path_select.place(relx=0.77, rely=0.78, anchor="center")

    global select_angle_var
    select_angle_var = ctk.StringVar(value="0")
    select_angle = ctk.CTkCheckBox(master=gui.window, text="Rotate by 90°", text_color="#7d6f8a", command=angle_check, variable=select_angle_var, onvalue="90", offvalue="0", font=my_font)
    select_angle.place(relx=0.23, rely=0.85, anchor="center")

    global entry_var
    entry_var = ctk.StringVar(value="5")
    entry = ctk.CTkEntry(master=gui.window, textvariable=entry_var, font=my_font, fg_color="#7d6f8a")
    entry.place(relx=0.5, rely=0.7, anchor="center")
    
    entry_label = ctk.CTkLabel(master=gui.window, text = "(Enter seconds for timer)\n(Exmaple: 5, 30, 150, etc)", text_color="#7d6f8a", font=my_font)
    entry_label.place(relx=0.5, rely=0.77, anchor="center")

    git = ctk.CTkButton(master=gui.window, text="Github", command=github_press, fg_color="#7d6f8a", hover_color="#de425d", font=my_font)
    git.place(relx=0.5, rely=0.9, anchor="center")

    gui.window.mainloop()


def get_names(dpath):
    supported = ['.png', '.jpg', '.jpeg', '.bmp']
    fields = ["Name", "Path"]
    get_names.names = []
    get_names.path = []
    for i in listdir(dpath):
        if any(k in i.lower() for k in supported):
            if isfile(join(dpath, i)):
                  # get_names.names.append({fields[0]:i, fields[1]:(dpath + "/" + i)})
                  get_names.path.append(dpath + "/" + i)

    # if isfile("images.csv"):
    #     remove("images.csv")
    # fc = open("images.csv", "x")
    # fc.close()
    # with open("images.csv", "w") as f:
    #     writer = csv.DictWriter(f, fieldnames=fields)
    #     writer.writeheader()
    #     for item in get_names.names:
    #         writer.writerow(item)
    # 
    # if isfile("images1.csv"):
    #     remove("images1.csv")
    # fc = open("images1.csv", "x")
    # fc.close()


def github_press():
    webbrowser.open("https://github.com/aistdio/ArtRef")


main()


# Features to add:
# Important:
# 0. Error Checkers to repeat functions for getting user input
# 1. Create a process for (IMAGE, not GUI) # while True (with sleep in process): save to settings.txt current size of window 
# (in case user wants to modify it), then on next start take window resolution for slide-show in settings in beginning each time
#
# Not yet important:
# 0. Change default size of GUI/img display and save it to settings.txt
# 1. Show on front page inspiring memes or a tracker of art progress/art studies to do today
# (everything is pre-configured by user in-app but by default its meme link)
# 2. If two or more monitors detected in get_monitos(), then first load mini-window to monitor(is_primary=True)
# to ask user if he wants to place entire window to one of the monitors, then remember setting and never ask again
# 3. You can put your drawing to reference with PIL.Image.blend(im1, im2, 0.5) to see where are your mistakes
