# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
# Copyright 2018-2019 GanstaKingofSA <azarieldc@gmail.com>
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

# Asks whether they downloaded DDLC from Steam or DDLC.moe/Itch.io
label ddlc_location:

    python:

        release_kind = interface.choice(
            _("Where did you download DDLC? If you downloaded DDLC from Steam, select Steam. If you downloaded DDLC from ddlc.moe or itch.io, select DDLC.moe."),
            [ ( 'ddlc_steam_release', _("Steam") ), ( 'ddlc_moe_release', _("DDLC.moe")) ],
            "ddlc_steam_release",
            cancel=Jump("front_page"),
            )

        renpy.jump(release_kind)
# Asks User where ddlc-win.zip is
label ddlc_moe_release:

    python hide:

        interface.interaction(_("DDLC ZIP/DDLC.moe Directory"), _("Please choose the folder where you have 'ddlc-win.zip'."), _("This will make DDML find DDLC and copy it to your Mod Folder for Mods."),)

        moepath, is_default = choose_directory(persistent.zip_directory)

        if is_default:
            interface.info(_("DDML has set the DDLC ZIP directory to:"), "[moepath!q]", moepath=moepath)

        persistent.zip_directory = moepath
    # Returns False that this directory is Steam
    $ persistent.steam_release = False

    return
# Asks User where Steam/SteamApps/Common is
label ddlc_steam_release:

    python hide:
        interface.interaction(_("Steam Directory"), _("Please choose the 'common' folder inside of the Steam folder."), _("This will make DDML find DDLC and copy it to your Mod Folder for Mods."),)

        steampath, is_default = choose_directory(persistent.zip_directory)

        if is_default:
            interface.info(_("DDML has set the Steam directory to:"), "[steampath!q]", steampath=steampath)

        persistent.zip_directory = steampath
    # Returns True that this directory is Steam
    $ persistent.steam_release = True

    return