# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

init python:
    import os, shutil, zipfile, glob, hashlib

    def ext_move(ext, path):
        for file in os.listdir(ext + path):
            src_file = os.path.join(ext + path, file)
            if renpy.macintosh:
                dst_file = os.path.join(project_dir + '/DDLC.app/Contents/Resources/autorun/' + path, file)
            else:
                dst_file = os.path.join(project_dir + path, file)
            shutil.move(src_file, dst_file)

    def rpy_ext(ext):
        for file in os.listdir(ext):
            base = [".exe", ".sh", ".py", ".txt", ".md", ".html", ".app"]
            if file.endswith(tuple(base)):
                src = os.path.join(ext, file)
                dst = os.path.join(project_dir, file)
                shutil.move(src, dst)

    def lib_move(ext):
        for file in os.listdir(ext + '/lib'):
            src_file = os.path.join(ext + '/lib', file)
            if renpy.macintosh:
                dst_file = os.path.join(project_dir + '/DDLC.app/Contents/MacOS/lib', file)
            else:
                dst_file = os.path.join(project_dir + '/lib', file)
            shutil.move(src_file, dst_file)     

    def rpy_move(ext):
        for file in os.listdir(ext + '/renpy'):
            src_file = os.path.join(ext + '/renpy', file)
            if renpy.macintosh:
                dst_file = os.path.join(project_dir + '/DDLC.app/Contents/Resources/autorun/renpy', file)
            else:
                dst_file = os.path.join(project_dir + '/renpy', file)
            shutil.move(src_file, dst_file)

    def reg_move(mzt, ext):
        for file in os.listdir(mzt + '/game'):
            src_file = os.path.join(mzt + ext, file)
            if renpy.macintosh:
                dst_file = os.path.join(project_dir + '/DDLC.app/Contents/Resources/autorun/game', file)
            else:
                dst_file = os.path.join(project_dir + '/game', file)
            shutil.move(src_file, dst_file)

    def zip_extract():
        if renpy.macintosh:
            sha = 'abc3d2fee9433ad454decd15d6cfd75634283c17aa3a6ac321952c601f7700ec'
        else:
            sha = '2a3dd7969a06729a32ace0a6ece5f2327e29bdf460b8b39e6a8b0875e545632e'
        
        path = open(persistent.zip_directory, 'rb')
        if hashlib.sha256(path.read()).hexdigest() != sha:
            interface.error(_("The DDLC ZIP file chosen is not official. Download a official DDLC ZIP file from {a=https://ddlc.moe}DDLC's website{/a}, select it in Settings, and try again."))
        path.close() # JIC
        
        with zipfile.ZipFile(persistent.zip_directory, "r") as z:
            z.extractall(persistent.projects_directory + "/temp")
            if renpy.macintosh:
                ddlc = persistent.projects_directory + '/temp'
            else:
                ddlc = persistent.projects_directory + '/temp/DDLC-1.1.1-pc'
        shutil.move(ddlc, project_dir)
    
    def steam_copy():
        try:
            shutil.copytree(persistent.zip_directory + "/Doki Doki Literature Club", project_dir)
        except:
            interface.error(_("Cannot Locate your Doki Doki Literature Club Folder"), _("Make sure it is set to your 'Steam\steamapps\common' folder."),)

    def ddlc_copy():
        if not glob.glob(persistent.zip_directory + "/ddlc-mac/DDLC.app"):
            interface.error(_("Cannot find DDLC.app."), _("Please make sure that your OS and ZIP Directory settings are set correctly."))
        
        sha = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        path = open(persistent.zip_directory + "/ddlc-mac/DDLC.app", 'rb')
        if hashlib.sha256(path.read()).hexdigest() != sha:
            interface.error(_("The DDLC.app file downloaded is not official. Download a official DDLC ZIP file from {a=https://ddlc.moe}DDLC's website{/a} and try again."))
        path.close()

        shutil.copytree(persistent.zip_directory, project_dir)
    
    def modzip_extract(path):
        with zipfile.ZipFile(path, "r") as z:
            z.extractall(persistent.projects_directory + "/temp")

    def modzip_copy(path):
        shutil.copytree(path, persistent.projects_directory + '/temp')

# Code to add a mod
label add_a_mod:
    # Checks if user set Mod Install Folder
    if persistent.projects_directory is None:
        call choose_projects_directory
    # Ren'Py Failsafe
    if persistent.projects_directory is None:
        $ interface.error(_("The Mod directory could not be set. Giving up."))
    # Browser Set?
    if renpy.macintosh:
        if persistent.safari is None:
            call auto_extract
        if persistent.safari is None:
            $ interface.error(_("Couldn't check if OS auto-extracts ZIPs. Please reconfigure your settings."))
    # Checks if user set DDLC ZIP Location (All OS)
    if persistent.zip_directory is None:
        call ddlc_location
    # Ren'Py Failsafe 2
    if persistent.zip_directory is None:
        $ interface.error(_("The DDLC copy directory could not be set. Giving up."))
    if persistent.mzip_directory is None:
        call choose_modzip_directory
    if persistent.mzip_directory is None:
        $ interface.error(_("The Mod ZIP directory could not be set. Giving up."))

    python:
        modinstall_foldername = ""
        while True:
            # Asks User the name of the folder they want their mod folder to be
            modinstall_foldername = interface.input(
                _("Mod Folder Name"),
                _("Please enter the name of the mod you are installing:"),
                allow=interface.PROJECT_LETTERS,
                cancel=Jump("front_page"),
                default=modinstall_foldername,
            )

            modinstall_foldername = modinstall_foldername.strip()

            if not modinstall_foldername:
                interface.error(_("The mod name may not be empty."), label=None)
                continue
            if modinstall_foldername == "launcher":
                interface.error(_("'launcher' is a reserved mod name. Please choose a different mod name."), label=None)
                continue

            project_dir = os.path.join(persistent.projects_directory, modinstall_foldername)

            if project.manager.get(modinstall_foldername) is not None:
                interface.error(_("[modinstall_foldername!q] already exists. Please choose a different project name."), modinstall_foldername=modinstall_foldername, label=None)
                continue
            if os.path.exists(project_dir):
                interface.error(_("[project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir, label=None)
                continue

            if renpy.macintosh and persistent.safari == True:
                interface.interaction(_("Making a Mod Folder"), _("Copying DDLC, Please Wait..."),)
                ddlc_copy(project_dir)
            else:
                interface.interaction(_("Making a Mod Folder"), _("Extracting DDLC, Please Wait..."),)
                if not renpy.macintosh:
                    # Asks if the copy is Steam
                    if persistent.steam_release == True:
                        # Copy DDLC (Steam Release) (Assuming Steam Copy is Unmodded)
                        steam_copy()
                    else:
                        # Extract DDLC (Moe Release)
                        zip_extract()
                else:
                    zip_extract()

            # RPA Download Install Check (for mods that aren't in ZIPs or downloaded as seperate .rpas)
            if glob.glob(persistent.mzip_directory + '/*.rpa'):
                interface.interaction(_("Copying"), _("Copying Mod Files from Mod ZIP Directory, Please Wait..."),)
                for file in os.listdir(persistent.mzip_directory):
                    if file.endswith('.rpa'):
                        src = os.path.join(persistent.mzip_directory, file)
                        if renpy.macintosh:
                            shutil.move(src, project_dir + '/DDLC.app/Contents/Resources/autorun/game')
                        else:
                            shutil.move(src, project_dir + '/game')
                # Auto-Refresh
                project.manager.scan()
                renpy.jump("front_page")

            # Asks User name of ZIP
            if renpy.macintosh and persistent.safari == True:
                interface.interaction(_("Mod to Install Folder"), _("Please choose the the mod folder you wish to install."),)
                
                path, is_default = choose_directory(persistent.mzip_directory)

            else:
                interface.interaction(_("Mod ZIP File"), _("Please choose the mod ZIP file you wish to install."),)

                path, is_default = choose_file(persistent.mzip_directory)

            if is_default:
                shutil.rmtree(project_dir)
                interface.error(_("The operation has been cancelled."))
                renpy.jump("front_page")

            modzip_path = path

            if renpy.macintosh and persistent.safari:
                interface.interaction(_("Copying"), _("Copying Mod Files, Please Wait..."),)
                modzip_copy(modzip_path)
            else:
                # Extract Mod
                interface.interaction(_("Extracting"), _("Extracting Mod ZIP, Please Wait..."),)
                modzip_extract(modzip_path)

            # Search for if there is a folder in /temp that isn't mod related (Yuri-1.0)
            mzt = persistent.projects_directory + "/temp"
            mzte = [x[0] for x in os.walk(mzt)]
            try:
                mzte[1]
                if str(mzte[1]).endswith('-Mod') or str(mzte[1]).endswith('-pc') or str(mzte[1]).endswith('-mac') or str(mzte[1]).endswith('-Renpy7Mod'):
                    mztex = True
                else:
                    mztex = False
            # if there is no folders in there
            except IndexError:
                # return false for advanced scan
                mztex = False
            if mztex == False:
                # if folder inside is /game to move to mod folder
                if glob.glob(mzt + '/characters'):
                    reg_move(mzt, '/characters')
                if glob.glob(mzt + '/lib'):
                    lib_move('/lib')
                if glob.glob(mzt + '/renpy'):
                    rpy_move('/renpy')
                    rpy_ext(mzt)
                if glob.glob(mzt + '/game'):
                    reg_move(mzt, '/game')
                else:
                    # move mod files to the /game folder or mod folder
                    for file in os.listdir(mzt):
                        src_file = os.path.join(mzt, file)
                        if renpy.macintosh:
                            dst_file = os.path.join(project_dir + '/DDLC.app/Contents/Resources/autorun/game', file)
                        else:
                            dst_file = os.path.join(project_dir + '/game', file)
                        shutil.move(src_file, dst_file)
            else:
                #Extended Scanning (If Contents during extract are inside another folder (Yuri-1.0/script-ch1.rpyc))
                # if folder inside is /game to move to mod folder
                if glob.glob(str(mzte[1]) + '/characters'):
                    ext_move(str(mzte[1]), '/characters')
                if glob.glob(str(mzte[1]) + '/lib'):
                    lib_move(str(mzte[1]))
                if glob.glob(str(mzte[1]) + '/renpy'):
                    rpy_move(str(mzte[1]))
                    rpy_ext(str(mzte[1]))
                if glob.glob(str(mzte[1]) + '/game'):
                    ext_move(str(mzte[1]),'/game')
                else:
                    for file in os.listdir(str(mzte[1])):
                        src_file = os.path.join(str(mzte[1]), file)
                        if renpy.macintosh:
                            dst_file = os.path.join(project_dir + '/DDLC.app/Contents/Resources/autorun/game', file)
                        else:
                            dst_file = os.path.join(project_dir + '/game', file)
                        shutil.move(src_file, dst_file)

            # Prevents copy of any other RPA or other mod files
            shutil.rmtree(persistent.projects_directory + '/temp')
            # Auto-Refresh
            project.manager.scan()
            break
        
    jump front_page

# Code to install DDLC only
label add_base_game:
    # Checks if user set Mod Install Folder
    if persistent.projects_directory is None:
        call choose_projects_directory
    # Ren'Py Failsafe
    if persistent.projects_directory is None:
        $ interface.error(_("The Mod directory could not be set. Giving up."))
    # Browser Set?
    if renpy.macintosh:
        if persistent.safari is None:
            call auto_extract
        if persistent.safari is None:
            $ interface.error(_("Couldn't check if OS auto-extracts ZIPs. Please reconfigure your settings."))
    # Checks if user set DDLC ZIP Location (All OS)
    if persistent.zip_directory is None:
        call ddlc_location
    # Ren'Py Failsafe 2
    if persistent.zip_directory is None:
        $ interface.error(_("The DDLC copy directory could not be set. Giving up."))

    python:
        modinstall_foldername = ""
        while True:
            # Asks User the name of the folder they want their mod folder to be
            modinstall_foldername = interface.input(
                _("Mod Folder Name"),
                _("Please enter the name of the mod you are installing:"),
                allow=interface.PROJECT_LETTERS,
                cancel=Jump("front_page"),
                default=modinstall_foldername,
            )

            modinstall_foldername = modinstall_foldername.strip()

            if not modinstall_foldername:
                interface.error(_("The mod name may not be empty."), label=None)
                continue
            if modinstall_foldername == "launcher":
                interface.error(_("'launcher' is a reserved mod name. Please choose a different mod name."), label=None)
                continue

            project_dir = os.path.join(persistent.projects_directory, modinstall_foldername)

            if project.manager.get(modinstall_foldername) is not None:
                interface.error(_("[modinstall_foldername!q] already exists. Please choose a different project name."), modinstall_foldername=modinstall_foldername, label=None)
                continue
            if os.path.exists(project_dir):
                interface.error(_("[project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir, label=None)
                continue

            if renpy.macintosh and persistent.safari == True:
                interface.interaction(_("Making a Mod Folder"), _("Copying DDLC, Please Wait..."),)
                ddlc_copy(project_dir)
            else:
                interface.interaction(_("Making a Mod Folder"), _("Extracting DDLC, Please Wait..."),)
                if not renpy.macintosh:
                    # Asks if the copy is Steam
                    if persistent.steam_release == True:
                        # Copy DDLC (Steam Release) (Assuming Steam Copy is Unmodded)
                        steam_copy()
                    else:
                        # Extract DDLC (Moe Release)
                        zip_extract()
                else:
                    zip_extract()
            
            # Prevents copy of any other RPA or other mod files
            shutil.rmtree(persistent.projects_directory + '/temp')
            project.manager.scan()
            break
    jump front_page