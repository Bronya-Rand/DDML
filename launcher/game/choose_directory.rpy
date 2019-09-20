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

init python:

    def directory_is_writable(path):
        test = os.path.join(path, "renpy test do not use")

        try:
            if os.path.isdir(test):
                os.rmdir(test)

            os.mkdir(test)
            os.rmdir(test)

            return True

        except:
            return False

    def choose_directory(path):
        """
        Pops up a directory chooser.

        `path`
            The directory that is selected by default. If None, config.renpy_base
            is selected.

        Returns a (path, is_default) tuple, where path is the chosen directory,
        and is_default is true if and only if it was chosen by default mechanism
        rather than user choice.
        """

        if path:
            default_path = path
        else:
            try:
                default_path = os.path.dirname(os.path.abspath(config.renpy_base))
            except:
                default_path = os.path.abspath(config.renpy_base)

        if EasyDialogs:

            choice = EasyDialogs.AskFolder(defaultLocation=default_path, wanted=unicode)

            if choice is not None:
                path = choice
            else:
                path = None

        else:

            try:

                cmd = [ "/usr/bin/python", os.path.join(config.gamedir, "tkaskdir.py"), renpy.fsencode(default_path) ]

                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                choice = p.stdout.read()
                code = p.wait()

            except:
                import traceback
                traceback.print_exc()

                code = 0
                choice = ""
                path = None

                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            if code:
                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            elif choice:
                path = choice.decode("utf-8")

        is_default = False

        if path is None:
            path = default_path
            is_default = True

        path = renpy.fsdecode(path)

        if (not os.path.isdir(path)) or (not directory_is_writable(path)):
            interface.error(_("The selected mod directory is not writable."))
            path = default_path
            is_default = True

        if is_default and (not directory_is_writable(path)):
            path = os.path.expanduser("~")

        return path, is_default

    # DDLC ZIP/ Mod Chooser
    def choose_directory(pathz):
        """
        Pops up a directory chooser.
        `pathz`
            The directory that is selected by default. If None, config.renpy_base
            is selected.
        Returns a (pathz, is_defaultm) tuple, where pathz is the chosen directory,
        and is_defaultm is true if and only if it was chosen by default mechanism
        rather than user choice.
        """

        if pathz:
            default_pathm = pathz
        else:
            try:
                default_pathm = os.path.dirname(os.path.abspath(config.renpy_base))
            except:
                default_pathm = os.path.abspath(config.renpy_base)

        if EasyDialogs:

            choice = EasyDialogs.AskFolder(defaultLocation=default_pathm, wanted=unicode)

            if choice is not None:
                pathz = choice
            else:
                pathz = None

        else:

            try:

                cmd = [ "/usr/bin/python", os.path.join(config.gamedir, "tkaskdir.py"), renpy.fsencode(default_pathm) ]

                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                choice = p.stdout.read()
                code = p.wait()

            except:
                import traceback
                traceback.print_exc()

                code = 0
                choice = ""
                pathz = None

                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            if code:
                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            elif choice:
                pathz = choice.decode("utf-8")

        is_defaultm = False

        if pathz is None:
            pathz = default_pathm
            is_defaultm = True

        pathz = renpy.fsdecode(pathz)

        if (not os.path.isdir(pathz)) or (not directory_is_writable(pathz)):
            interface.error(_("The selected mod directory is not writable."))
            pathz = default_pathm
            is_defaultm = True

        if is_defaultm and (not directory_is_writable(pathz)):
            pathz = os.path.expanduser("~")

        return pathz, is_defaultm

    def choose_directory(pathmz):
        """
        Pops up a directory chooser.

        `pathmz`
            The directory that is selected by default. If None, config.renpy_base
            is selected.

        Returns a (pathmz, is_defaultmz) tuple, where pathmz is the chosen directory,
        and is_defaultmz is true if and only if it was chosen by default mechanism
        rather than user choice.
        """

        if pathmz:
            default_pathm = pathmz
        else:
            try:
                default_pathm = os.path.dirname(os.path.abspath(config.renpy_base))
            except:
                default_pathm = os.path.abspath(config.renpy_base)

        if EasyDialogs:

            choice = EasyDialogs.AskFolder(defaultLocation=default_pathm, wanted=unicode)

            if choice is not None:
                pathmz = choice
            else:
                pathmz = None

        else:

            try:

                cmd = [ "/usr/bin/python", os.path.join(config.gamedir, "tkaskdir.py"), renpy.fsencode(default_pathm) ]

                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                choice = p.stdout.read()
                code = p.wait()

            except:
                import traceback
                traceback.print_exc()

                code = 0
                choice = ""
                pathmz = None

                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            if code:
                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            elif choice:
                pathmz = choice.decode("utf-8")

        is_defaultmz = False

        if pathmz is None:
            pathmz = default_pathm
            is_defaultmz = True

        pathmz = renpy.fsdecode(pathmz)

        if (not os.path.isdir(pathmz)) or (not directory_is_writable(pathmz)):
            interface.error(_("The selected mod directory is not writable."))
            pathmz = default_pathm
            is_defaultmz = True

        if is_defaultmz and (not directory_is_writable(pathmz)):
            pathmz = os.path.expanduser("~")

        return pathmz, is_defaultmz