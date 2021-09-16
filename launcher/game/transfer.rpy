
init python:
    from ddmm_compatibility import DDMM_Compatibility
    
    mm_compat = DDMM_Compatibility()

label transfer:

    python hide:

        failed_mods = 0

        interface.info(_("Ready to transfer your DDMM (Doki Doki Mod Manager) data to DDML?"),
        _("This transfer tool with help you setup your mods made in DDMM to work DDML."))

        interface.info(_("First we will try to see where DDMM stores your mods in."),
        _("This will help detect what mods you have in DDMM for DDML to use."))

        if not mm_compat.ddmm_detection():

            interface.error(_("The transfer tool was unable to find your DDMM directory."),
            _("If you believe this message was made in error, contact the developer on Github."),
            label=preferences)
        
        persistent.projects_directory = mm_compat.ddmm_path_setup()

        interface.info(_("Your DDMM directory was found successfully."), 
        _("Now the transfer tool will now detect and setup your mods to work with DDMM."),
        _("Make sure no mods or DDMM are running on your computer before proceeding."))

        for x in os.listdir(persistent.projects_directory):
            if mm_compat.ddmm_folder_not_compliant():
                interface.interaction(_("Setting up " + x + " for DDML."))
                try:
                    mm_compat.ddmm_folder_setup(persistent.projects_directory)
                except:
                    mm_compat.ddmm_traceback()
                    mm_compat.ddmm_revert_folder_setup(persistent.projects_directory)
                    failed_mods = 1
        
        if failed_mods != 0:
            interface.info(_("DDML encountered some errors with transferring some mods."),
            _("See {i}ddmm_transfer_traceback.txt{/i} for more information."),
            _("If the issue persists, contact the developer on Github and provide this file when issuing the issue.")
        else:
            interface.information(_("DDML transferred all your mods from DDMM with no issues."))

    renpy.jump("preferences")
