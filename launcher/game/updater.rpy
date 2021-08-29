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

    def decode_list():
        with interface.error_handling(_("Decoding the mod list...")):
            ddmc_data = config.basedir + '/ddmc.json'
            with open(ddmc_data, 'r') as f:
                return json.load(f)

screen update_channel(channels):

    frame:
        style_group "l"
        style "l_root"

        window:

            has viewport:
                scrollbars "vertical"
                mousewheel True

            has vbox

            label _("DD Mod Club Mod List")

            add HALF_SPACER

            hbox:
                frame:
                    style "l_indent"
                    xfill True

                    has vbox

                    text _("Select the mod you will like to download, download it, then return to the home menu and install it with DDML.")

                    for c in channels:
                        
                        if c['modShow']:
                            add SPACER

                            textbutton c["modName"].replace("[", "").replace("]", "") action OpenURL(c["modUploadURL"])

                            add HALF_SPACER

                            text c["modShortDescription"] style "l_small_text"

    textbutton _("Return") action Jump("front_page") style "l_left_button"

label update:

    python hide:
        interface.processing(_("Fetching the mod list..."))

        # Disabled due to obsoleteness but it may be useful in code someday
        
        # with interface.error_handling(_("Downloading a updated mod list...")):
        #     url = "https://www.dokidokimodclub.com/api/mod/"
        #     headers = {'Authorization': 'Api-Key [REDACTED]'}
        #     context = ssl._create_unverified_context()
        #     req = urllib2.Request(url=url, headers=headers)
        #     response = urllib2.urlopen(req, context=context)
        #     the_page = response.read()

        channels = decode_list()
        if channels is None:
            interface.error(_("DDML was unable to find any mods from the mod list.\nCheck if 'ddmc.json' exists, then try again."))
            
        renpy.call_screen("update_channel", channels)

    jump front_page

