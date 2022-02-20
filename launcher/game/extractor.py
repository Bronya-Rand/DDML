from zipfile import ZipFile
import tempfile
import os
import shutil
import sys


class Extractor:
    """
    This class is responsible for the extraction of
    zip files for DDLC mods.
    """

    def __init__(self):
        self.renpy_script_contents = (".rpa", ".rpyc", ".rpy")
        self.ddlc_base_contents = ("characters", "game", "lib", "renpy")
        self.renpy_executables = (".exe", ".sh", ".app")

    def valid_zip(self, filePath):
        """
        Returns whether the given ZIP file is a valid Ren'Py/DDLC mod ZIP file.

            filePath - the direct path to the ZIP file.
        """

        contents = []

        with ZipFile(filePath, "r") as z:
            contents = z.namelist()

        for x in contents:
            if x.endswith((self.renpy_script_contents)):
                contents = []
                return True

        return False

    def game_installation(self, filePath, modFolder, copy=False):
        """
        Extracts DDLC/Ren'Py game to the mod folder.

            filePath - The given game zip package.

            modFolder - The mod folder inside the mod install folder.

            copy - Makes sure this is a folder or a ZIP we are working with.
        """

        os.makedirs(modFolder)

        if not copy:
            td = tempfile.mkdtemp(prefix="NewDDML_", suffix="_TempGame")

            with ZipFile(filePath, "r") as z:
                z.extractall(td)

            if sys.platform == "darwin":
                game_dir = td
            else:
                game_dir = os.path.join(td, os.listdir(td)[-1])
        else:
            game_dir = filePath

        for temp_src, dirs, files in os.walk(game_dir):
            dst_dir = temp_src.replace(game_dir, modFolder)

            for d in dirs:
                if not os.path.exists(os.path.join(dst_dir, d)):
                    os.makedirs(os.path.join(dst_dir, d))

            for f in files:
                shutil.move(os.path.join(temp_src, f), os.path.join(dst_dir, f))

    def installation(self, filePath, modFolder, copy=False):
        """
        Extracts the mod archive to the mod folder and attempts to fix the mod
        for Ren'Py structure compliance.

            filepath - The given mod zip package.

            modFolder - The mod folder inside the mod install folder.

            copy - Makes sure this is a folder or a ZIP we are working with.
        """

        if not copy:
            mod_dir = tempfile.mkdtemp(prefix="NewDDML_", suffix="_TempArchive")

            with ZipFile(filePath, "r") as z:
                z.extractall(mod_dir)
        else:
            mod_dir = filePath

        base_files_dir = None

        # Check if the folder copy/extracted has a Renpy7Mod/Mod folder or game
        # folder inside to set directory.
        for mod_src, dirs, files in os.walk(mod_dir):
            for d in dirs:
                if d.endswith(("Renpy7Mod", "Mod")):
                    base_files_dir = os.path.join(mod_src, d)
                elif d.endswith(("game")):
                    base_files_dir = mod_src
                elif os.path.exists(os.path.join(mod_src, d, "game")):
                    base_files_dir = os.path.join(mod_src, d)

        # If we were unable to get a directory from the above check, fix the archive
        # by sending it to an new temp folder and applying fixes.
        if not base_files_dir:
            fix_dir = tempfile.mkdtemp(prefix="NewDDML_", suffix="_TempFixArchive")
            os.makedirs(os.path.join(fix_dir, "game"))

            for mod_src, dirs, files in os.walk(mod_dir):
                dst_dir = mod_src.replace(mod_dir, fix_dir)

                for d in dirs:
                    if mod_src.endswith(self.ddlc_base_contents):
                        if not os.path.exists(os.path.join(dst_dir, d)):
                            os.makedirs(os.path.join(dst_dir, d))
                    else:
                        if not os.path.exists(os.path.join(dst_dir, "game", d)):
                            os.makedirs(os.path.join(dst_dir, "game", d))

                for f in files:
                    if f.endswith(self.renpy_executables):
                        shutil.move(os.path.join(mod_src, f), os.path.join(dst_dir, f))
                    elif f.endswith(".py") and os.path.join(mod_src, f) == os.path.join(mod_dir, f):
                        shutil.move(os.path.join(mod_src, f), os.path.join(dst_dir, f))
                    elif mod_src.endswith(self.ddlc_base_contents):
                        if os.path.exists(os.path.join(dst_dir, f)):
                            if os.path.samefile(os.path.join(mod_src, f), os.path.join(dst_dir, f)):
                                continue

                            os.remove(os.path.join(dst_dir, f))

                        shutil.move(os.path.join(mod_src, f), os.path.join(dst_dir, f))
                    else:
                        if os.path.exists(os.path.join(mod_src.replace(mod_dir, fix_dir + "/game"), f)):
                            if os.path.samefile(os.path.join(mod_src.replace(mod_dir, fix_dir + "/game"), f), os.path.join(dst_dir, f)):
                                continue
                            
                            os.remove(os.path.join(mod_src.replace(mod_dir, fix_dir + "/game"), f))

                        shutil.move(
                            os.path.join(mod_src, f),
                            os.path.join(
                                mod_src.replace(mod_dir, fix_dir + "/game"), f
                            ),
                        )

            # Set the directory to the fixed mod folder
            base_files_dir = fix_dir

        if sys.platform == "darwin":
            modFolder = os.path.join(modFolder, "DDLC.app/Contents/Resources/autorun")

        for mod_src, dirs, files in os.walk(base_files_dir):
            dst_dir = mod_src.replace(base_files_dir, modFolder)

            for d in dirs:
                if not os.path.exists(os.path.join(dst_dir, d)):
                    os.makedirs(os.path.join(dst_dir, d))

            for f in files:
                shutil.move(os.path.join(mod_src, f), os.path.join(dst_dir, f))
