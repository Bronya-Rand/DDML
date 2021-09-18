
init python:
    from ddmm_compatibility import DDMM_Compatibility
    mm_compat = DDMM_Compatibility()

label transfer:

    python hide:

        failed_mods = 0

        interface.info(_("Ready to transfer your DDMM (Doki Doki Mod Manager) data to DDML?"),
        _("This transfer tool with help you setup your mods made in DDMM to work DDML."))

        mm_compat = ddmm_traceback_start()

        interface.info(_("First we will try to see where DDMM stores your mods in."),
        _("This will help detect what mods you have in DDMM for DDML to use."))

        interface.interaction( _("Finding DDMM Directory"), _("Finding your DDMM directory. Please wait..."))

        if not mm_compat.ddmm_detection():

            interface.error(_("The transfer tool was unable to find your DDMM directory."),
            _("If you believe this message was made in error, contact the developer on Github."))

        persistent.projects_directory = mm_compat.ddmm_path_setup()

        interface.info(_("Your DDMM directory was found successfully."), 
        _("Now the transfer tool will now detect and setup your mods to work with DDMM."),
        _("Make sure no mods or DDMM are running on your computer before proceeding."))

        for x in os.listdir(persistent.projects_directory):
            if mm_compat.ddmm_folder_not_compliant(persistent.projects_directory, x):
                interface.interaction(_("Setting Up Mods"), _("Setting up " + x + " for DDML. Please wait..."))
                try:
                    mm_compat.ddmm_folder_setup(persistent.projects_directory, x)
                except:
                    mm_compat.ddmm_traceback(x)
                    mm_compat.ddmm_revert_folder_setup(persistent.projects_directory, x)
                    failed_mods = 1
        
        if failed_mods != 0:
            interface.error(_("DDML encountered some errors with transferring some mods."),
            _("See {i}transfer_log.txt{/i} for more information. If the issue persists, contact the developer on Github."))
        else:
            interface.info(_("DDML transferred all your mods from DDMM with no issues."))

        mm_compat.ddmm_traceback_shutdown()
        project.manager.scan()

    jump preferences
