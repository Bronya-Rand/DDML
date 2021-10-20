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
    import urllib2
    import ssl
    import json

    # This can be one of None, "available", "not-available", or "error".
    #
    # It must be None for a release.
    UPDATE_SIMULATE = os.environ.get("RENPY_UPDATE_SIMULATE", None)

    PUBLIC_KEY = "renpy_public.pem"

    CHANNELS_URL = "https://www.renpy.org/channels.json"

    version_tuple = renpy.version(tuple=True)

    def check_dlc(name):
        """
        Returns true if the named dlc package is present.
        """

        return name in updater.get_installed_packages()

    def add_dlc(name, restart=False):
        """
        Adds the DLC package, if it doesn't already exist.

        Returns True if the DLC is installed, False otherwise.
        """

        dlc_url = "http://update.renpy.org/{}/updates.json".format(".".join(str(i) for i in version_tuple[:-1]))

        state = updater.get_installed_state()

        if state is not None:
            base_name = state.get("sdk", {}).get('base_name', '')

            if base_name.startswith("renpy-nightly-"):
                dlc_url = "http://nightly.renpy.org/{}/updates.json".format(base_name[6:])

        return renpy.invoke_in_new_context(updater.update, dlc_url, add=[name], public_key=PUBLIC_KEY, simulate=UPDATE_SIMULATE, restart=restart)

    filter_keywords = []

    def decode_list():
        with interface.error_handling(_("Decoding the mod list...")):
            ddmc_data = config.basedir + '/ddmc.json'
            with open(ddmc_data, 'r') as f:
                return json.load(f)

    def nsfw_tag(modList):
        for c in modList:
            if c['modNSFW'] and not persistent.nsfw:
                modList.remove(c)
            elif c['modNSFW'] and persistent.nsfw:
                c["modName"] = "{b}(NSFW){/b} " + c["modName"]

screen update_channel(channels, criteria=None):

    frame:
        style_group "l"
        style "l_root"

        window:

            has viewport:
                scrollbars "vertical"
                mousewheel True

            has vbox

            frame style "l_alternate":
                has hbox xfill True
                text _("Mod List") style "l_label_text"

            frame style "l_label":
                has hbox xfill True
            
                text _("Select the mod you will like to download, then return to the home menu and install it with DDML."):
                    style "l_small_text"
                    size 15
                    xpos INDENT 

                add HALF_SPACER
                
                frame:
                    style "l_alternate"
                    style_group "l_small"

                    has hbox

                    textbutton _("Search") action Jump("search")

            hbox:
                frame:
                    style "l_indent"
                    xfill True

                    has vbox

                    if criteria is not None:
                        
                        python:
                            filter_keywords.clear()

                            if criteria != " " and not "," in criteria:
                                filter_keywords.append(criteria)
                            else:
                                cs = criteria.split(",")
                                for k in cs:
                                    filter_keywords.append(k.replace(" ", ""))

                        python:
                            chosen_channels = []
                            
                            for c in channels:
                                category_kwds = c["modSearch"]
                                name_kwds = c["modName"]
                                
                                for e in filter_keywords:
                                    e = e.lower()

                                    if e in category_kwds or e in name_kwds.lower():
                                        
                                        if c not in chosen_channels:

                                            chosen_channels.append(c)
                            
                            channels = chosen_channels
                        
                        text "Found {} mods that are tagged with the following search phrases: ".format(
                            len(chosen_channels)) + ", ".join(filter_keywords) + "." style "l_small_text"

                        add SPACER

                    for c in channels:
                        
                        if c['modShow']:

                            textbutton c["modName"].replace("[", "[[").replace("]", "]]"): 
                                text_style "mod_search_name"
                                action OpenURL(c["modUploadURL"])

                            add HALF_SPACER

                            text c["modShortDescription"] style "mod_search_small_text"

                            python:
                                playTime = "Playtime: {i}"

                                if c["modPlayTimeHours"]:

                                    playTime += str(c["modPlayTimeHours"]) + " hour"

                                    if c["modPlayTimeHours"] > 1:
                                        playTime += "s"

                                    playTime += " "

                                if c["modPlayTimeMinutes"]:

                                    playTime += str(c["modPlayTimeMinutes"]) + " minute"

                                    if c["modPlayTimeMinutes"] > 1:
                                        playTime += "s"
                                
                                if not c["modPlayTimeHours"] and c["modPlayTimeMinutes"] == 0:

                                    playTime += "Unknown"

                            add SPACER
                            
                            text playTime + "{/i}" style "mod_search_playtime"

                            add SPACER
                            add SEPARATOR2 at mod_search_seperator
                            add SPACER

    textbutton _("Return") action Jump("front_page") style "l_left_button"

label update:

    python hide:
        interface.processing(_("Fetching the mod list..."))

        # Disabled due to obsoleteness but it may be useful in code someday
        # Thanks Vige!
        
        # with interface.error_handling(_("Downloading a updated mod list...")):
        #     url = "https://www.dokidokimodclub.com/api/mod/"
        #     headers = {'Authorization': 'Api-Key [REDACTED]'}
        #     context = ssl._create_unverified_context()
        #     req = urllib2.Request(url=url, headers=headers)
        #     response = urllib2.urlopen(req, context=context)
        #     the_page = response.read()

        channels = decode_list()
        nsfw_tag(channels)
            
        renpy.call_screen("update_channel", channels, None)

    jump front_page

label search:

    python hide:

        while True:

            criteria = ""
            criteria = interface.input(
                _("Search a Mod"),
                _("Type in the mod name or search phrases (separated by commas) of the mod that you are looking for."),
                allow=interface.PROJECT_LETTERS + ",",
                cancel=Jump("front_page"),
                default="",
            )
            
            if criteria == "":
                interface.error(_("Your search cannot be left empty. Please try again."), label=None)
                continue

            channels = decode_list()
            nsfw_tag(channels)

            renpy.call_screen("update_channel", channels, criteria)
            break

    jump front_page

style mod_search_small_text is l_small_text:
    size 18

style mod_search_name is l_left_button_text:
    size 20
    underline True

style mod_search_playtime is l_small_text:
    size 16

transform mod_search_seperator:
    ysize 5