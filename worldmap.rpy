screen worldmap:  #prototype worldmap screen for later on.
    side "c b":

        area (100, 100, 600, 400)

        viewport id "vp":
            draggable True
            imagemap:

                ground "images/bigpic.png"
                idle "images/bigpic_idle.png"
                hover "images/bigpic_hover.png"
                hotspot (57, 35, 194, 174) action Return()

        textbutton "Exit Map" action Return()