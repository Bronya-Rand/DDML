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
    import os
    import shutil
    import zipfile
    import glob

    def ext_move(project, ext, path):
        if renpy.macintosh:
            if os.path.exists(project + '/DDLC.app/Contents/Resources/autorun/game/python-packages'):
                if os.path.exists(ext + path + '/python-packages'):
                    shutil.rmtree(project + '/DDLC.app/Contents/Resources/autorun/game/python-packages')
                else:
                    pass
            for file in os.listdir(ext + path):
                print file
                src_file = os.path.join(ext + path, file)
                dst_file = os.path.join(project + '/DDLC.app/Contents/Resources/autorun/' + path, file)
            shutil.move(src_file, dst_file)
        else:
            if os.path.exists(project + '/game/python-packages'):
                if os.path.exists(ext + path + '/python-packages'):
                    shutil.rmtree(project + '/game/python-packages')
                else:
                    pass
            for file in os.listdir(ext + path):
                print file
                src_file = os.path.join(ext + path, file)
                dst_file = os.path.join(project + path, file)
                shutil.move(src_file, dst_file)

    def rpy_ext(project, ext):
        for file in os.listdir(ext):
            base = [".exe", ".sh", ".py", ".txt", ".md", ".html", ".app"]
            if file.endswith(tuple(base)):
                src = os.path.join(ext, file)
                shutil.move(src, project)

    def lib_move(project, ext):
        if renpy.macintosh:
            shutil.rmtree(project + '/DDLC.app/Contents/MacOS/lib')
            for file in os.listdir(ext + '/lib'):
                print file
                src_file = os.path.join(ext + '/lib', file)
                dst_file = os.path.join(project + '/DDLC.app/Contents/MacOS/lib', file)
        else:
            shutil.rmtree(project + '/lib')
            for file in os.listdir(ext + '/lib'):
                print file
                src_file = os.path.join(ext + '/lib', file)
                dst_file = os.path.join(project + '/lib', file)
                shutil.move(src_file, dst_file)

    def rpy_move(project, ext):
        if renpy.macintosh:
            for file in os.listdir(project + '/DDLC.app/Contents/Resources/autorun/renpy'):
                file_path = os.path.join(project + '/DDLC.app/Contents/Resources/autorun/renpy', file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): 
                shutil.rmtree(file_path)
            for file in os.listdir(ext + '/renpy'):
                print file
                src_file = os.path.join(ext + '/renpy', file)
                dst_file = os.path.join(project + '/DDLC.app/Contents/Resources/autorun/renpy', file)
            shutil.move(src_file, dst_file)
        else:
            for file in os.listdir(project + '/renpy'):
                file_path = os.path.join(project + '/renpy', file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): 
                    shutil.rmtree(file_path)
            for file in os.listdir(ext + '/renpy'):
                print file
                src_file = os.path.join(ext + '/renpy', file)
                dst_file = os.path.join(project + '/renpy', file)
                shutil.move(src_file, dst_file)

    def reg_move(project, mzt, ext):
        if renpy.macintosh:
            if os.path.exists(project + '/DDLC.app/Contents/Resources/autorun/game/python-packages'):
                if os.path.exists(mzt + '/python-packages'):
                    shutil.rmtree(project + '/DDLC.app/Contents/Resources/autorun/game/python-packages')
            shutil.move(mzt + ext, project + '/DDLC.app/Contents/Resources/autorun')
        else:
            if os.path.exists(project + '/game/python-packages'):
                if os.path.exists(mzt + '/python-packages'):
                    shutil.rmtree(project+ '/game/python-packages')
            shutil.move(mzt + ext, project_dir)

    def zip_extract(project):
        if renpy.macintosh:
            try: 
                with zipfile.ZipFile(persistent.zip_directory, "r") as z:
                    z.extractall(persistent.projects_directory + "/temp")
                    ddlc = persistent.projects_directory + '/temp'
                    shutil.move(ddlc, project)
            except: 
                interface.error(_("Cannot Locate 'ddlc-mac.zip' in [persistent.zip_directory!q]."), _("Make sure you have DDLC downloaded from 'https://ddlc.moe' and check if it exists."),)
        else:
            try: 
                with zipfile.ZipFile(persistent.zip_directory, "r") as z:
                    z.extractall(persistent.projects_directory + "/temp")
                    ddlc = persistent.projects_directory + '/temp' + '/DDLC-1.1.1-pc'
                    shutil.move(ddlc, project)
            except: 
                interface.error(_("Cannot Locate 'ddlc-win.zip' in [persistent.zip_directory!q]."), _("Make sure you have DDLC downloaded from 'https://ddlc.moe' and check if it exists."),)
    
    def steam_copy(project):
        try:
            shutil.copytree(persistent.zip_directory + "/Doki Doki Literature Club", project)
        except:
            interface.error(_("Cannot Locate Your Doki Doki Literature Club Folder"), _("Make sure it is set to your 'Steam\steamapps\common' folder."),)

    def ddlc_copy(project):
        import shutil
        try:
            shutil.copytree(persistent.zip_directory, project)
        except:
            interface.error(_("Cannot find DDLC.app."). _("Please make sure your OS and ZIP Directory are set correctly."),)
    
    def modzip_extract(project, name):
        try:
            with zipfile.ZipFile(name, "r") as z:
                z.extractall(persistent.projects_directory + "/temp")
        except:
            shutil.rmtree(project)
            interface.error(_("Cannot locate ZIP in [persistent.mzip_directory!q]."), _("Check the name of your Mod ZIP file and try again."))

    def modzip_copy(project, name):
        import shutil
        try:
            shutil.copytree(persistent.mzip_directory, persistent.projects_directory + '/temp/' + name)
        except:
            shutil.rmtree(project)
            interface.error(_("Cannot find Folder in [persistent.mzip_directory!q]."), _("Check the name of your Mod Folder extracted by MacOS and try again."))

# Code to add a mod
label add_a_mod:
    # Checks if user set Mod Install Folder
    if persistent.projects_directory is None:
        call choose_projects_directory
    # Ren'Py Failsafe
    if persistent.projects_directory is None:
        $ interface.error(_("The Mod directory could not be set. Giving up."))
    # Browser Set?
    if renpy.macintosh and persistent.safari is None:
        call browser
    # Ren'Py Failsafe
    if renpy.macintosh and persistent.safari is None:
        $ interface.error(_("The browser could not be set. Giving up."))
    # Checks if user set DDLC ZIP Location (All OS)
    if persistent.zip_directory is None:
        if renpy.macintosh:
            call choose_zip_directory
        else:
            call ddlc_location
    # Ren'Py Failsafe 2
    if persistent.zip_directory is None:
        $ interface.error(_("The DDLC Copy directory could not be set. Giving up."))

    python:
        import glob
        import shutil
        import os
        # Asks User the name of the folder they want their mod folder to be
        modinstall_foldername = interface.input(
            _("Mod Folder Name"),
            _("Please enter the name of the mod you are installing:"),
            filename=True,
            cancel=Jump("front_page"))

        modinstall_foldername = modinstall_foldername.strip()
        if not modinstall_foldername:
            interface.error(_("The mod name may not be empty."))

        project_dir = os.path.join(persistent.projects_directory, modinstall_foldername)

        if project.manager.get(modinstall_foldername) is not None:
            interface.error(_("[modinstall_foldername!q] already exists. Please choose a different project name."), modinstall_foldername=modinstall_foldername)
        if os.path.exists(project_dir):
            interface.error(_("[project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir)

        if renpy.macintosh:
            if persistent.safari == False:
                #Chrome/Firefox (Safari Safe Mode Off)
                interface.interaction(_("Making a DDLC Folder"), _("Extracting DDLC, Please Wait..."),)
                zip_extract(project_dir)
            else:
                interface.interaction(_("Making a DDLC Folder"), _("Copying DDLC, Please Wait..."),)
                ddlc_copy(project_dir)
        else:
            interface.interaction(_("Making a Mod Folder"), _("Extracting DDLC, Please Wait..."),)
            # Asks if the copy is Steam
            if persistent.steam_release == True:
                # Copy DDLC (Steam Release) (Assuming Steam Copy is Unmodded)
                steam_copy(project_dir)
            else:
                # Extract DDLC (Moe Release)
                zip_extract(project_dir)
        # RPA Download Install Check (for mods that aren't in ZIPs or downloaded as seperate .rpas)
        if glob.glob(persistent.mzip_directory + '/*.rpa'):
            if renpy.macintosh:
                interface.interaction(_("Copying"), _("Copying Mod Files from Mod ZIP Directory, Please Wait..."),)
                for file in os.listdir(persistent.mzip_directory):
                    if file.endswith('.rpa'):
                        src = os.path.join(persistent.mzip_directory, file)
                        shutil.copy(src, project + '/DDLC.app/Contents/Resources/autorun/game')
                        os.remove(src)
            else:
                if glob.glob(persistent.mzip_directory + '/*.rpa'):
                    interface.interaction(_("Copying"), _("Copying Mod Files from Mod ZIP Directory, Please Wait..."),)
                    for file in os.listdir(persistent.mzip_directory):
                        if file.endswith('.rpa'):
                            src = os.path.join(persistent.mzip_directory, file)  
                            shutil.copy(src, project + '/game')
                            os.remove(src)
            # Auto-Refresh
            project.manager.scan()
            renpy.jump("front_page")

        # Asks User name of ZIP
        if renpy.macintosh and persistent.safari == True:
            interface.interaction(_("Mod to Install Folder"), _("Please choose the the mod to install folder."),)
            try:
                path, is_default = choose_directory(persistent.mzip_directory)
            except TypeError: #JIC
                shutil.rmtree(project_dir)
                interface.error(_("The operation has been cancelled."))
                renpy.jump("front_page")

            if is_default:
                shutil.rmtree(project_dir)
                interface.error(_("The operation has been cancelled."))
                renpy.jump("front_page")

            modzip_name = path
        else:
            interface.interaction(_("Mod ZIP File"), _("Please choose the mod file using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"),)

            try:
                path, is_default = choose_file(persistent.mzip_directory)
            except TypeError:
                shutil.rmtree(project_dir)
                interface.error(_("The operation has been cancelled."))
                renpy.jump("front_page")

            modzip_name = path

        modzip_name = modzip_name.strip()
        if not modzip_name:
            shutil.rmtree(project_dir)
            interface.error(_("The mod zip name may not be empty."))
        if renpy.macintosh:
            if persistent.safari == False:
                interface.interaction(_("Extracting Mod"), _("Extracting Mod ZIP, Please Wait..."),)
                modzip_extract(project_dir, modzip_name)
            else:
                interface.interaction(_("Copying Mod"), _("Copying Mod, Please Wait..."),)
                modzip_copy(project_dir, modzip_name)
        else:
            # Extract Mod
            interface.interaction(_("Extracting"), _("Extracting Mod ZIP, Please Wait..."),)
            modzip_extract(project_dir, modzip_name)
        # Search for if there is a folder in /temp that isn't mod related (Yuri-1.0)
        mzt = persistent.projects_directory + "/temp"
        mzte = [x[0] for x in os.walk(mzt)]
        try:
            mzte[1]
            if str(mzte[1]).endswith('-Mod') or str(mzte[1]).endswith('-pc') or str(mzte[1]).endswith('-mac'):
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
                reg_move(project_dir, mzt, '/characters')
            if glob.glob(mzt + '/lib'):
                lib_move(project_dir, '/lib')
            if glob.glob(mzt + '/renpy'):
                rpy_move(project_dir,'/renpy')
                rpy_ext(project_dir, mzt)
            if glob.glob(mzt + '/game'):
                reg_move(project_dir, mzt, '/game')
            else:
                if renpy.macintosh:
                    if os.path.exists(project_dir + '/DDLC.app/Contents/Resources/autorun/game/python-packages'):
                        if os.path.exists(mzt + '/python-packages'):
                            shutil.rmtree(project_dir + '/DDLC.app/Contents/Resources/autorun/game/python-packages')
                        else:
                            pass
                else:
                    # move mod files to the /game folder or mod folder
                    for file in os.listdir(mzt):
                        print file
                        src_file = os.path.join(mzt, file)
                        dst_file = os.path.join(project_dir + '/DDLC.app/Contents/Resources/autorun/game', file)
                        shutil.move(src_file, dst_file)
                    if os.path.exists(project_dir + '/game/python-packages'):
                        if os.path.exists(mzt + '/python-packages'):
                            shutil.rmtree(project_dir + '/game/python-packages')
                        else:
                            pass
                    # move mod files to the /game folder or mod folder
                    for file in os.listdir(mzt):
                        print file
                        src_file = os.path.join(mzt, file)
                        dst_file = os.path.join(project_dir + '/game', file)
                        shutil.move(src_file, dst_file)
        else:
            #Extended Scanning (If Contents during extract are inside another folder (Yuri-1.0/script-ch1.rpyc))
            # if folder inside is /game to move to mod folder
            if glob.glob(str(mzte[1]) + '/characters'):
                ext_move(project_dir, str(mzte[1]), '/characters')
            if glob.glob(str(mzte[1]) + '/lib'):
                lib_move(project_dir, str(mzte[1]))
            if glob.glob(str(mzte[1]) + '/renpy'):
                rpy_move(project_dir, str(mzte[1]))
                rpy_ext(project_dir, str(mzte[1]))
            if glob.glob(str(mzte[1]) + '/game'):
                ext_move(project_dir, str(mzte[1]),'/game')
            else:
                if renpy.macintosh:
                    # move mod files to the /game folder or mod folder
                    if os.path.exists(project_dir + '/DDLC.app/Contents/Resources/autorun/game/python-packages'):
                        if os.path.exists(str(mzte[1]) + '/python-packages'):
                            shutil.rmtree(project_dir + '/DDLC.app/Contents/Resources/autorun/game/python-packages')
                        else:
                            pass
                    import os
                    for file in os.listdir(str(mzte[1])):
                        print file
                        src_file = os.path.join(str(mzte[1]), file)
                        dst_file = os.path.join(project_dir + '/DDLC.app/Contents/Resources/autorun/game', file)
                        shutil.move(src_file, dst_file)
                else:
                    # move mod files to the /game folder or mod folder
                    if os.path.exists(project_dir + '/game/python-packages'):
                        if os.path.exists(str(mzte[1]) + '/python-packages'):
                            shutil.rmtree(project_dir + '/game/python-packages')
                        else:
                            pass
                    import os
                    for file in os.listdir(str(mzte[1])):
                        print file
                        src_file = os.path.join(str(mzte[1]), file)
                        dst_file = os.path.join(project_dir + '/game', file)
                        shutil.move(src_file, dst_file)

        # Prevents copy of any other RPA or other mod files
        shutil.rmtree(persistent.projects_directory + '/temp')
        # Auto-Refresh
        project.manager.scan()
        
    jump front_page

# Add-On Installation for some mods (BETA)
label install_addon:
    # Checks if user set Mod Install Folder
    if persistent.projects_directory is None:
        call choose_projects_directory
    # Ren'Py Failsafe
    if persistent.projects_directory is None:
        $ interface.error(_("The Mod directory could not be set. Giving up."))
    # Browser Set?
    if renpy.macintosh and persistent.safari is None:
        call browser
    # Ren'Py Failsafe
    if renpy.macintosh and persistent.safari is None:
        $ interface.error(_("The browser could not be set. Giving up."))
    # Checks if user set DDLC ZIP Location (All OS)
    if persistent.zip_directory is None:
        if renpy.macintosh:
            call choose_zip_directory
        else:
            call ddlc_location
    # Ren'Py Failsafe 2
    if persistent.zip_directory is None:
        $ interface.error(_("The DDLC Copy directory could not be set. Giving up."))

    python:
        interface.info("Please note that the Add-On installer is in beta and may not work. \nContact the Mod Dev if you face any bugs.")
        import os
        import glob
        import shutil
        # Asks ZIP name of add-on
        if renpy.macintosh and persistent.safari == True:
            interface.interaction(_("Mod to Install Folder"), _("Please choose the the mod to install folder."),)
            try:
                path, is_default = choose_directory(persistent.mzip_directory)
            except TypeError: #JIC
                shutil.rmtree(project_dir)
                interface.error(_("The operation has been cancelled."))
                renpy.jump("front_page")

            if is_default:
                shutil.rmtree(project_dir)
                interface.error(_("The operation has been cancelled."))
                renpy.jump("front_page")

            modzip_name = path
        else:
            interface.interaction(_("Mod ZIP File"), _("Please choose the mod file using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"),)

            try:
                path, is_default = choose_file(persistent.mzip_directory)
            except TypeError:
                shutil.rmtree(project_dir)
                interface.error(_("The operation has been cancelled."))
                renpy.jump("front_page")

            modzip_name = path
            
        modzip_name = modzip_name.strip()
        if not modzip_name:
            interface.error(_("The mod add-on zip name may not be empty."))
        project_dir = os.path.join(persistent.projects_directory, project.current.name)
        if renpy.macintosh:
            # Extract Mod
            if persistent.safari == False:
                interface.interaction(_("Extracting"), _("Extracting Mod Update/Add-On ZIP, Please Wait..."),)
                modzip_extract(modzip_name)
            else:
                interface.interaction(_("Copying Mod"), _("Copying Mod Update/Add-On, Please Wait..."),)
                modzip_copy(modzip_name)
        else:
            # Extract Mod
            interface.interaction(_("Extracting"), _("Extracting Mod ZIP, Please Wait..."),)
            modzip_extract(modzip_name)
        # Search for if there is a folder in /temp that isn't mod related (Yuri-1.0)
        mzt = persistent.projects_directory + "/temp"
        mzte = [x[0] for x in os.walk(mzt)]
        try:
            mzte[1]
            if str(mzte[1]).endswith('-Mod') or str(mzte[1]).endswith('-pc') or str(mzte[1]).endswith('-mac'):
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
                reg_move(project_dir, mzt, '/characters')
            if glob.glob(mzt + '/lib'):
                lib_move(project_dir, '/lib')
            if glob.glob(mzt + '/renpy'):
                rpy_move('/renpy')
                rpy_ext(project_dir, mzt)
            if glob.glob(mzt + '/game'):
                reg_move(project_dir, mzt, '/game')
            else:
                if renpy.macintosh:
                    if os.path.exists(project_dir + '/DDLC.app/Contents/Resources/autorun/game/python-packages'):
                        if os.path.exists(mzt + '/python-packages'):
                            shutil.rmtree(project_dir + '/DDLC.app/Contents/Resources/autorun/game/python-packages')
                        else:
                            pass
                else:
                    # move mod files to the /game folder or mod folder
                    for file in os.listdir(mzt):
                        print file
                        src_file = os.path.join(mzt, file)
                        dst_file = os.path.join(project_dir + '/DDLC.app/Contents/Resources/autorun/game', file)
                        shutil.move(src_file, dst_file)
                    if os.path.exists(project_dir + '/game/python-packages'):
                        if os.path.exists(mzt + '/python-packages'):
                            shutil.rmtree(project_dir + '/game/python-packages')
                        else:
                            pass
                    # move mod files to the /game folder or mod folder
                    for file in os.listdir(mzt):
                        print file
                        src_file = os.path.join(mzt, file)
                        dst_file = os.path.join(project_dir + '/game', file)
                        shutil.move(src_file, dst_file)
        else:
            #Extended Scanning (If Contents during extract are inside another folder (Yuri-1.0/script-ch1.rpyc))
            # if folder inside is /game to move to mod folder
            if glob.glob(str(mzte[1]) + '/characters'):
                ext_move(str(mzte[1]), '/characters')
            if glob.glob(str(mzte[1]) + '/lib'):
                lib_move(project_dir, str(mzte[1]))
            if glob.glob(str(mzte[1]) + '/renpy'):
                rpy_move(project_dir, str(mzte[1]))
                rpy_ext(project_dir, str(mzte[1]))
            if glob.glob(str(mzte[1]) + '/game'):
                ext_move(str(mzte[1]),'/game')
            else:
                if renpy.macintosh:
                    # move mod files to the /game folder or mod folder
                    if os.path.exists(project_dir + '/DDLC.app/Contents/Resources/autorun/game/python-packages'):
                        if os.path.exists(str(mzte[1]) + '/python-packages'):
                            shutil.rmtree(project_dir + '/DDLC.app/Contents/Resources/autorun/game/python-packages')
                        else:
                            pass
                    import os
                    for file in os.listdir(str(mzte[1])):
                        print file
                        src_file = os.path.join(str(mzte[1]), file)
                        dst_file = os.path.join(project_dir + '/DDLC.app/Contents/Resources/autorun/game', file)
                        shutil.move(src_file, dst_file)
                else:
                    # move mod files to the /game folder or mod folder
                    if os.path.exists(project_dir + '/game/python-packages'):
                        if os.path.exists(str(mzte[1]) + '/python-packages'):
                            shutil.rmtree(project_dir + '/game/python-packages')
                        else:
                            pass
                    import os
                    for file in os.listdir(str(mzte[1])):
                        print file
                        src_file = os.path.join(str(mzte[1]), file)
                        dst_file = os.path.join(project_dir + '/game', file)
                        shutil.move(src_file, dst_file)

        # Prevents copy of any other RPA or other mod files
        shutil.rmtree(persistent.projects_directory + '/temp')

        interface.info("Mod Add-on for " + project.current.name + " has been installed.")

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
    if renpy.macintosh and persistent.safari is None:
        call browser
    # Ren'Py Failsafe
    if renpy.macintosh and persistent.safari is None:
        $ interface.error(_("The browser could not be set. Giving up."))
    # Checks if user set DDLC ZIP Location (All OS)
    if persistent.zip_directory is None:
        if renpy.macintosh:
            call choose_zip_directory
        else:
            call ddlc_location
    # Ren'Py Failsafe 2
    if persistent.zip_directory is None:
        $ interface.error(_("The DDLC ZIP directory could not be set. Giving up."))

    python hide:
        import shutil
        # Asks User the name of the folder they want their mod folder to be
        modinstall_foldername = interface.input(
            _("DDLC Folder Name"),
            _("Please enter the name of your DDLC folder:"),
            filename=True,
            cancel=Jump("front_page"))

        modinstall_foldername = modinstall_foldername.strip()
        if not modinstall_foldername:
            interface.error(_("The folder name may not be empty."))

        project_dir = os.path.join(persistent.projects_directory, modinstall_foldername)

        if project.manager.get(modinstall_foldername) is not None:
            interface.error(_("[modinstall_foldername!q] already exists. Please choose a different folder name."), modinstall_foldername=modinstall_foldername)

        if os.path.exists(project_dir):
            interface.error(_("[project_dir!q] already exists. Please choose a different name."), project_dir=project_dir)

        interface.interaction(_("Making a DDLC Folder"), _("Extracting DDLC, Please Wait..."),)
        if renpy.macintosh:
            if persistent.safari == False:
                #Chrome/Firefox (Safari Safe Mode Off)
                interface.interaction(_("Making a DDLC Folder"), _("Extracting DDLC, Please Wait..."),)
                zip_extract(project_dir)
            else:
                interface.interaction(_("Making a DDLC Folder"), _("Copying DDLC, Please Wait..."),)
                ddlc_copy(project_dir)
            project.manager.scan()
        else:
            # Asks if the copy is Steam
            if persistent.steam_release == True:
                steam_copy(project_dir)
            else:
                zip_extract(project_dir)

        project.manager.scan()
    
    jump front_page