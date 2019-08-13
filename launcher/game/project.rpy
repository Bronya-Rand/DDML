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

# Code that manages projects.

init python:
    if renpy.windows:
        import EasyDialogsWin as EasyDialogs
    else:
        EasyDialogs = None

    import os

init python in project:
    from store import persistent, config, Action, renpy
    import store.util as util
    import store.interface as interface

    import sys
    import os.path
    import json
    import subprocess
    import re
    import tempfile

    if persistent.blurb is None:
        persistent.blurb = 0

    LAUNCH_BLURBS = [
        _("After making changes to the script, press shift+R to reload your game."),
        _("Press shift+O (the letter) to access the console."),
        _("Press shift+D to access the developer menu."),
        _("Have you backed up your projects recently?"),
    ]

    class Project(object):

        def __init__(self, path, name=None):

            if name is None:
                name = os.path.basename(path)

            while path.endswith("/"):
                path = path[:-1]

            if not os.path.exists(path):
                raise Exception("{} does not exist.".format(path))

            self.name = name

            # The path to the project.
            self.path = path

            # The path to the game directory.
            gamedir = os.path.join(path, "game")
            if os.path.isdir(gamedir):
                self.gamedir = gamedir
            else:
                self.gamedir = path

            # Load the data.
            self.load_data()

            # The project's temporary directory.
            self.tmp = None

            # This contains the result of dumping information about the game
            # to disk.
            self.dump = { }

            # The mtime of the last dump file loaded.
            self.dump_mtime = 0

        def get_dump_filename(self):
            self.make_tmp()
            return os.path.join(self.tmp, "navigation.json")

        def load_data(self):
            try:
                f = open(os.path.join(self.path, "project.json"), "rb")
                self.data = json.load(f)
                f.close()
            except:
                self.data = { }

            self.update_data()


        def save_data(self):
            """
            Saves the project data.
            """

            try:
                with open(os.path.join(self.path, "project.json"), "wb") as f:
                    json.dump(self.data, f)
            except:
                self.load_data()

        def update_data(self):
            data = self.data

            data.setdefault("build_update", False)
            data.setdefault("packages", [ "pc", "mac" ])
            data.setdefault("add_from", True)
            data.setdefault("force_recompile", True)

            if "renamed_all" not in data:
                dp = data["packages"]

                if "all" in dp:
                    dp.remove("all")

                    if "pc" not in dp:
                        dp.append("pc")

                    if "mac" not in dp:
                        dp.append("mac")

                data["renamed_all"] = True

        def make_tmp(self):
            """
            Makes the project's temporary directory, if it doesn't exist
            yet.
            """

            if self.tmp and os.path.isdir(self.tmp):
                return

            tmp = os.path.join(config.renpy_base, "tmp", self.name)

            try:
                os.makedirs(tmp)
            except:
                pass

            if os.path.isdir(tmp):
                self.tmp = tmp
                return

            self.tmp = tempfile.mkdtemp()

        def temp_filename(self, filename):
            """
            Returns a filename in the temporary directory.
            """

            self.make_tmp()
            return os.path.join(self.tmp, filename)

        def launch(self, args=[], wait=False, env={}):
            """
            Launches the project.

            `args`
                Additional arguments to give to the project.

            `wait`
                If true, waits for the launched project to terminate before
                continuing.

            `env`
                Additional variables to include in the environment.
            """

            self.make_tmp()

            # Find the python executable to run.
            executable_path = os.path.dirname(renpy.fsdecode(sys.executable))

            if renpy.renpy.windows:
                extension = ".exe"
            else:
                extension = ""

            if persistent.windows_console:
                executables = [ "python" + extension ]
            else:
                executables = [ "pythonw" + extension ]

            executables.append(sys.executable)

            for i in executables:
                executable = os.path.join(executable_path, i)
                if os.path.exists(executable):
                    break
            else:
                raise Exception("Python interpreter not found: %r", executables)

            # Put together the basic command line.
            cmd = [ executable, "-EO", sys.argv[0] ]

            cmd.append(self.path)
            cmd.extend(args)

            # Add flags to dump game info.
            cmd.append("--json-dump")
            cmd.append(self.get_dump_filename())

            if persistent.navigate_private:
                cmd.append("--json-dump-private")

            if persistent.navigate_library:
                cmd.append("--json-dump-common")

            environ = dict(os.environ)
            environ.update(env)

            encoded_environ = { }

            for k, v in environ.items():
                if v is None:
                    continue

                encoded_environ[renpy.fsencode(k)] = renpy.fsencode(v)

            # Launch the project.
            cmd = [ renpy.fsencode(i) for i in cmd ]

            p = subprocess.Popen(cmd, env=encoded_environ)

            if wait:
                if p.wait():
                    interface.error(_("Launching the project failed."), _("Please ensure that your project launches normally before running this command."))

        def update_dump(self, force=False, gui=True, compile=False):
            """
            If the dumpfile does not exist, runs Ren'Py to create it. Otherwise,
            loads it in iff it's newer than the one that's already loaded.
            """

            dump_filename = self.get_dump_filename()

            if force or not os.path.exists(dump_filename):

                if gui:
                    interface.processing(_("Ren'Py is scanning the project..."))

                if compile:
                    self.launch(["compile", "--keep-orphan-rpyc" ], wait=True)
                else:
                    self.launch(["quit"], wait=True)

            if not os.path.exists(dump_filename):
                self.dump["error"] = True
                return

            file_mtime = os.path.getmtime(dump_filename)
            if file_mtime == self.dump_mtime:
                return

            self.dump_mtime = file_mtime

            try:
                with open(dump_filename, "r") as f:
                    self.dump = json.load(f)
                # add todo list to dump data
                self.update_todos()

            except:
                self.dump["error"] = True

        def update_todos(self):
            """
            Scans the scriptfiles for lines TODO comments and add them to
            the dump data.
            """

            todos = self.dump.setdefault("location", {})["todo"] = {}

            files = self.script_files()

            for f in files:

                data = file(self.unelide_filename(f))

                for l, line in enumerate(data):
                    l += 1

                    try:
                        line = line.decode("utf-8")
                    except:
                        continue

                    m = re.search(ur".*#\s*TODO(\s*:\s*|\s+)(.*)", line, re.I)

                    if m is None:
                        continue

                    raw_todo_text = m.group(2).strip()
                    todo_text = raw_todo_text

                    index = 0

                    while not todo_text or todo_text in todos:
                        index += 1
                        todo_text = u"{0} ({1})".format(raw_todo_text, index)

                    todos[todo_text] = [f, l]


        def unelide_filename(self, fn):
            """
            Unelides the filename relative to the project base.
            """

            fn1 = os.path.join(self.path, fn)
            if os.path.exists(fn1):
                return fn1

            fn2 = os.path.join(config.renpy_base, fn)
            if os.path.exists(fn2):
                return fn2

            return fn

        def script_files(self):
            """
            Return a list of the script files that make up the project. These
            are elided, and so need to be passed to unelide_filename before they
            can be included in the project.
            """

            rv = [ ]
            rv.extend(i for i, isdir in util.walk(self.path)
                if (not isdir) and (i.endswith(".rpy") or i.endswith(".rpym")) and (not i.startswith("tmp/")) )

            return rv

        def exists(self, fn):
            """
            Returns true if the file exists in the game.
            """

            return os.path.exists(os.path.join(self.path, fn))


    class ProjectManager(object):
        """
        This maintains a list of the various types of projects that
        we know about.
        """

        def __init__(self):

           # The projects directory.
           self.projects_directory = ""

           # Normal projects, in alphabetical order by lowercase name.
           self.projects = [ ]

           # Template projects.
           self.templates = [ ]

           # All projects - normal, template, and hidden.
           self.all_projects = [ ]

           # Directories that have been scanned.
           self.scanned = set()

           self.scan()

        def scan(self):
            """
            Scans for projects.
            """

            if (persistent.projects_directory is not None) and not os.path.isdir(persistent.projects_directory):
                persistent.projects_directory = None

            self.projects_directory = persistent.projects_directory

            if (persistent.zip_directory is not None) and not os.path.isdir(persistent.zip_directory):
                persistent.zip_directory = None

            self.ddlc_directory = persistent.zip_directory

            if (persistent.mzip_directory is not None) and not os.path.isdir(persistent.mzip_directory):
                persistent.mzip_directory = None

            self.ddlcmod_directory = persistent.zip_directory

            self.projects = [ ]
            self.templates = [ ]
            self.all_projects = [ ]
            self.scanned = set()

            if self.projects_directory is not None:
                self.scan_directory(self.projects_directory)

            self.scan_directory(config.renpy_base)
            self.scan_directory(os.path.join(config.renpy_base, "templates"))

            self.projects.sort(key=lambda p : p.name.lower())
            self.templates.sort(key=lambda p : p.name.lower())


        def find_basedir(self, d):
            """
            Try to find a project basedir in d.
            """

            def has_game(dn):
                return os.path.isdir(os.path.join(dn, "game"))

            if has_game(d):
                return d

            dn = os.path.join(d, "Contents", "Resources", "autorun")
            if has_game(dn):
                return dn

            for dn in os.listdir(d):
                if not dn.endswith(".app"):
                    continue

                dn = os.path.join(d, dn, "Contents", "Resources", "autorun")

                if has_game(dn):
                    return dn

            return None

        def scan_directory(self, d):
            """
            Scans for projects in directories directly underneath `d`.
            """

            global current

            d = os.path.abspath(d)

            if not os.path.isdir(d):
                return

            for pdir in util.listdir(d):

                ppath = os.path.join(d, pdir)

                # A project must be a directory.
                if not os.path.isdir(ppath):
                    continue

                try:
                    ppath = self.find_basedir(ppath)
                except:
                    continue

                if ppath is None:
                    continue

                if ppath in self.scanned:
                    continue

                self.scanned.add(ppath)

                # We have a project directory, so create a Project.
                p = Project(ppath, pdir)

                project_type = p.data.get("type", "normal")

                if project_type == "hidden":
                    pass
                elif project_type == "template":
                    self.templates.append(p)
                else:
                    self.projects.append(p)

                self.all_projects.append(p)

            # Select the default project.
            if persistent.active_project is not None:
                p = self.get(persistent.active_project)

                if p is not None:
                    current = p
                    return

            p = self.get("tutorial")
            if p is not None:
                current = p
                return

            current = None


        def get(self, name):
            """
            Gets the project with the given name.

            Returns None if the project doesn't exist.
            """

            for p in self.all_projects:
                if p.name == name:
                    return p

            return None

    manager = ProjectManager()

    # The current project.
    current = None

    # Actions
    class Select(Action):
        """
        An action that causes p to become the selected project when it was
        clicked. If label is not None, jumps to the given label.
        """

        def __init__(self, p, label=None):
            """
            `p`
                Either a project object, or a string giving the name of a
                project.

            `label`
                The label to jump to when clicked.
            """

            if isinstance(p, basestring):
                p = manager.get(p)

            self.project = p
            self.label = label

        def get_selected(self):
            if self.project is None:
                return False

            if current is None:
                return False

            return current.path == self.project.path

        def get_sensitive(self):
            return self.project is not None

        def __call__(self):
            global current

            current = self.project
            persistent.active_project = self.project.name

            renpy.restart_interaction()

            if self.label is not None:
                renpy.jump(self.label)


    class Launch(Action):
        """
        An action that launches the supplied project, or the current
        project if no project is supplied.
        """

        def __init__(self, p=None):
            if p is None:
                self.project = current
            elif isinstance(p, basestring):
                self.project = manager.get(p)
            else:
                self.project = p

        def get_sensitive(self):
            return self.project is not None

        def post_launch(self):
            blurb = LAUNCH_BLURBS[persistent.blurb % len(LAUNCH_BLURBS)]
            persistent.blurb += 1

            interface.interaction(_("Launching"), blurb, pause=2.5)


        def __call__(self):
            self.project.launch()
            renpy.invoke_in_new_context(self.post_launch)

    class Rescan(Action):
        def __call__(self):
            """
            Rescans the projects directory.
            """

            manager.scan()
            renpy.restart_interaction()


    manager.scan()

    if isinstance(persistent.projects_directory, str):
        persistent.projects_directory = renpy.fsdecode(persistent.projects_directory)

init 10 python:
    if persistent.projects_directory is not None:
        if not directory_is_writable(persistent.projects_directory):
            persistent.projects_directory = None

###############################################################################
# Code to choose the projects directory.

label choose_projects_directory:

    python hide:

        interface.interaction(_("Mod Directory"), _("Please choose the Mod directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"), _("This launcher will scan for mods in this directory, will create new mods and DDLC Installs, and will place mods and DDLC into this directory."),)

        path, is_default = choose_directory(persistent.projects_directory)

        if is_default:
            interface.info(_("DDML has set the Mod directory to:"), "[path!q]", path=path)

        persistent.projects_directory = path

        project.manager.scan()

    return

label move_mod_folder:

    python hide:

        import os
        import shutil

        oldmod_dir = persistent.projects_directory

        interface.interaction(_("Mod Directory"), _("Please choose the new mod directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"), _("This launcher will create new mods in this directory, and will place old and new mods into this directory."),)

        pathnew, is_default = choose_directory(persistent.projects_directory)

        if is_default:
            interface.error(_("The operation has been cancelled."))

        persistent.projects_directory = pathnew

        #Moving Files!
        for file in os.listdir(oldmod_dir):
            print file
            src_file = os.path.join(oldmod_dir, file)
            dst_file = os.path.join(persistent.projects_directory, file)
            shutil.move(src_file, dst_file)

        project.manager.scan()

    return


label choose_modzip_directory:

    python hide:

        interface.interaction(_("Mod ZIP Download Directory"), _("Please choose the directory in which your Mod ZIP is located."), _("This will make DDML find the Mod ZIP in this folder."),)

        pathmz, is_defaultmz = choose_directory(persistent.mzip_directory)

        if is_defaultmz:
            interface.error(_("The operation has been cancelled."))

        persistent.mzip_directory = pathmz

    return

label delete_mod_folder:

    python hide:

        mod_delete_response = interface.input(
            _("Deleting a Mod"),
            _("Are you sure you want to delete this mod? Type either Yes or No."),
            filename=False,
            cancel=Jump("front_page"))

        mod_delete_response = mod_delete_response.strip()

        if not mod_delete_response:
            interface.error(_("The operation has been cancelled."))

        mod_response = mod_delete_response

        if mod_response == "No" or mod_response == "no":
            interface.error(_("The operation has been cancelled."))
        elif mod_response == "Yes" or mod_response == "yes":
            deleted_mod_name = project.current.name
            shutil.rmtree(persistent.projects_directory + '/' + project.current.name)
        else:
            interface.error(_("Invalid Input."))

        interface.info(deleted_mod_name + " has been deleted.")
        deleted_mod_name = None

        project.manager.scan()

    jump front_page

label add_a_mod:

    # Checks if user set Mod Install Folder
    if persistent.projects_directory is None:
        call choose_projects_directory

    # Ren'Py Failsafe
    if persistent.projects_directory is None:
        $ interface.error(_("The Mod directory could not be set. Giving up."))
    # Checks if user set DDLC ZIP Location (All OS)
    if persistent.zip_directory is None:
        call ddlc_location

    # Ren'Py Failsafe 2
    if persistent.zip_directory is None:
        $ interface.error(_("The DDLC ZIP directory could not be set. Giving up."))

    # Checks if User set Mod ZIP Directory
    if persistent.mzip_directory is None:
        call choose_modzip_directory

    # Ren'Py Failsafe 3
    if persistent.mzip_directory is None:
        $ interface.error(_("The Mod ZIP directory could not be set. Giving up."))

    python hide:

        # Asks User the name of the folder they want their mod folder to be
        modinstall_foldername = interface.input(
            _("Mod Folder Name"),
            _("Please enter the name of your project:"),
            filename=True,
            cancel=Jump("front_page"))

        modinstall_foldername = modinstall_foldername.strip()
        if not modinstall_foldername:
            interface.error(_("The mod name may not be empty."))

        project_dir = os.path.join(persistent.projects_directory, modinstall_foldername)

        if project.manager.get(modinstall_foldername) is not None:
            interface.error(_("[modinstall_foldername!q] already exists. Please choose a different project name."), modinstall_foldername=modinstall_foldername)

        if os.path.exists(project_dir):
            interface.error(_("[project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir)

        interface.interaction(_("Making a Mod Folder"), _("Extracting DDLC, Please Wait..."),)

        if persistent.steam_release == True:
            # Copy DDLC (Win) (Steam Release) (Assuming Steam Copy is Unmodded)
            import zipfile
            import shutil

            try: shutil.copytree(persistent.zip_directory + "/Doki Doki Literature Club", project_dir)
            except:
                interface.error(_("Cannot Locate Your Doki Doki Literature Club Folder"), _("Make sure it is set to your 'Steam\steamapps\common' folder."),)
        else:
            # Extract DDLC (Win/Linux) (Moe/ZIP Release)
            import zipfile

            try: 
                with zipfile.ZipFile(persistent.zip_directory + '/ddlc-win.zip', "r") as z:
                    z.extractall(persistent.projects_directory + "/temp")

                    ddlc = persistent.projects_directory + '/temp' + '/DDLC-1.1.1-pc'

            except: interface.error(_("Cannot Locate 'ddlc-win.zip' in [persistent.zip_directory!q]."), _("Make sure you have DDLC downloaded from 'https://ddlc.moe' and check if it exists."),)

            import shutil

            shutil.move(ddlc, project_dir)

        # Asks User name of ZIP (Ren'Py already states only ASCII)
        modzip_name = interface.input(
            _("Mod ZIP Name"),
            _("Please enter the name of your Mod ZIP File. It is recommended to rename the ZIP for easy installation."),
            filename=True,
            cancel=Jump("front_page"))

        modzip_name = modzip_name.strip()
        if not modzip_name:
            interface.error(_("The mod zip name may not be empty."))

        # Extract Mod
        interface.interaction(_("Extracting"), _("Extracting Mod ZIP, Please Wait..."),)

        try:
            with zipfile.ZipFile(persistent.mzip_directory + '/' + modzip_name + ".zip", "r") as z:
                z.extractall(persistent.projects_directory + "/temp")

                mzt = persistent.projects_directory + "/temp"

        except: 
            interface.error(_("Cannot locate ZIP in [persistent.mzip_directory!q]."), _("Check the name of your Mod ZIP File and try again."))
        import glob

        mzte = [x[0] for x in os.walk(mzt)]

        try:
            mzte[1]
            if (str(mzte[1]) == mzt + "\\cache" or str(mzte[1]) == mzt + "\\gui" or str(mzte[1]) == mzt + "\\mod_assets" or str(mzte[1]) == mzt + "\\images" or str(mzte[1]) == mzt + "\\fonts" or str(mzte[1]) == mzt + "\\audio" or str(mzte[1]) == mzt + "\\python-packages" or str(mzte[1]) == mzt + "\\saves" or str(mzte[1]) == mzt + "\\submods"):
                mztex = False
            else:
                mztex = True
        except IndexError:
            mztex = False

        if mztex == False:
            #Normal Scanning
            
            if glob.glob(mzt + '/game'):
                shutil.move(mzt + '/game', project_dir)
            else:
                import os
                for file in os.listdir(mzt):
                    print file
                    src_file = os.path.join(mzt, file)
                    dst_file = os.path.join(project_dir + '/game', file)
                    shutil.move(src_file, dst_file)
        else:
            #Extended Scanning (If Contents during extract are inside another folder (Yuri-1.0/script-ch1.rpyc))
            if glob.glob(str(mzte[1]) + '/game'):
                for file in os.listdir(str(mzte[1]) + '/game'):
                    print file
                    src_file = os.path.join(str(mzte[1]) + '/game', file)
                    dst_file = os.path.join(project_dir + '/game', file)
                    shutil.move(src_file, dst_file)
            else:
                import os
                for file in os.listdir(str(mzte[1])):
                    print file
                    src_file = os.path.join(str(mzte[1]), file)
                    dst_file = os.path.join(project_dir + '/game', file)
                    shutil.move(src_file, dst_file)

        # Prevents copy of any other RPA or other mod files
        shutil.rmtree(persistent.projects_directory + '/temp')

        # Auto-Refresh
        project.manager.scan()

    return

label add_base_game:

    # Checks if user set Mod Install Folder
    if persistent.projects_directory is None:
        call choose_projects_directory

    # Ren'Py Failsafe
    if persistent.projects_directory is None:
        $ interface.error(_("The Mod directory could not be set. Giving up."))

    # Checks if user set DDLC ZIP Location (All OS)
    if persistent.zip_directory is None:
        call ddlc_location

    # Ren'Py Failsafe 2
    if persistent.zip_directory is None:
        $ interface.error(_("The DDLC ZIP directory could not be set. Giving up."))

    python hide:
        # Asks User the name of the folder they want their mod folder to be
        modinstall_foldername = interface.input(
            _("DDLC Folder Name"),
            _("Please enter the name of your DDLC folder:"),
            filename=True,
            cancel=Jump("front_page"))

        modinstall_foldername = modinstall_foldername.strip()
        if not modinstall_foldername:
            interface.error(_("The folder name may not be empty."))

        project_dir = os.path.join(persistent.projects_directory, modinstall_foldername)

        if project.manager.get(modinstall_foldername) is not None:
            interface.error(_("[modinstall_foldername!q] already exists. Please choose a different folder name."), modinstall_foldername=modinstall_foldername)

        if os.path.exists(project_dir):
            interface.error(_("[project_dir!q] already exists. Please choose a different name."), project_dir=project_dir)

        interface.interaction(_("Making a DDLC Folder"), _("Extracting DDLC, Please Wait..."),)

        if persistent.steam_release == True:
            # Copy DDLC (Steam Release)
            import shutil

            try:
                shutil.copytree(persistent.zip_directory + "/Doki Doki Literature Club", project_dir)
            except:
                interface.error(_("Cannot Locate Your Doki Doki Literature Club Folder"), _("Make sure it is set to your 'Steam\steamapps\common' folder."),)

        else:

            # Extract DDLC (Win/Linux)
            import zipfile

            try:
                with zipfile.ZipFile(persistent.zip_directory + '/ddlc-win.zip', "r") as z:
                    z.extractall(persistent.projects_directory + "/temp")

                    ddlc = persistent.projects_directory + '/temp' + '/DDLC-1.1.1-pc'

            except:
                interface.error(_("Cannot Locate 'ddlc-win.zip' in [persistent.zip_directory!q]."), _("Make sure you have DDLC downloaded from 'https://ddlc.moe' and check if it exists."),)

            import shutil

            shutil.move(ddlc, project_dir)

            # Prevents copy of any other RPA or other mod files
            shutil.rmtree(persistent.projects_directory + '/temp')

        project.manager.scan()

    return

label scripts_rpa:

    python hide:
        script_choice = interface.choice(
                _("Some mods may require scripts.rpa to be removed in order to run. Are you sure you want to continue?"),
                [ ( 'delete_scripts', _("Yes") ), ( 'front_page', _("No")) ],
                "front_page",
                cancel=Jump("front_page"),
                )

        renpy.jump(script_choice)

label delete_scripts:

    python hide:
        interface.interaction(_("Deleting scripts.rpa"), _("Please wait..."),)

        import os
        try: os.remove(persistent.projects_directory + "/" + project.current.name + "/game/scripts.rpa")
        except: interface.error(_("images.rpa already deleted or is missing."), _("Check the game directory and try again."))
        
        interface.info("scripts.rpa has been deleted.")

    jump front_page

label images_rpa:
    python hide:
        image_choice = interface.choice(
                _("Some mods may require images.rpa to be removed in order to run. Are you sure you want to continue?"),
                [ ( 'delete_images', _("Yes") ), ( 'front_page', _("No")) ],
                "front_page",
                cancel=Jump("front_page"),
                )

        renpy.jump(image_choice)

label delete_images:

    python hide:
        interface.interaction(_("Deleting images.rpa"), _("Please wait..."),)

        import os
        try: os.remove(persistent.projects_directory + "/" + project.current.name + "/game/images.rpa")
        except: interface.error(_("images.rpa already deleted or is missing.") _("Check the game directory and try again."))
        
        interface.info("images.rpa has been deleted.")

    jump front_page

init python:

    def set_projects_directory_command():
        ap = renpy.arguments.ArgumentParser()
        ap.add_argument("projects", help="The path to the projects directory.")

        args = ap.parse_args()

        persistent.projects_directory = renpy.fsdecode(args.projects)
        renpy.save_persistent()

        return False

    renpy.arguments.register_command("set_projects_directory", set_projects_directory_command)

    def get_projects_directory_command():
        ap = renpy.arguments.ArgumentParser()
        args = ap.parse_args()

        print renpy.fsencode(persistent.projects_directory)

        return False

    renpy.arguments.register_command("get_projects_directory", get_projects_directory_command)
