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
    persistent.b_ddml = None
    
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
            rv.append((i.title(), i))

        for i in (("Schinese", "schinese"), ("Tchinese", "tchinese")):
            if i in rv:
                rv.remove(i)
                rv.append(({"schinese": "Simplified Chinese", "tchinese": "Traditional Chinese"}.get(i[1]), i[1]))

        rv.sort()

        if ("Piglatin", "piglatin") in rv:
            rv.remove(("Piglatin", "piglatin"))
            rv.append(("Pig Latin", "piglatin"))

        return rv

    show_legacy = os.path.exists(os.path.join(config.renpy_base, "templates", "english", "game", "script.rpy"))

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

                        text _("Mod Folder Path")

                        add HALF_SPACER


                        frame style "l_indent":
                            if persistent.projects_directory:
                                textbutton _("[persistent.projects_directory!q]"):
                                    action Jump("projects_directory_preference")
                                    alt _("Mod Folder Path [text]")
                            else:
                                textbutton _("Not Set"):
                                    action Jump("projects_directory_preference")
                                    alt _("Mod Folder Path [text]")

                    add SPACER

                    # Text editor selection.
                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        yminimum 75
                        has vbox
                        text _("DDLC Copy Directory")

                        add HALF_SPACER

                        frame style "l_indent":
                            if persistent.zip_directory:
                                textbutton _("[persistent.zip_directory!q]"):
                                    action Jump("projects_zip_preference")
                                    alt _("DDLC ZIP Path [text]")
                            else:
                                textbutton _("Not Set"):
                                    action Jump("projects_zip_preference")
                                    alt _("DDLC ZIP Path [text]")

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
                            text _("ZIP Auto-Extracts?")

                            add HALF_SPACER

                            frame style "l_indent":
                                if persistent.safari != None:
                                    if persistent.safari == True:
                                        text _("Yes")
                                    else:
                                        text _("No")
                                else:
                                    text _("Unknown")
                            
                            add HALF_SPACER

                            textbutton _("Change Auto-Extract Setting") action Jump("browser")
                        else:
                            text _("DDLC Version")

                            add HALF_SPACER

                            frame style "l_indent":
                                if persistent.steam_release == True:
                                    text _("Steam Version")
                                else:
                                    if persistent.steam_release == None:
                                        text _("Unknown")
                                    else:
                                        text _("DDLC.moe Version")

                    add SPACER

                    frame:
                        style "l_indent"
                        yminimum 75
                        has vbox

                        add SPACER

                        textbutton _("Dev Options") style "l_checkbox" action ToggleField(persistent, "b_ddml")
                        if persistent.b_ddml:

                            add HALF_SPACER

                            textbutton _("Build") action [project.Select("launcher"), Jump("build_distributions")]

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

                        text _("Launcher Options:")

                        add HALF_SPACER

                        textbutton _("Reset Window Size") style "l_nonbox" action Preference("display", 1.0)
                        textbutton _("Transfer DDMM Data") style "l_nonbox" action Jump("transfer")
                        
                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        yminimum 75
                        has vbox

                        text _("Theme:")

                        add HALF_SPACER

                        textbutton _("One UI") style "l_checkbox" action [ToggleField(persistent, "oneui"), Jump("restart_ddmm")]

    textbutton _("Return") action Jump("front_page") style "l_left_button"

label projects_directory_preference:
    python:
        release_kind = interface.choice(
            _("Are you wanting to move your mods to a new folder path or set a new path?"),
            [ ( 'move_mod_folder', _("Move Mods to a New Folder Path") ), ( 'choose_projects_directory', _("Setup a New Mod Path")) ],
            "choose_projects_directory",
            cancel=Jump("preferences"),
            )

        renpy.jump(release_kind)

    jump preferences

label projects_zip_preference:
    call ddlc_location
    jump preferences

label preferences:
    call screen preferences
    jump preferences

label restart_ddmm:
    python:
        renpy.quit(relaunch=True)
    return 
