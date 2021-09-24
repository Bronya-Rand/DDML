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
    from extractor import Extractor

    extract = Extractor()

label add_a_mod:
    if persistent.projects_directory is None:
        call choose_projects_directory
    if persistent.projects_directory is None:
        $ interface.error(_("The mod folder path could not be set. Please try again."))
    if renpy.macintosh:
        if persistent.safari is None:
            call browser
        if persistent.safari is None:
            $ interface.error(_("Couldn't check if the OS auto-extracts ZIPs. Please try again."))
    if persistent.zip_directory is None:
        call ddlc_location
    if persistent.zip_directory is None:
        $ interface.error(_("The DDLC path could not be set. Giving up."))
    if persistent.zip_directory is None:
        call ddlc_location
    if persistent.zip_directory is None:
        $ interface.error(_("The DDLC path could not be set. Giving up."))

    python:
        modinstall_foldername = ""
        while True:
            modinstall_foldername = interface.input(
                _("Mod Name"),
                _("Please type in the name of the mod that you are installing."),
                allow=interface.PROJECT_LETTERS,
                cancel=Jump("front_page"),
                default=modinstall_foldername,
            )
            modinstall_foldername = modinstall_foldername.strip()

            if not modinstall_foldername:
                interface.error(_("The mod name may not be empty."), label=None)
                continue
            if modinstall_foldername == "launcher":
                interface.error(_("'launcher' is a reserved folder name. Please choose a different mod name."), label=None)
                continue

            project_dir = os.path.join(persistent.projects_directory, modinstall_foldername)

            if project.manager.get(modinstall_foldername) is not None:
                interface.error(_("[modinstall_foldername!q] already exists. Please choose a different mod name."), modinstall_foldername=modinstall_foldername, label=None)
                continue
            if os.path.exists(project_dir):
                interface.error(_("[project_dir!q] already exists. Please choose a different mod name."), project_dir=project_dir, label=None)
                continue

            if renpy.macintosh and persistent.safari == True:
                interface.interaction(_("Making the Mod Folder"), _("Copying DDLC, Please Wait..."),)
                extract.game_installation(persistent.zip_directory, project_dir, True)
            else:
                interface.interaction(_("Making the Mod Folder"), _("Extracting DDLC, Please Wait..."),)
                if not renpy.macintosh:
                    if persistent.steam_release == True:
                        extract.game_installation(persistent.zip_directory, project_dir, True)
                    else:
                        extract.game_installation(persistent.zip_directory, project_dir)
                else:
                    if persistent.safari == True:
                        extract.game_installation(persistent.zip_directory, project_dir, True)
                    else:
                        extract.game_installation(persistent.zip_directory, project_dir)

            if renpy.macintosh and persistent.safari == True:
                interface.interaction(_("Mod Files"), _("Please select the the mod folder you wish to install."),)
                
                path, is_default = choose_directory(None)
            else:
                interface.interaction(_("Mod Files"), _("Please select the mod ZIP file you wish to install."),)

                path, is_default = choose_file(None)

            if path is None:
                shutil.rmtree(project_dir)
                interface.error(_("The operation has been cancelled."))
                renpy.jump("front_page")

            if path.endswith('.zip'):
                valid = extract.valid_zip(path)
                if valid:
                    pass
                else:
                    shutil.rmtree(project_dir)
                    inteface.error(_("The mod ZIP you selected is not a valid DDLC mod archive.\nSelect a different mod ZIP and try again."),)
                    renpy.jump("front_page")
            elif path.endswith('.rar'):
                shutil.rmtree(project_dir)
                inteface.error(_("RAR files cannot be unzipped or unrarred by DDML.\nConvert the file to a ZIP file and try again."),)
                renpy.jump("front_page")
            else:
                shutil.rmtree(project_dir)
                inteface.error(_("Unknown file type.\nSelect a DDMC mod ZIP file and try again."),)
                renpy.jump("front_page")

            interface.interaction(_("Installing the Mod"), _("This process may take some time. Please wait."),)

            if not renpy.macintosh:
                if persistent.steam_release == True:
                    extract.installation(path, project_dir, True)
                else:
                    extract.installation(path, project_dir)
            else:
                if persistent.safari == True:
                    extract.installation(path, project_dir, True)
                else:
                    extract.installation(path, project_dir)

            interface.info(_("DDML has installed [modinstall_foldername!q] to the mod folder."), modinstall_foldername=modinstall_foldername)
            project.manager.scan()
            break
        
    jump front_page

label add_base_game:
    if persistent.projects_directory is None:
        call choose_projects_directory
    if persistent.projects_directory is None:
        $ interface.error(_("The mod folder path could not be set. Please try again."))
    if renpy.macintosh:
        if persistent.safari is None:
            call browser
        if persistent.safari is None:
            $ interface.error(_("Couldn't check if the OS auto-extracts ZIPs. Please try again."))
    if persistent.zip_directory is None:
        call ddlc_location
    if persistent.zip_directory is None:
        $ interface.error(_("The DDLC path could not be set. Giving up."))
    if persistent.zip_directory is None:
        call ddlc_location
    if persistent.zip_directory is None:
        $ interface.error(_("The DDLC path could not be set. Giving up."))

    python:
        modinstall_foldername = ""
        while True:
            modinstall_foldername = interface.input(
                _("DDLC Name"),
                _("Please type in the name of the folder you want to install DDLC onto."),
                allow=interface.PROJECT_LETTERS,
                cancel=Jump("front_page"),
                default=modinstall_foldername,
            )
            modinstall_foldername = modinstall_foldername.strip()

            if not modinstall_foldername:
                interface.error(_("The DDLC folder name may not be empty."), label=None)
                continue
            if modinstall_foldername == "launcher":
                interface.error(_("'launcher' is a reserved folder name. Please choose a different folder name."), label=None)
                continue

            project_dir = os.path.join(persistent.projects_directory, modinstall_foldername)

            if project.manager.get(modinstall_foldername) is not None:
                interface.error(_("[modinstall_foldername!q] already exists. Please choose a different folder name."), modinstall_foldername=modinstall_foldername, label=None)
                continue
            if os.path.exists(project_dir):
                interface.error(_("[project_dir!q] already exists. Please choose a different folder name."), project_dir=project_dir, label=None)
                continue

            if renpy.macintosh and persistent.safari == True:
                interface.interaction(_("Making the DDLC Folder"), _("Copying DDLC, Please Wait..."),)
                extract.game_installation(persistent.zip_directory, project_dir, True)
            else:
                interface.interaction(_("Making the DDLC Folder"), _("Extracting DDLC, Please Wait..."),)
                if not renpy.macintosh:
                    if persistent.steam_release == True:
                        extract.game_installation(persistent.zip_directory, project_dir, True)
                    else:
                        extract.game_installation(persistent.zip_directory, project_dir)
                else:
                    if persistent.safari == True:
                        extract.game_installation(persistent.zip_directory, project_dir, True)
                    else:
                        extract.game_installation(persistent.zip_directory, project_dir)
            
            interface.info(_("DDML has installed DDLC to the mod folder."), modinstall_foldername=modinstall_foldername)
            project.manager.scan()
            break

    jump front_page
