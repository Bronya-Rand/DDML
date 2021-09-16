
import shutil
import os
from launcher.game.modmanagement import ModManagement

class DDMM_Compatibility:
    '''
    This class adds DDMM (Mod Manager) compatibility features to DDML.
    '''

    def __init__(self) -> None:
        # The DDMM directory in Windows
        self.ddmm_gamedir = os.path.join(os.getenv("APPDATA"), 
                            "DokiDokiModManager/GameData/installs")
        self.modman = ModManagement()
    
    def ddmm_path_setup(self, project_dir):
        '''
        This define sets the project directory in DDML to the one in DDMM.
        '''

        project_dir = self.ddmm_gamedir

    def ddmm_folder_setup(self, project_dir):
        '''
        This define adjusts the folders in the DDMM directory to be Ren'Py
        Launcher compliant.
        '''

        for x in os.listdir(project_dir):
            main_path = os.path.join(project_dir, x, "install")
            
            self.modman.move_mod_folder(main_path, os.path.join(project_dir, x))
            shutil.rmtree(main_path)
