# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

    def directory_is_writable(pathm):
        testm = os.path.join(pathm, "renpy test do not use")

        try:
            if os.path.isdir(testm):
                os.rmdir(testm)

            os.mkdir(testm)
            os.rmdir(testm)

            return True

        except:
            return False

    def directory_is_writable(pathmz):
        testmz = os.path.join(pathmz, "renpy test do not use")

        try:
            if os.path.isdir(testmz):
                os.rmdir(testmz)

            os.mkdir(testmz)
            os.rmdir(testmz)

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

        # Path being None or "" means nothing was selected.
        if not path:
            path = default_path
            is_default = True

        path = renpy.fsdecode(path)

        if (not os.path.isdir(path)) or (not directory_is_writable(path)):
            interface.error(_("The selected projects directory is not writable."))
            path = default_path
            is_default = True

        if is_default and (not directory_is_writable(path)):
            path = os.path.expanduser("~")

        return path, is_default

    def choose_directory(pathm):
        """
        Pops up a directory chooser.
        `pathm`
            The directory that is selected by default. If None, config.renpy_base
            is selected.
        Returns a (pathm, is_defaultm) tuple, where pathm is the chosen directory,
        and is_defaultm is true if and only if it was chosen by default mechanism
        rather than user choice.
        """

        if pathm:
            default_pathm = pathm
        else:
            try:
                default_pathm = os.path.dirname(os.path.abspath(config.renpy_base))
            except:
                default_pathm = os.path.abspath(config.renpy_base)

        if EasyDialogs:

            choice = EasyDialogs.AskFolder(defaultLocation=default_pathm, wanted=unicode)

            if choice is not None:
                pathm = choice
            else:
                pathm = None

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
                pathm = None

                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            if code:
                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            elif choice:
                pathm = choice.decode("utf-8")

        is_defaultm = False

        # pathm being None or "" means nothing was selected.
        if not pathm:
            pathm = default_pathm
            is_defaultm = True

        pathm = renpy.fsdecode(pathm)

        if (not os.path.isdir(pathm)) or (not directory_is_writable(pathm)):
            interface.error(_("The selected projects directory is not writable."))
            pathm = default_pathm
            is_defaultm = True

        if is_defaultm and (not directory_is_writable(pathm)):
            pathm = os.path.expanduser("~")

        return pathm, is_defaultm

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
            default_pathmz = pathmz
        else:
            try:
                default_pathmz = os.path.dirname(os.path.abspath(config.renpy_base))
            except:
                default_pathmz = os.path.abspath(config.renpy_base)

        if EasyDialogs:

            choice = EasyDialogs.AskFolder(defaultLocation=default_pathmz, wanted=unicode)

            if choice is not None:
                pathmz = choice
            else:
                pathmz = None

        else:

            try:

                cmd = [ "/usr/bin/python", os.path.join(config.gamedir, "tkaskdir.py"), renpy.fsencode(default_pathmz) ]

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

        # pathmz being None or "" means nothing was selected.
        if not pathmz:
            pathmz = default_pathmz
            is_defaultmz = True

        pathmz = renpy.fsdecode(pathmz)

        if (not os.path.isdir(pathmz)) or (not directory_is_writable(pathmz)):
            interface.error(_("The selected projects directory is not writable."))
            pathmz = default_pathmz
            is_defaultmz = True

        if is_defaultmz and (not directory_is_writable(pathmz)):
            pathmz = os.path.expanduser("~")

        return pathmz, is_defaultmz
