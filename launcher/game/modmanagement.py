
import os
import shutil

class ModManagement:
    '''
    This class manages what the user can do to a mod
    in the mod launcher.
    '''

    def __init__(self):
        self.failedMods = []

    def delete_mod(self, modFolder, modName):
        '''
        This define deletes a mod folder from the mod install folder 
        if confirmed by the user.
        '''

        shutil.rmtree(os.path.join(modFolder, modName))

    def move_mod_folder(self, modFolder, newModFolder):
        '''
        This define moves the contents of the old mod install folder
        to the new mod install folder.
        '''

        self.failedMods = []
        
        for x in os.listdir(modFolder):
            if os.path.isdir(os.path.join(modFolder, x)):
                try:
                    shutil.move(os.path.join(modFolder, x), os.path.join(newModFolder, x))
                except:
                    self.failedMods.append(x)

    def delete_rpa(self, modFolder, rpaName):
        '''
        This define deletes a RPA from the mod folder 
        if confirmed by the user.
        '''

        os.remove(os.path.join(modFolder, rpaName))