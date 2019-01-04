#GOBFADU Policy 1.7 DDLC

#If you want to change the theme of the DDML Mod Selection Screen, just replace the current DDMLTheme Image with the image or your choosing. 
#Please make sure your image has either the name set to "DDMLTheme" or change the name of the png down below
image bg theme1 = "mod_assets/DDMLTheme.png"

#DO NOT MESS WITH THE LABEL!!! THIS IS IMPORTANT TO CALL ALL MOD SCRIPTS
label gobfadupolicygobfadu:
    stop music fadeout 2.0
    scene bg theme1
    with dissolve_scene_full
    menu:
        "Select a Mod to Launch"
        #Here you can change the Name of Mod Template to your Mod (e.g. Monika After Story)
        "Mod Template":
            #Here you should call your script (e.g. MASScript.rpy)
            call MTDay1
            return
        #"Tutorial":
            #menu:
                #"Which Doki do you want to get taught from?"

                #"Monika":
                    #call GOBFADU857Moni
                    #return
                #"Natsuki":
                    #call GOBFADU857Natsu
                    #return
                #"Sayori":
                    #call GOBFADU857Sayo
                    #return
                #"Yuri":
                    #call GOBFADU857Yuri
                    #return
    return
    