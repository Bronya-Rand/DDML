# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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

default persistent.steam_release = None 
init python:
    import shutil
    import os
    import time
    import re

    def check_language_support():

        language = _preferences.language


        new = False
        legacy = False


        # Check for a translation of the words "New GUI Interface".
        if (language is None) or (__("Steam Release") != "Steam Release"):
            new = True

        try:
            if (language is None) or os.path.exists(os.path.join(config.renpy_base, "templates", language)):
                legacy = True
        except:
            pass

        if new and legacy:
            store.language_support = _("Both interfaces have been translated to your language.")
        elif new:
            store.language_support = _("Only the new GUI has been translated to your language.")
        elif legacy:
            store.language_support = _("Only the legacy theme interface has been translated to your language.")
        else:
            store.language_support = _("Neither interface has been translated to your language.")


label ddlc_location:

    if persistent.projects_directory is None:
        call choose_projects_directory

    if persistent.projects_directory is None:
        $ interface.error(_("The projects directory could not be set. Giving up."))

    python:

        check_language_support()

        release_kind = interface.choice(
            _("Which DDLC release do you have. If you downloaded DDLC from Steam, select Steam Release. If you downloaded DDLC from ddlc.moe, select DDLC ZIP/DDLC.moe Release."),
            [ ( 'ddlc_steam_release', _("Steam Release") ), ( 'ddlc_moe_release', _("DDLC ZIP/DDLC.moe Release")) ],
            "ddlc_steam_release",
            cancel=Jump("front_page"),
            )

        renpy.jump(release_kind)

label ddlc_moe_release:

    python hide:

        interface.interaction(_("DDLC ZIP/DDLC.moe Directory"), _("Please choose the location of your DDLC ZIP."), _("This will make DDML find DDLC and copy it to your Mod Folder for Mods."),)

        moepath, is_default = choose_directory(persistent.zip_directory)

        if is_default:
            interface.info(_("DDML has set the DDLC ZIP directory to:"), "[moepath!q]", moepath=moepath)

        persistent.zip_directory = moepath

    $ persistent.steam_release = False

    jump front_page

label ddlc_steam_release:

    python hide:
        interface.interaction(_("Steam Directory"), _("Please choose the location of your Steam's common folder."), _("This will make DDML find DDLC and copy it to your Mod Folder for Mods."),)

        steampath, is_default = choose_directory(persistent.zip_directory)

        if is_default:
            interface.info(_("DDML has set the Steam directory to:"), "[steampath!q]", steampath=steampath)

        persistent.zip_directory = steampath

    $ persistent.steam_release = True

    return