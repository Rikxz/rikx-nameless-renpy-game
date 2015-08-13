# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"
#image eileen happy = "eileen_happy.png"


# Declare characters used by this game.

# The game starts here.

label start:
    image muhbackground = Solid("#555")
    scene muhbackground
    call screen battle(defaultbattle)
    return


label genuflect:
    image genuflectend = Solid("#911")
    scene genuflectend
    "And I died."
    "Game Over"
    return