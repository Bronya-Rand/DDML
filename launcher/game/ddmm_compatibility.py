
import shutil
import os
from modmanagement import ModManagement
import sys
import logging
from renpy import config

class DDMM_Compatibility:
    '''
    This class adds DDMM (Mod Manager) compatibility features to DDML.
    '''

    def __init__(self):
        # The DDMM directory in Windows
        if sys.platform == "windows":
            self.ddmm_gamedir = os.path.join(os.getenv("APPDATA"), 
                                "DokiDokiModManager/GameData/installs")
        else:
            self.ddmm_gamedir = None
        self.modman = ModManagement()
        self.log_file = os.path.join(config.basedir, "transfer_log.txt")

        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def ddmm_detection(self):
        '''
        This define returns True if the DDMM directory in %APPDATA% is present.
        '''
        logging.debug("Locating DDMM directory in %APPDATA%.")

        if sys.platform != "windows":
            logging.exception("OS is not Windows! Exiting execution.")
            return False

        return os.path.exists(self.ddmm_gamedir)
    
    def ddmm_path_setup(self):
        '''
        This define sets the project directory in DDML to the one in DDMM.
        '''

        logging.debug("Located DDMM directory. Setting it to persistent.projects_directory.")

        return self.ddmm_gamedir

    def ddmm_folder_not_compliant(self, project_dir, x):
        '''
        This define checks if the mod in the DDMM has not been setup already
        by DDML if transfer is started again.
        '''
        logging.debug("Checking if " + x + " is DDML compliant.")

        return os.path.exists(os.path.join(project_dir, x, "install"))

    def ddmm_folder_setup(self, project_dir, x):
        '''
        This define adjusts the folders in the DDMM directory to be Ren'Py
        Launcher compliant.
        '''

        logging.debug("Making " + x + " DDML Compliant.")

        main_path = os.path.join(project_dir, x, "install")
            
        self.modman.move_mod_folder(main_path, os.path.join(project_dir, x))
        shutil.rmtree(main_path)

        logging.debug(x + " is now DDML Compliant.")

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

        logging.debug("Reverted changes made to " + x + ".")
    
    def ddmm_traceback(self, x):
        '''
        This define makes a custom traceback file for the DDMM transfer tool.
        '''

        logging.exception("Error occured when transferring " + x + ".")
    
    def ddmm_traceback_start(self):
        '''
        This define starts the transfer traceback when the transfer tool is
        running.
        '''

        logging.basicConfig(filename=self.log_file, level=logging.DEBUG)

    def ddmm_traceback_shutdown(self):
        '''
        This define stops the transfer traceback when the transfer tool is not
        running.
        '''
        logging.debug("Stopped logging for this session.")

        logging.shutdown()
