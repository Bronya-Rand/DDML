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
        This define checks if the ZIP is a valid DDLC mod.
        archive.
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
        This define extracts the game/tool archive to the temp folder.

        filePath - The given game zip package.\n
        modFolder - The mod folder inside the mod install folder.\n
        copy - Makes sure this is a copy or a ZIP we are working with.
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

        if not copy:
            shutil.rmtree(game_dir)

        if sys.platform == "darwin":
            if os.path.exists(
                os.path.join(
                    modFolder, "DDLC.app/Contents/Resources/autorun/game/scripts.rpa"
                )
            ):
                os.remove(
                    os.path.join(
                        modFolder,
                        "DDLC.app/Contents/Resources/autorun/game/scripts.rpa",
                    )
                )
        else:
            if os.path.exists(os.path.join(modFolder, "game/scripts.rpa")):
                os.remove(os.path.join(modFolder, "game/scripts.rpa"))

    def installation(self, filePath, modFolder, copy=False):
        """
        This define extracts the mod archive to the temp folder and installs it
        to the mod folder.

        filepath - The given mod zip package.\n
        modFolder - The mod folder inside the mod install folder.
        copy - Makes sure this is a copy or a ZIP we are working with.
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
                    if mod_src.endswith(self.ddlc_base_contents):
                        shutil.move(os.path.join(mod_src, f), os.path.join(dst_dir, f))
                    else:
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
