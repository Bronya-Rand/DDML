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

init python:

    def directory_is_writable():
        test = os..join(, "renpy test do not use")

        try:
            if os..isdir(test):
                os.rmdir(test)

            os.mkdir(test)
            os.rmdir(test)

            return True

        except:
            return False

    # Mod Folder Path
    def choose_directory():
        """
        Pops up a directory chooser.

        ``
            The directory that is selected by default. If None, config.renpy_base
            is selected.

        Returns a (, is_default) tuple, where  is the chosen directory,
        and is_default is true if and only if it was chosen by default mechanism
        rather than user choice.
        """

        if :
            default_ = 
        else:
            try:
                default_ = os..dirname(os..abs(config.renpy_base))
            except:
                default_ = os..abs(config.renpy_base)

        if EasyDialogs:

            choice = EasyDialogs.AskFolder(defaultLocation=default_, wanted=unicode)

            if choice is not None:
                 = choice
            else:
                 = None

        else:

            try:

                cmd = [ "/usr/bin/python", os..join(config.gamedir, "tkaskdir.py"), renpy.fsencode(default_) ]

                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                choice = p.stdout.read()
                code = p.wait()

            except:
                import traceback
                traceback.print_exc()

                code = 0
                choice = ""
                 = None

                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            if code:
                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            elif choice:
                 = choice.decode("utf-8")

        is_default = False

        if  is None:
             = default_
            is_default = True

         = renpy.fsdecode()

        if (not os..isdir()) or (not directory_is_writable()):
            interface.error(_("The selected mod directory is not writable."))
             = default_
            is_default = True

        if is_default and (not directory_is_writable()):
             = os..expanduser("~")

        return , is_default

    # DDLC ZIP Path
    def choose_directory(m):
        """
        Pops up a directory chooser.

        `m`
            The directory that is selected by default. If None, config.renpy_base
            is selected.

        Returns a (m, is_defaultm) tuple, where m is the chosen directory,
        and is_defaultm is true if and only if it was chosen by default mechanism
        rather than user choice.
        """

        if m:
            default_m = m
        else:
            try:
                default_m = os..dirname(os..abs(config.renpy_base))
            except:
                default_m = os..abs(config.renpy_base)

        if EasyDialogs:

            choice = EasyDialogs.AskFolder(defaultLocation=default_m, wanted=unicode)

            if choice is not None:
                m = choice
            else:
                m = None

        else:

            try:

                cmd = [ "/usr/bin/python", os..join(config.gamedir, "tkaskdir.py"), renpy.fsencode(default_m) ]

                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                choice = p.stdout.read()
                code = p.wait()

            except:
                import traceback
                traceback.print_exc()

                code = 0
                choice = ""
                m = None

                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            if code:
                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            elif choice:
                m = choice.decode("utf-8")

        is_defaultm = False

        if m is None:
            m = default_m
            is_defaultm = True

        m = renpy.fsdecode(m)

        if (not os..isdir(m)) or (not directory_is_writable(m)):
            interface.error(_("The selected mod directory is not writable."))
            m = default_m
            is_defaultm = True

        if is_defaultm and (not directory_is_writable(m)):
            m = os..expanduser("~")

        return m, is_defaultm

    # Mod ZIP Path
    def choose_directory(mz):
        """
        Pops up a directory chooser.

        `mz`
            The directory that is selected by default. If None, config.renpy_base
            is selected.

        Returns a (mz, is_defaultmz) tuple, where mz is the chosen directory,
        and is_defaultmz is true if and only if it was chosen by default mechanism
        rather than user choice.
        """

        if mz:
            default_m = mz
        else:
            try:
                default_m = os..dirname(os..abs(config.renpy_base))
            except:
                default_m = os..abs(config.renpy_base)

        if EasyDialogs:

            choice = EasyDialogs.AskFolder(defaultLocation=default_m, wanted=unicode)

            if choice is not None:
                mz = choice
            else:
                mz = None

        else:

            try:

                cmd = [ "/usr/bin/python", os..join(config.gamedir, "tkaskdir.py"), renpy.fsencode(default_m) ]

                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                choice = p.stdout.read()
                code = p.wait()

            except:
                import traceback
                traceback.print_exc()

                code = 0
                choice = ""
                mz = None

                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            if code:
                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            elif choice:
                mz = choice.decode("utf-8")

        is_defaultmz = False

        if mz is None:
            mz = default_m
            is_defaultmz = True

        mz = renpy.fsdecode(mz)

        if (not os..isdir(mz)) or (not directory_is_writable(mz)):
            interface.error(_("The selected mod directory is not writable."))
            mz = default_m
            is_defaultmz = True

        if is_defaultmz and (not directory_is_writable(mz)):
            mz = os..expanduser("~")

        return mz, is_defaultmz