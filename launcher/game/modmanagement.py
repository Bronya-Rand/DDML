import os
import shutil
import sys


class ModManagement:
    """
    This class manages what the user can do to a mod in the mod launcher.
    """

    def delete_mod(self, modFolder, modName):
        """
        This define deletes a mod folder from the mod install folder if
        confirmed by the user.
        """

        for mod_src, dirs, files in os.walk(os.path.join(modFolder, modName)):
            for f in files:
                os.remove(os.path.join(mod_src, f))
            
            for d in dirs:
                shutil.rmtree(os.path.join(mod_src, d))

        shutil.rmtree(os.path.join(modFolder, modName))

    def move_mod_folder(self, modFolder, newModFolder):
        """
        This define moves the contents of the old mod install folder to the new
        mod install folder.
        """

        for mod_src, dirs, files in os.walk(modFolder):
            dst_dir = mod_src.replace(modFolder, newModFolder)

            for d in dirs:
                shutil.move(os.path.join(mod_src, d), os.path.join(dst_dir, d))

    def delete_rpa(self, modFolder, rpaName):
        """
        This define deletes a RPA from the mod folder if confirmed by the user.
        """

        if sys.platform == "darwin":
            modFolder = os.path.join(modFolder, "DDLC.app/Contents/Resources/autorun/game")
        else:
            modFolder = os.path.join(modFolder, "game")

        os.remove(os.path.join(modFolder, rpaName))
