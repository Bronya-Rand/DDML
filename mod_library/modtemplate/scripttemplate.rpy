#This is where you should name your Mod Script (e.g. "label MASScript:")
label scripttemplate:

#definitions for your mod should go here. Only add your mod definitions since definitions.rpyc already has the vanilla definitions
#
#end of definitions
#your script should go here

    $ anticheat = persistent.anticheat

    $ chapter = 0

    $ _dismiss_pause = config.developer
    
#this controls the names of the Doki's before the MC meets them
#to add a new character define them first in the definitions tab here (
#e.g. define ph = DynamicCharacter('ph_name', image='', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
#afterwards insert the name of the character here (e.g. $ ph_name = "Phil")
    $ s_name = "Sayori"
    $ m_name = "Monika"
    $ n_name = "Natsuki"
    $ y_name = "Yuri"

    $ quick_menu = True
    $ style.say_dialogue = style.normal

    $ allow_skipping = True
    $ config.allow_skipping = True
    
#this is where you call your scripts aka your story
if persistent.playthrough == 0:

    call MTDay1

elif persitent.playthrough == 1:

    return
