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

define PROJECT_ADJUSTMENT = ui.adjustment()

init python:

    import os
    import subprocess
    from modmanagement import ModManagement
    from ddmm_compatibility import DDMM_Compatibility

    modman = ModManagement()
    mm_compat = DDMM_Compatibility()

    class OpenDirectory(Action):
        """
        Opens `directory` in a file browser. `directory` is relative to
        the project root.
        """

        alt = _("Open [text] directory.")

        def __init__(self, directory, absolute=False):
            if absolute:
                self.directory = directory
            else:
                self.directory = os.path.join(project.current.path, directory)

        def get_sensitive(self):
            return os.path.exists(self.directory)

        def __call__(self):

            try:
                directory = renpy.fsencode(self.directory)

                if renpy.windows:
                    os.startfile(directory)
                elif renpy.macintosh:
                    subprocess.Popen([ "open", directory ])
                else:
                    subprocess.Popen([ "xdg-open", directory ])

            except:
                pass

    # Used for testing.
    def Relaunch():
        renpy.quit(relaunch=True)

screen front_page:
    frame:
        alt ""

        style_group "l"
        style "l_root"

        has hbox

        # Projects list section - on left.

        frame:
            style "l_projects"
            xmaximum 300
            right_margin 2

            top_padding 20
            bottom_padding 26

            side "t c b":

                window style "l_label":

                    has hbox:
                        xfill True

                    text _("Mods:") style "l_label_text" size 36 yoffset 10

                    textbutton _("refresh"):
                        xalign 1.0
                        yalign 1.0
                        yoffset 5
                        style "l_small_button"
                        action project.Rescan()
                        right_margin HALF_INDENT

                side "c r":

                    viewport:
                        yadjustment PROJECT_ADJUSTMENT
                        mousewheel True
                        use front_page_project_list

                    vbar:
                        style "l_vscrollbar"
                        adjustment PROJECT_ADJUSTMENT

                vbox:
                    add HALF_SPACER
                    add SEPARATOR
                    add HALF_SPACER
                
                    vbox:
                        xfill True

                        textbutton _("+ Change Mod Folder"):
                            left_margin (HALF_INDENT) 
                            action Jump("move_mod_folder")

                        add HALF_SPACER
                        textbutton _("+ Add a Mod"):
                            left_margin (HALF_INDENT) 
                            action Jump("add_a_mod")

                        add HALF_SPACER
                        textbutton _("+ Add DDLC"):
                            left_margin (HALF_INDENT) 
                            action Jump("add_base_game")
                    
                        add HALF_SPACER
                        textbutton _("+ Search for Mods"):
                            left_margin (HALF_INDENT) 
                            action Jump("update")

        # Project section - on right.

        if project.current is not None:
            use front_page_project

    if project.current is not None:
        textbutton _("Launch Mod") action project.Launch() style "l_right_button"
        key "K_F5" action project.Launch()



# This is used by front_page to display the list of known projects on the screen.
screen front_page_project_list:

    $ projects = project.manager.projects
    $ templates = project.manager.templates

    vbox:

        if templates and persistent.show_templates:

            for p in templates:

                textbutton _("[p.name!q] (template)"):
                    action project.Select(p)
                    alt _("Select project [text].")
                    style "l_list"

            null height 12

        if projects:

            for p in projects:

                textbutton "[p.name!q]":
                    action project.Select(p)
                    alt _("Select project [text].")
                    style "l_list"

            null height 12


# This is used for the right side of the screen, which is where the project-specific
# buttons are.
screen front_page_project:

    $ p = project.current

    window:

        has vbox

        frame style "l_label":
            has hbox xfill True
            text "[p.display_name!q]" style "l_label_text"
            label _("Active Mod") style "l_alternate"

        grid 1 1:
            xfill True
            spacing HALF_INDENT

            vbox:

                label _("Mod Options") style "l_label_small"

                frame style "l_indent":
                    has vbox

                    textbutton _("Delete 'scripts.rpa'") action Jump("scripts_rpa")
                    textbutton _("Delete 'images.rpa'") action Jump("images_rpa")
                    textbutton _("Delete Saves") action Jump("rmpersistent")

        add SPACER

        label _("DDML Options") style "l_label_small"

        grid 1 1:
            xfill True
            spacing HALF_INDENT

            frame style "l_indent":
                has vbox

                if persistent.projects_directory:
                    textbutton _("Browse Mod Directory") action OpenDirectory(persistent.projects_directory)
                    textbutton _("Browse Game Directory") action OpenDirectory("game")
                    if renpy.windows:
                        textbutton _("Browse Save Directory") action OpenDirectory(os.getenv('APPDATA') + '/RenPy')
                    elif renpy.macintosh:
                        textbutton _("Browse Save Directory") action OpenDirectory(os.environ['HOME'] +"/Library/RenPy")
                    else:
                        textbutton _("Browse Save Directory") action OpenDirectory(os.environ['HOME'] + "/.renpy")
                textbutton _("Delete Mod") action Jump("delete_mod_folder")

                # textbutton "Relaunch" action Relaunch

label main_menu:
    return

label start:
    show screen bottom_info
    $ dmgcheck()

label front_page:
    call screen front_page
    jump front_page

label scripts_rpa:

    python:
        interface.processing(_("Deleting scripts.rpa..."))
        modman.delete_rpa(os.path.join(persistent.projects_directory, "/game"), "scripts.rpa")

    jump front_page

label images_rpa:

    python:
        interface.processing(_("Deleting scripts.rpa..."))
        modman.delete_rpa(os.path.join(persistent.projects_directory, "/game"), "images.rpa")

    jump front_page

label lint:
    python hide:

        interface.processing(_("Checking script for potential problems..."))
        lint_fn = project.current.temp_filename("lint.txt")

        project.current.launch([ 'lint', lint_fn ], wait=True)

        e = renpy.editor.editor
        e.begin(True)
        e.open(lint_fn)
        e.end()

    jump front_page

label rmpersistent:

    python hide:
        interface.processing(_("Deleting save data..."))
        project.current.launch([ 'rmpersistent' ], wait=True)

    jump front_page

label force_recompile:

    python hide:
        interface.processing(_("Recompiling all rpy files into rpyc files..."))
        project.current.launch([ 'compile' ], wait=True)

    jump front_page

# Code to delete a mod from the mod folder
label delete_mod_folder:

    python hide:
        while True:
            mod_delete_response = interface.input(
                _("Deleting a Mod"),
                _("Are you sure you want to delete [project.current.name]? Type either Yes or No."),
                filename=False,
                cancel=Jump("front_page"))
            mod_delete_response = mod_delete_response.strip()

            if not mod_delete_response or mod_delete_response.lower() == "no":
                interface.error(_("The operation has been cancelled."))
                return

            elif mod_delete_response.lower() == "yes":

                with interface.error_handling(_("deleting mod.")):
                    modman.delete_mod(persistent.projects_directory, project.current.name)

                interface.info("[project.current.name] has been deleted from the mod folder.")
            else:
                interface.error(_("Invalid Input. Expected either a Yes or No response."))
                continue

            project.manager.scan()
            break

    jump front_page

# Code to move mod folder
label move_mod_folder:

    python hide:

        interface.interaction(_("New Mod Directory"), _("Please choose the new mod folder using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"), _("DDML will create new mods in this folder, and place your existing mods in here."),)

        path, is_default = choose_directory(None)

        if is_default:
            interface.error(_("The operation has been cancelled."))
            renpy.jump("front_page")

        # Moves Mods from old folder to new folder
        mm_compat.ddmm_traceback_start()
        interface.processing(_("Moving your existing mods to the new mod folder. Please wait..."))
        try:
            modman.move_mod_folder(persistent.projects_directory, path)
            persistent.projects_directory = path
            interface.info(_("DDML transferred all your mods to the new mod folder with no errors."),)
        except:
            mm_compat.ddmm_traceback("new mod folder")
            modman.move_mod_folder(path, persistent.projects_directory)
            interface.error(_("DDML was unable to move your mods to the new mod folder due to a error."),
            _("See {i}transfer_log.txt{/i} for more information. If the issue persists, contact the developer on Github."))

        project.manager.scan()
        mm_compat.ddmm_traceback_shutdown()

    return