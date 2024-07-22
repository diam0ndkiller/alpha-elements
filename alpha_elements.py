#!/bin/python3
import os

RUNDIR = os.path.realpath(__file__).split("/alpha_elements.py")[0]

os.chdir(RUNDIR)

try:
    from dcgf import *
except:
    try:
        from dia_graphics import *
    except:
        print("Please download https://github.com/diam0ndkiller/dcgf graphics library.")

try:
    import requests
    import bs4
    import tkinter
    import pygame
except:
    cmd.import_python_module("requests")
    cmd.import_python_module("bs4")
    cmd.import_python_module("tk")
    cmd.import_python_module("pygame")

import tkinter as tk
from tkinter import filedialog as fd

root = tk.Tk()
root.withdraw()

import requests
import getpass
import bs4
import subprocess

pg.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = f'0,0'

SCROLL_SPEED = 15
VERSION = "V1.0"
RELEASEDATE = "2024-01-28"
WIDTH, HEIGHT, total_width, total_height, factor = init__surface((1000, 1000), (1000, 1000), 8, '1.0', True, 0, "AlphaElements Minecraft Launcher", "__RESOURCES__/alpha_elements/images/alpha_elements.png")
init__logger("__LOGS__/" + time.strftime("%Y-%m-%d, %H-%M-%S") + ".log")

init__fonts(COLORS.content.values(), name = "minecraft", plugin = "alpha_elements")

if cmd.LINUX:
    MC_DIR = "/home/" + getpass.getuser() + "/.minecraft"
elif cmd.WINDOWS:
    MC_DIR = "C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft"

cmd.create_dir(MC_DIR + "/alpha_elements")
CONFIG_DIR = MC_DIR + "/alpha_elements"


class Mod:
    def __init__(this, name: str, version: str, url: str = ""):
        this.name = name
        this.version = version
        this.url = url or f"{CONFIG_DIR}/mods/{this.version}/{this.name}.jar"

    def copy(this):
        cmd.copy_file(this.url, f"{MC_DIR}/mods/{this.name}-{this.version}.jar")

    def __repr__(this):
        return f"Mod('{this.name}', '{this.version}', '{this.url}')"


class Profile:
    def __init__(this, version: str, name: str = '', mods: list = []):
        if "[" in version: version = version[2:-2]
        if "[" in name: name = name[2:-2]
        this.version = version
        this.name = name or version
        this.mods = mods or [Mod("aetweaks", this.version).__repr__(), Mod("OptiFine", this.version).__repr__()]
        install_of(this.version)

    def launch(this):
        global pro
        draw_loading("forging forge...")
        forgeV = install_forge(this.version)
        draw_loading("setting up version...")
        create_mc_profile(this.name, forgeV)
        backup_mods()
        for i in this.mods: eval(i).copy()
        draw_loading("launching minecraft...")
        pro = subprocess.Popen("minecraft-launcher", shell=True)
        setup_page_home()

        return pro

    def __repr__(this):
        return f"Profile('{this.version}', '{this.name}', {str(this.mods)})"



def get_all_dash(text: str):
    text = text.replace(" ", "").replace(".", "").replace("-", "")
    return recursive_dash(text, len(text) // 5 + 1)

def recursive_dash(text: str, depth: int = 1):
    if depth == 1:
        return [text]
    texts = recursive_dash(text, depth - 1)
    output = [text]
    for i in texts:
        for j in range(len(i)):
            if j == 0: continue
            x = i[:j] + "-" + i[j:]
            output.append(x)
    return output


def get_forge_versions():
    global VERSIONS, CONFIG

    VERSIONS = []

    r = requests.get(f"https://files.minecraftforge.net/net/minecraftforge/forge/")

    soup = bs4.BeautifulSoup(r.text, "html.parser")

    for i in soup.find_all("ul", {"class": "nav-collapsible"}):
        for j in i:
            for k in j:
                k = str(k).strip("\n")
                if not k: continue
                if "a" in k:
                    v = k.split(">")[1].split("<")[0]
                else:
                    v = k
                    if not 'version' in CONFIG: CONFIG['version'] = v
                if not "pre" in v and (int(v.split(".")[1]) > 5 or v == "1.5.2"): VERSIONS.append(v)


def create_mc_profile(version_name: str, version_id: str):
    file_data = cmd.read_json(MC_DIR + "/launcher_profiles.json")

    icon = cmd.image_to_base64('__RESOURCES__/alpha_elements/images/alpha_elements.png')

    profile = {"created": time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
               "icon": icon,
               "javaArgs" : "-Xmx8G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M",
               "lastUsed": time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
               "lastVersionId": version_id,
               "name": "alpha-elements: Forge " + version_name,
               "type": "custom"}
    file_data["profiles"]["forge_" + version_name] = profile
    cmd.write_json(file_data, MC_DIR + "/launcher_profiles.json")

def search_mc_mod(mod_name: str):
    os.system("xdg-open https://www.curseforge.com/minecraft/mc-mods/search?search=" + mod_name)
    pg.display.iconify()

def import_mod():
    url = fd.askopenfilename()
    if type(url) != str or not url: return
    file = url.split("/")[-1]
    filename = file.split(".jar")[0]
    path = url[:-len(file)]
    modname = filename
    modversion = "generic"
    if "[" in filename:
        version = filename.split("[")[1].split("]")[0]
        name = filename.split(" ")[1]
        if version in VERSIONS:
            modversion = version
            modname = name.split("-")[0].split("_")[0]
    elif not "lib" in filename.lower():
        if "-" in filename:
            for i in range(1, 4):
                try: version = filename.split("-")[i]
                except: break
                if version == "forge": version = filename.split("-")[i + 1]
                if "mc" in version: version = version[2:]
                if "_" in version: version = version.split("_")[0]
                if version in VERSIONS:
                    modname = filename.split("-")[i - 1]
                    modversion = version
                    break
        elif "_" in filename:
            for i in range(1, 4):
                try: version = filename.split("_")[i]
                except: break
                if version == "forge": version = filename.split("_")[i + 1]
                if "mc" in version: version = version[2:]
                if version in VERSIONS:
                    modname = filename.split("_")[i - 1]
                    modversion = version
    cmd.create_dir(f"{CONFIG_DIR}/mods/{modversion}")
    cmd.copy_file(url, f"{CONFIG_DIR}/mods/{modversion}/{modname}.jar")
    read_mods()
    setup_page_mods()


def backup_mods():
    cmd.create_dir(f"{CONFIG_DIR}/mods/backup")
    for i in cmd.list_directory(f"{MC_DIR}/mods"):
        cmd.copy_file(f"{MC_DIR}/mods/{i}", f"{CONFIG_DIR}/mods/backup/")
        cmd.delete_file(f"{MC_DIR}/mods/{i}")

def get_real_forge_install_folder(direct_forge_version):
    mc_version = int(direct_forge_version.split(".")[1].split("-")[0])

    mc_version_string = direct_forge_version.split("-")[0]
    forge_version_string = direct_forge_version.split("-")[2]

    # correct forge install folder for versions before 1.12
    if mc_version > 11:
        output = "{}-forge-{}".format(mc_version_string, forge_version_string)

    elif mc_version > 7:
        # correct wrong version prefix in forge 1.10 -> 1.10.0
        mc_version_prefix = mc_version_string
        if mc_version_prefix in ["1.10"]:
            mc_version_prefix += ".0"
        
        # append version prefix to forge 1.10, 1.8.9, 1.9.4, 1.7.10
        if mc_version_string in ["1.10", "1.8.9", "1.9.4", "1.7.10"]:
            output = "{}-forge{}-{}-{}".format(mc_version_string, mc_version_string, forge_version_string, mc_version_prefix)
        else:
            output = "{}-forge{}-{}".format(mc_version_string, forge_version_string, mc_version_prefix)

    elif mc_version_string == "1.7.10":
        mc_version_prefix = mc_version_string

        output = "{}-Forge{}-{}".format(mc_version_string, forge_version_string, mc_version_prefix)

    elif mc_version_string == "1.7.2":
        mc_version_prefix = "mc" + mc_version_string.replace(".", "")

        output = "{}-Forge{}-{}".format(mc_version_string, forge_version_string, mc_version_prefix)

    elif mc_version_string in ["1.6.1"]:
        output = "Forge{}".format(forge_version_string)

    else:#if mc_version_string in ["1.6.4", "1.6.3", "1.6.2", "1.5.2"]:
        output = "{}-Forge{}".format(mc_version_string, forge_version_string)


    print__debug(mc_version_string)
    print__debug(output)

    return output


def install_forge(version):
    r = requests.get(f"https://files.minecraftforge.net/net/minecraftforge/forge/index_{version}.html")

    try:
        tag_A = r.content.decode().split('Download Recommended<br>\n')[1].split("<a")[1].split("</a>")[0]
    except:
        print__info("Downloading latest instead of recommended forge version.")
        tag_A = r.content.decode().split('Download Latest<br>\n')[1].split("<a")[1].split("</a>")[0]
        '''if not "jar" in tag_A:
            print__info("Downloading game executable instead of installer.")
            tags = r.content.decode().split('Download Latest<br>\n')[1].split("<a")
            for i in tags:
                if "universal.zip" in i or "client.zip" in i:
                    tag_A = i.split("</a>")[0]
                    break'''

    link = tag_A.split('"')[1]
    if "url=" in link:
        link = link.split("url=")[1]

    print__info("Downloading " + link)

    forge_version = link.split("/forge/")[1].split("/")[0]

    direct_forge_version = forge_version.split("-")[0] + "-forge-" + forge_version.split("-")[1]

    if not os.path.isdir(MC_DIR + "/versions/" + get_real_forge_install_folder(direct_forge_version)):
        r = requests.get(link)

        cmd.create_dir(CONFIG_DIR + "/versions/")

        with open(CONFIG_DIR + f"/versions/{direct_forge_version}.jar", "wb") as file:
            file.write(r.content)

        if "jar" in link:
            os.system(f"java -jar ./versions/{direct_forge_version}.jar")
        '''else:
            cmd.create_dir(f"{MC_DIR}/versions/{get_real_forge_install_folder(direct_forge_version)}")
            cmd.copy_file(f"./versions/{direct_forge_version}.jar", f"{MC_DIR}/versions/{get_real_forge_install_folder(direct_forge_version)}/{get_real_forge_install_folder(direct_forge_version)}.jar")'''

    # TODO
    exit(0)

    return get_real_forge_install_folder(direct_forge_version)


def install_of(version):
    if not os.path.exists(f"{CONFIG_DIR}/mods/{version}/OptiFine.jar"):
        draw_loading("downloading OptiFine...")

        r = requests.get(f"https://optifine.net/downloads")

        try:
            tagTable = r.content.decode().split("<h2>Minecraft " + version + "</h2>")[1].split("<table class='downloadTable mainTable'>")[1].split("</table>")[0]
            tagA = tagTable.split("colMirror")[1].split("</td>")[0]
            url = tagA.split('href="')[1].split('"')[0]
            r = requests.get(url)
            tagSpan = r.content.decode().split('<span id="Download">')[1].split("</span>")[0]
            link = "https://optifine.net/" + tagSpan.split("<a href='")[1].split("'")[0]
            print__debug(link)
        except:
            print__warning("No OptiFine version found for " + version)
            return

        r = requests.get(link)

        cmd.create_dir(f"{CONFIG_DIR}/mods/{version}/")

        with open(f"{CONFIG_DIR}/mods/{version}/OptiFine.jar", "wb") as file:
            file.write(r.content)


def save_config():
    with open(CONFIG_DIR + "/alpha_elements.conf", "w") as file:
        file.write(str(CONFIG))

def read_config():
    global CONFIG

    try:
        with open(CONFIG_DIR + "/alpha_elements.conf", "r") as file:
            CONFIG = eval(file.read())
    except:
        CONFIG = {"profiles": {}}

def read_mods():
    global MODS

    MODS = {}
    for v in cmd.list_directory(f"{CONFIG_DIR}/mods/"):
        if os.path.isdir(f"{CONFIG_DIR}/mods/{v}"):
            MODS[v] = []
            for m in cmd.list_directory(f"{CONFIG_DIR}/mods/{v}"):
                MODS[v].append(Mod(m.split(".jar")[0], v))


def setup_header():
    global IMAGES_header, BUTTONS_header, TEXTS_header, SCROLLABLES_header

    IMAGES_header = Enum()
    TEXTS_header = Enum()
    BUTTONS_header = Enum()

    IMAGES_header.set(background = ScreenObject(Surface((WIDTH, HEIGHT)).blit(Surface((70, HEIGHT), Color(25, 25, 25)), (0, 0)).blit(Surface((WIDTH, 50), Color(25, 25, 25, 172)), (0, 0))).set((0, 0), 7))

    IMAGES_header.set(overlay = ScreenObject(Surface((WIDTH, HEIGHT), Color(50, 50, 50, 100))).set((0, 0), 7))

    TEXTS_header.set(name = ScreenObject(Image("ae_text_header.png", (280, 30), plugin = "alpha_elements")).set((WIDTH // 2, 25), 7, (True, True)))
    
    #BUTTONS_header.set(close = Button(Image("close.png", plugin = "alpha_elements"), Image("close_chosen.png", plugin = "alpha_elements"), alt_text = "Close [Esc]").set((950, 0), 3))

    BUTTONS_header.set(home = Button(Image("home.png", plugin = "alpha_elements"), Image("home_chosen.png", plugin = "alpha_elements"), alt_text = "Home Screen").blit_all(Text("Play", Color(0, 75, 0), font_size = 0.8), (25, 35), (True, False)).set((10, 60), 7))
    BUTTONS_header.set(mods = Button(Image("mods.png", plugin = "alpha_elements"), Image("mods_chosen.png", plugin = "alpha_elements"), alt_text = "Mods List").blit_all(Text("Mods", Color(0, 75, 0), font_size = 0.8), (25, 35), (True, False)).set((10, 260), 7))
    BUTTONS_header.set(resource_packs = Button(Image("resource_packs.png", plugin = "alpha_elements"), Image("resource_packs_chosen.png", plugin = "alpha_elements"), alt_text = "Coming Soon TM").blit_all(Text("Packs", Color(0, 75, 0), font_size = 0.8), (25, 35), (True, False)).set((10, 460), 7))

    BUTTONS_header.set(version = Button(Text(VERSION, Color(0, 75, 0), font_size = 1), Text(VERSION, Color(0, 125, 0), font_size = 1), alt_text = "About...").set((35, 25), 7, (True, True)))

def setup_page_home():
    global IMAGES_page, BUTTONS_page, TEXTS_page, SCROLLABLES_page, TEXTBOXES_page, VERSION_BUTTONS, PAGE

    draw_loading("loading versions...")

    PAGE = PAGES['home']

    IMAGES_page = Enum()
    BUTTONS_page = Enum()
    TEXTS_page = Enum()
    TEXTBOXES_page = {}

    IMAGES_page.set(logo = ScreenObject(Image("alpha_elements.png", (280, 280), plugin = "alpha_elements")).set((535, 450), 4, (True, False)))
    IMAGES_page.set(background = ScreenObject(Image("background_mesa.png", plugin = "alpha_elements")).set((70, 0), 2))

    IMAGES_page.set(fade = ScreenObject(Image("fade_down.png", plugin = "alpha_elements")).set((70, 240), 3))

    update_version_button()

    update_version_list()

    update_play_button()

    TEXTS_page.set(name = ScreenObject(Image("ae_text.png", (450, 150), plugin = "alpha_elements")).set((100, 700), 4, (False, False)))

def setup_page_mods():
    global IMAGES_page, BUTTONS_page, TEXTS_page, SCROLLABLES_page, TEXTBOXES_page, MOD_BUTTONS, MOD_LIST, PAGE

    draw_loading("loading mods...")

    read_mods()

    PAGE = PAGES['mods']

    IMAGES_page = Enum()
    BUTTONS_page = Enum()
    TEXTS_page = Enum()
    TEXTBOXES_page = {}

    TEXTS_page.set(heading = ScreenObject(Text("Mods", color = Color(0, 50, 0), font_size = 3)).set((100, 60), 4))

    BUTTONS_page.set(add = Button(Surface((60, 60), Color(0, 75, 0)), Surface((60, 60), Color(0, 150, 0)), alt_text = "Import .jar file").set((920, 60), 4))
    BUTTONS_page.add.blit_all(Text("+", color = Color(255, 255, 255), font_size = 2), (32, 30), (True, True))

    IMAGES_page.set(background = ScreenObject(Image("background_mesa_blur.png", plugin = "alpha_elements")).set((70, 0), 2))
    IMAGES_page.set(fade = ScreenObject(Image("fade_down.png", plugin = "alpha_elements")).set((70, 240), 3))

    MOD_BUTTONS = []
    MOD_LIST = []

    mod_size = 0
    for l in MODS:
        if l == CONFIG['version'] or l == "generic":
            for i in MODS[l]:
                mod_size += 30

    SCROLLABLES_page = {}
    SCROLLABLES_page.clear()
    SCROLLABLES_page = {"mods": ScrollableSurface((700, 800), (700, mod_size), Color(50, 50, 50, 50), [0, 0].copy()).set((100, 170), 5)}

    n = 0
    for l in MODS:
        if l == CONFIG['version'] or l == "generic":
            for i in MODS[l]:
                MOD_BUTTONS.append(True)
                update_mod_button(n, i)
                n += 1
                MOD_LIST.append(i)

def setup_page_about():
    global IMAGES_page, BUTTONS_page, TEXTS_page, SCROLLABLES_page, TEXTBOXES_page, MOD_BUTTONS, MOD_LIST, PAGE

    draw_loading("loading information...")

    PAGE = PAGES['about']

    IMAGES_page = Enum()
    BUTTONS_page = Enum()
    TEXTS_page = Enum()
    TEXTBOXES_page = {}
    SCROLLABLES_page = {}

    TEXTS_page.set(heading = ScreenObject(Text(f"AlphaElements Minecraft Launcher", color = Color(0, 50, 0), font_size = 2)).set((535, 80), 4, (True, False)))

    TEXTS_page.set(subtitle = ScreenObject(Text(f"release {VERSION}, date {RELEASEDATE}", color=Color(0, 50, 0), font_size = 1.5)).set((535, 200), 4, (True, False)))

    TEXTS_page.set(description = ScreenObject(Surface((900, 120))).set((535, 350), 4, (True, False)))

    for n, i in enumerate(
"""AlphaElements is a launcher for the default Minecraft Launcher. 
It automatically installs the modded Minecraft Forge client and the 
performance and tweak mod OptiFine. In AlphaElements you can import 
other mods and enable or disable them to your needs in different 
versions. When you're done, just launch the Minecraft Launcher 
using the Play button.""".split("\n")):
        TEXTS_page.description.blit(Text(i, color=Color(255, 255, 255), font_size=1), (450, n * 20), (True, False))

    TEXTS_page.set(license = ScreenObject(Surface((900, 360))).set((535, 560), 4, (True, False)))

    TEXTS_page.license.blit(Text("BSD 2-Clause License", color=Color(200, 200, 200), font_size=1), (450, 0), (True, False))
    TEXTS_page.license.blit(Text("Copyright (c) 2024 by diam0ndkiller", color=Color(0, 127, 127), font_size=1), (450, 30), (True, False))

    for n, i in enumerate(
"""Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.""".split("\n")):
        TEXTS_page.license.blit(Text(i, color=Color(200, 200, 200), font_size=0.75), (450, 60 + n * 15), (True, False))

    IMAGES_page.set(background = ScreenObject(Image("background_mesa_blur.png", plugin = "alpha_elements")).set((70, 0), 2))
    IMAGES_page.set(fade = ScreenObject(Image("fade_down.png", plugin = "alpha_elements")).set((70, 240), 3))


def update_version_button():
    global BUTTONS_page

    BUTTONS_page.set(choose_version = Button(Surface((300, 60), Color(0, 75, 0)), Surface((300, 60), Color(0, 150, 0)), alt_text = "Choose Minecraft Version").set((690, 60), 4))

    BUTTONS_page.choose_version.blit_all(Text(CONFIG['version'], color = Color(255, 255, 255), font_size = 2), (160, 30), (True, True))

    if choose_version:
        BUTTONS_page.choose_version.blit_all(Text(";         ", color = Color(255, 255, 255), font_size = 2), (150, 30), (True, True))
    else:
        BUTTONS_page.choose_version.blit_all(Text("\\         ", color = Color(255, 255, 255), font_size = 2), (150, 30), (True, True))

def update_version_list():
    global VERSION_BUTTONS, SCROLLABLES_page

    VERSION_BUTTONS = []

    version_size = 0
    for i in VERSIONS:
        version_size += 30

    SCROLLABLES_page = {}
    SCROLLABLES_page.clear()
    SCROLLABLES_page = {"versions": ScrollableSurface((300, 300), (300, version_size), Color(50, 50, 50, 50)).set((690, 120), 5)}

    n = 0
    for i in VERSIONS:
        installed = True
        tooltip = "Play " + i
        prefix = "[ ]"
        color = Color(200, 200, 200)
        if not i in CONFIG["profiles"]:
            tooltip = "Install " + i
            installed = False
            prefix = " + "
            color = Color(150, 150, 150)
        if i == CONFIG['version']:
            tooltip += " (selected)"
            prefix = "[X]"
            color = Color(255, 255, 255)
        VERSION_BUTTONS.append(Button(Surface((300, 30), Color(50, 50, 50)), Surface((300, 30), Color(0, 150, 0)), alt_text = tooltip).set_pos_screen((0, n * 30), SCROLLABLES_page['versions']))

        VERSION_BUTTONS[n].blit_all(Text(i, color, font_size=1), (150, 15), (True, True))

        VERSION_BUTTONS[n].blit_all(Text(prefix, color, font_size=1), (15, 15), (False, True))
        #VERSION_BUTTONS[n].blit_all(Image("not-installed.png" if not installed else "active.png" if i == CONFIG['version'] else "installed.png", plugin="alpha_elements"), (15, 15), (True, True))

        n += 1

def update_play_button():
    global BUTTONS_page, pro

    if pro and not pro.poll():
        BUTTONS_page.set(play=Button(Surface((400, 100), Color(50, 50, 50)), Surface((400, 100), Color(75, 75, 75)), alt_text = "Minecraft Launcher is already running").set((590, 890), 2))
        BUTTONS_page.play.blit_all(Text("---running---", color=Color(255, 255, 255), font_size=1), (200, 10), (True, True))
    else:
        BUTTONS_page.set(play=Button(Surface((400, 100), Color(0, 75, 0)), Surface((400, 100), Color(0, 150, 0)), alt_text = "Start Minecraft Launcher").set((590, 890), 2))

    BUTTONS_page.play.blit_all(Text("Play...", color = Color(255, 255, 255), font_size = 3), (200, 50), (True, True))

def update_mod_button(n: int, mod: Mod):
    global MOD_BUTTONS
    text = f"{mod.name} ({mod.version})"
    if str(mod) in str(CONFIG['profiles'][CONFIG['version']].mods):
        text = "[X] " + text
        tooltip = f"disable '{mod.name}'"
        color = Color(255, 255, 255)
    else:
        text = "[ ] " + text
        tooltip = f"enable '{mod.name}'"
        color = Color(200, 200, 200)
    MOD_BUTTONS[n] = Button(Surface((700, 30), Color(50, 50, 50)), Surface((700, 30), Color(0, 150, 0)), alt_text = tooltip).set_pos_screen((0, n * 30), SCROLLABLES_page['mods'])
    MOD_BUTTONS[n].blit_all(Text(text, color, font_size=1), (0, 15), (False, True))
    MOD_BUTTONS[n].n = n
    MOD_BUTTONS[n].mod = mod


def draw_loading(text = "loading..."):
    draw__clean(Color(0, 15, 0))
    draw_header()
    draw(ScreenObject(Text(text, Color(0, 100, 0))).set((WIDTH // 2, HEIGHT // 2), 7, (True, True)))
    draw__window()

def draw_header():
    global IMAGES_header, BUTTONS_header, TEXTS_header, SCROLLABLES_header

    draw(IMAGES_header.background)

    draw(TEXTS_header.name)

    draw(BUTTONS_header.version)

    #draw(BUTTONS_header.close)

    draw(BUTTONS_header.home)
    draw(BUTTONS_header.mods)
    draw(BUTTONS_header.resource_packs)

def draw_page_home():
    draw(IMAGES_page.background)
    draw(IMAGES_page.fade)

    draw(BUTTONS_page.choose_version)

    draw(IMAGES_page.logo)
    draw(TEXTS_page.name)

    if choose_version:
        SCROLLABLES_page['versions'].fill(Color(50, 50, 50, 50))
        for i in VERSION_BUTTONS:
            draw(i)
        draw(SCROLLABLES_page['versions'])

    draw(BUTTONS_page.play)

def draw_page_mods():
    draw(IMAGES_page.background)
    draw(IMAGES_page.fade)

    draw(BUTTONS_page.add)

    draw(TEXTS_page.heading)

    SCROLLABLES_page['mods'].fill(Color(50, 50, 50, 50))
    for i in MOD_BUTTONS:
        draw(i)
    draw(SCROLLABLES_page['mods'])

def draw_page_about():
    draw(IMAGES_page.background)
    draw(IMAGES_page.fade)

    draw(TEXTS_page.heading)
    draw(TEXTS_page.subtitle)

    draw(TEXTS_page.description)
    draw(TEXTS_page.license)
    #TODO


def quit():
    save_config()
    pg.quit()
    exit(0)

def play():
    global pro
    if pro: return
    if not CONFIG['version'] in CONFIG['profiles']: CONFIG['profiles'][CONFIG['version']] = Profile(CONFIG['version'])
    pro = CONFIG['profiles'][CONFIG['version']].launch()
    pg.display.iconify()


shift = False
loop = True

pro = False

PAGES = {None: -1, "home": 0, "mods": 1, "packs": 2, "about": 9}

PAGE = PAGES[None]

choose_version = False

setup_header()

draw_loading()

read_config()

read_mods()

get_forge_versions()

if not CONFIG['version'] in CONFIG['profiles']: CONFIG['profiles'][CONFIG['version']] = Profile(CONFIG['version'])

setup_page_home()

while loop:
    pg.time.Clock().tick(60)

    draw__clean(Color(0, 15, 0))

    if PAGE == PAGES['home']:
        draw_page_home()
    elif PAGE == PAGES['mods']:
        draw_page_mods()
    elif PAGE == PAGES['about']:
        draw_page_about()

    draw_header()

    draw__window()

    for event in pg.event.get():
        # testing if minecraft process ended
        #TODO
        if event.type == pg.WINDOWFOCUSGAINED and pro:
            time.sleep(1)
            update_play_button()
            if pro.poll():
                pro = False

        if event.type == pg.KEYDOWN:
            # quit on escape
            if event.key == pg.K_ESCAPE:
                quit()
            # detecting shift for horizontal scrolling
            if event.key == pg.K_LSHIFT or event.key == pg.K_RSHIFT:
                shift = True
            # taking screenshot on f2
            if event.key == pg.K_F2:
                screenshot("alpha-elements-launcher")
            # scroll in ScrollableSurface with arrow keys when mouse in boundaries
            for k, i in SCROLLABLES_page.items():
                if isinstance(i, ScrollableSurface) and i.get_mouse_collision():
                    if event.key == pg.K_DOWN:
                        i.scroll(int(FACTOR * 10), 0)
                    elif event.key == pg.K_UP:
                        i.scroll(-int(FACTOR * 10), 0)
                    if event.key == pg.K_RIGHT:
                        i.scroll(0, int(FACTOR * 10))
                    elif event.key == pg.K_LEFT:
                        i.scroll(0, -int(FACTOR * 10))
                    break

        if event.type == pg.QUIT:
            quit()

        if event.type == pg.KEYUP:
            # detecting shift for horizontal scrolling
            if event.key == pg.K_LSHIFT or event.key == pg.K_RSHIFT:
                shift = False

        if event.type == pg.MOUSEBUTTONUP:
            # normal mouse press
            if event.button == 1:
                # switch to home page
                if BUTTONS_header.home.get_mouse_collision():
                    setup_page_home()
                    continue
                # switch to mods page
                elif BUTTONS_header.mods.get_mouse_collision():
                    choose_version = False
                    setup_page_mods()
                    continue
                # switch to about page
                elif BUTTONS_header.version.get_mouse_collision():
                    choose_version = False
                    setup_page_about()
                    continue

            # scroll in ScrollableSurface
            if event.button == 5 or event.button == 4:
                for k, i in SCROLLABLES_page.items():
                    if isinstance(i, ScrollableSurface) and i.get_mouse_collision():
                        if shift:
                            if event.button == 5:
                                i.scroll(int(FACTOR * SCROLL_SPEED), 0)
                            elif event.button == 4:
                                i.scroll(-int(FACTOR * SCROLL_SPEED), 0)
                        else:
                            if event.button == 5:
                                i.scroll(0, int(FACTOR * SCROLL_SPEED))
                            elif event.button == 4:
                                i.scroll(0, -int(FACTOR * SCROLL_SPEED))
                        break

        # if on home page
        if PAGE == PAGES['home']:
            if event.type == pg.MOUSEBUTTONUP:
                # open version list
                if BUTTONS_page.choose_version.get_mouse_collision():
                    if event.button == 1:
                        choose_version = not choose_version
                        update_version_button()
                # launch minecraft
                elif BUTTONS_page.play.get_mouse_collision():
                    play()
                # choosing profile
                elif choose_version:
                    for i in VERSION_BUTTONS:
                        if i.get_mouse_collision():
                            # select (or create) profile
                            if event.button == 1:
                                same_selection = CONFIG['version'] == Profile(i.element_list[0][0].element_list[0][0].text).version
                                CONFIG['version'] = Profile(i.element_list[0][0].element_list[0][0].text).version
                                choose_version = False
                                update_version_button()
                                if not CONFIG['version'] in CONFIG['profiles']:
                                    CONFIG['profiles'][CONFIG['version']] = Profile(CONFIG['version'])
                                    setup_page_home()
                                elif not same_selection:
                                    update_version_list()
                                save_config()
                            # delete profile
                            elif event.button == 2:
                                if i.element_list[0][0].element_list[0][0].text in CONFIG['profiles']: CONFIG['profiles'].pop(i.element_list[0][0].element_list[0][0].text)
                                choose_version = False
                                update_version_button()
                                save_config()
                                update_version_list()

        # if on mods page
        elif PAGE == PAGES['mods']:
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    # add a mod
                    if BUTTONS_page.add.get_mouse_collision():
                        import_mod()
                    # select / deselect a mod
                    for i in MOD_BUTTONS:
                        if i.get_mouse_collision():
                            if str(i.mod) in CONFIG['profiles'][CONFIG['version']].mods: CONFIG['profiles'][CONFIG['version']].mods.remove(str(i.mod))
                            else: CONFIG['profiles'][CONFIG['version']].mods.append(str(i.mod))
                            save_config()
                            update_mod_button(i.n, i.mod)
