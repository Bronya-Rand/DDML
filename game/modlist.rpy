
label ADU:
    default persistent.ddmlfirstboot = False
    default persistent.playernametwo = False
    stop music fadeout 2.0
    scene black
    with dissolve_scene_full

    if not persistent.special_poems:
        python hide:
            persistent.special_poems = [0,0,0]
            a = range(1,12)
            for i in range(3):
                b = renpy.random.choice(a)
                persistent.special_poems[i] = b
                a.remove(b)

    if persistent.playernametwo == True and persistent.ddmlfirstboot == False:
        $ persistent.playernametwo == False

    if not persistent.playernametwo:
        python:
            player = renpy.input("Enter a Name", default='', allow="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", length=12)
            player = player.strip()
            persistent.playername = player

        $ persistent.playernametwo = True

    if not persistent.ddmlfirstboot:
        "Doki Doki Mod Launcher and this Modification of DDLC is a DDLC Mod that is unaffiliated with Team Salvato."
        "It is designed to be played or used once you have played the original DDLC."
        "Game Files for Doki Doki Literature Club can be obtained on Steam or ddlc.moe"
        menu:
            "By Agreeing to the IP Guidelines, you agree that you have played DDLC and accept and spoilers within."
            "I Agree.":
                    pass

        $ persistent.ddmlfirstboot = True
        
    menu:
        "Select a DDML Mode."
        "DDLC Mode":            

            if persistent.playthrough != 0:
                "Warning: You have a existing playthrough of DDLC or a Mod in progress. Selecting this mode may override your current playthrough."
                "This will not affect your saves."
                menu:
                    "Do you wish to continue into this mode?"
                    "Yes.":
                        $ persistent.playthrough = 0
                        jump ddlc
                        return
                    "No.":
                        "Returning to the Main Menu..."
                        $ renpy.full_restart(transition=None, label="splashscreen")

            jump ddlc
            return

        "Mod Mode":

            if persistent.playthrough != 0:
                "Warning: You have a existing playthrough of DDLC or a Mod in progress. Selecting this mode may override your current playthrough."
                "This will not affect your saves."
                menu:
                    "Do you wish to continue into this mode?"
                    "Yes.":
                        $ persistent.playthrough = 0
                        jump start
                        return
                    "No.":
                        "Returning to the Main Menu..."
                        $ renpy.full_restart(transition=None, label="splashscreen")

            jump start
            return
        
        "Change Player Name":
            $ playernametwo = True
            python:
                player = renpy.input("Enter a Name", default='', allow="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", length=12)
                player = player.strip()
                persistent.playername = player

            "Changed Player Name to [player]."

