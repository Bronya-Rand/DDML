
import shutil
import os
from launcher.game.modmanagement import ModManagement
import sys
from renpy import config

class DDMM_Compatibility:
    '''
    This class adds DDMM (Mod Manager) compatibility features to DDML.
    '''

    def __init__(self) -> None:
        # The DDMM directory in Windows
        self.ddmm_gamedir = os.path.join(os.getenv("APPDATA"), 
                            "DokiDokiModManager/GameData/installs")
        self.traceback_file = os.path.join(config.basedir, 
                            "ddmm_transfer_traceback.txt")
        self.modman = ModManagement()

        if os.path.exists(self.traceback_file):
            os.remove(self.traceback_file)

    def ddmm_detection(self):
        return os.path.exists(self.ddmm_gamedir)
    
    def ddmm_path_setup(self):
        '''
        This define sets the project directory in DDML to the one in DDMM.
        '''

        return self.ddmm_gamedir

    def ddmm_folder_not_compliant(self, project_dir, x):
        '''
        This define checks if the mod in the DDMM has not been setup already
        by DDML if transfer is started again.
        '''
        return os.path.exists(os.path.join(project_dir, x, "install"))

    def ddmm_folder_setup(self, project_dir, x):
        '''
        This define adjusts the folders in the DDMM directory to be Ren'Py
        Launcher compliant.
        '''

        main_path = os.path.join(project_dir, x, "install")
            
        self.modman.move_mod_folder(main_path, os.path.join(project_dir, x))
        shutil.rmtree(main_path)

    def ddmm_revert_folder_setup(self, project_dir, x):
        '''
        This define reverts changes made to the DDMM directory if a error has
        occured.
        '''

        main_path = os.path.join(project_dir, x)

        for y in os.listdir(main_path):
            if y != "install":
                if os.path.isdir(os.path.join(main_path, y)):
                    shutil.move(os.path.join(main_path, y), os.path.join(main_path, "install"))
                else:
                    shutil.copy2(os.path.join(main_path, y), os.path.join(main_path, "install"))
    
    def ddmm_traceback(self):
        '''
        This define makes a custom traceback file for the DDMM transfer tool.
        '''
        with open(self.traceback_file, "a") as t:
            t.write(sys.stdout + "\n\n")
