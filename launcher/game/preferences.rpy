# Copyright 2004-2020 Tom Rothamel <pytom@bishoujo.us>
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
    if persistent.show_edit_funcs is None:
        persistent.show_edit_funcs = True

    if persistent.windows_console is None:
        persistent.windows_console = False

    def scan_translations():

        languages = renpy.known_languages()

        if not languages:
            return None

        rv = [ ( "English", None) ]

        for i in languages:
            rv.append((i.replace("_", " ").title(), i))

        rv.sort()

        if ("Piglatin", "piglatin") in rv:
            rv.remove(("Piglatin", "piglatin"))
            rv.append(("Pig Latin", "piglatin"))

        return rv

    show_legacy = os.path.exists(os.path.join(config.renpy_base, "templates", "english", "game", "script.rpy"))

    class ImgDir(Action):
        """
        Opens `images` in a file browser.
        """

        alt = _("Open [text] directory.")

        def __init__(self, directory, absolute=False):
            if absolute:
                self.directory = directory
            else:
                self.directory = os.path.join(os.getcwd(), directory)

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

default persistent.legacy = False
default persistent.force_new_tutorial = False
default persistent.sponsor_message = True

screen preferences:

    $ translations = scan_translations()

    frame:
        style_group "l"
        style "l_root"
        alt "Preferences"

        window:

            has vbox

            label _("Settings")

            add HALF_SPACER

            hbox:

                frame:
                    style "l_indent"
                    xmaximum ONETHIRD
                    xfill True

                    has vbox

                    # Projects directory selection.
                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        yminimum 75
                        has vbox

                        text _("Mod Folder Directory:")

                        add HALF_SPACER


                        frame style "l_indent":
                            if persistent.projects_directory:
                                textbutton _("[persistent.projects_directory!q]"):
                                    action Jump("projects_directory_preference")
                                    alt _("Projects directory: [text]")
                            else:
                                textbutton _("Not Set"):
                                    action Jump("projects_directory_preference")
                                    alt _("Projects directory: [text]")

                        add SPACER

                        # Text editor selection.
                        add SEPARATOR2

                        frame:
                            style "l_indent"
                            yminimum 75
                            has vbox
                            text _("DDLC Copy Directory:")

                            add HALF_SPACER

                            frame style "l_indent":
                                if persistent.zip_directory:
                                    textbutton _("[persistent.zip_directory!q]"):
                                        action Jump("projects_zip_preference")
                                        alt _("DDLC ZIP directory: [text]")
                                else:
                                    textbutton _("Not Set"):
                                        action Jump("projects_zip_preference")
                                        alt _("DDLC ZIP directory: [text]")
                                        
                        add SPACER

                        # Text editor selection.
                        add SEPARATOR2
                        
                        frame:
                            style "l_indent"
                            yminimum 75
                            has vbox
                            text _("Mod Download Folder:")

                            add HALF_SPACER

                            frame style "l_indent":
                                if persistent.mzip_directory:
                                    textbutton _("[persistent.mzip_directory!q]"):
                                        action Jump("projects_mzip_preference")
                                        alt _("Mod Download Directory: [text]")
                                else:
                                    textbutton _("Not Set"):
                                        action Jump("projects_mzip_preference")
                                        alt _("Mod Download Directory: [text]")

                frame:
                    style "l_indent"
                    xmaximum ONETHIRD
                    xfill True

                    has vbox
                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        yminimum 75
                        has vbox
                        if renpy.macintosh:
                            text _("OS auto-extracts '.zip' files?")
                            add HALF_SPACER

                            frame style "l_indent":
                                if persistent.safari != None:
                                    if persistent.safari == True:
                                        text _("Yes")
                                    else:
                                        text _("No")
                                else:
                                    text _("None Selected")
                        else:
                            text _("DDLC Copy:")
                            add HALF_SPACER

                            frame style "l_indent":
                                if persistent.steam_release == True:
                                    text _("Steam Copy")
                                else:
                                    if persistent.steam_release == None:
                                        text _("No DDLC Copy Selected")
                                    else:
                                        text _("DDLC.moe ZIP Copy")
                    add SPACER
                    if renpy.macintosh:     
                        textbutton _("Change Browser") action Jump("browser")
                        add SPACER
                    #add SEPARATOR2
                    if renpy.windows:
                        frame:
                            style "l_indent"
                            yminimum 75
                            has vbox

                            text _("Customization:")
                            add HALF_SPACER
                            frame style "l_indent":
                                textbutton _("Change Layout") action ImgDir("launcher/game/images")
                    add SPACER
                    frame:
                        style "l_indent"
                        yminimum 75
                        has vbox

                        add SPACER
                        textbutton _("Build Mode") style "l_checkbox" action ToggleField(persistent, "b_ddml")
                        if persistent.b_ddml:
                            textbutton _("Build Distributions") action [project.Select("launcher"), Jump("build_distributions")]

    textbutton _("Return") action Jump("front_page") style "l_left_button"

label projects_directory_preference:
    python:
        release_kind = interface.choice(
            _("Are you wanting to move your existing mod folder to a new folder or set a new one?"),
            [ ( 'move_mod_folder', _("Move Existing Mod Folder to a New Folder") ), ( 'choose_projects_directory', _("Setup a New One")) ],
            "choose_projects_directory",
            cancel=Jump("preferences"),
            )

        renpy.jump(release_kind)

    jump preferences

label projects_mzip_preference:
    call choose_modzip_directory
    jump preferences
    
# Setting Configuration Calls
label projects_zip_preference:
    call ddlc_location
    jump preferences

label preferences:
    call screen preferences
    jump preferences
