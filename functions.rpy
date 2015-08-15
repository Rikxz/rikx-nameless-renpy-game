init python:

    def unit_clicked(battle, fighter):
        battle.state = ("initialclick", fighter)
        renpy.transition(dissolve)
        renpy.restart_interaction()
        return

    def unit_dragged(drags, drop):
        ## This function will snap the drag on top of the drop if the middle is over the drop
        if drop:
            dragvarx = int(drags[0].w/2 + drags[0].x)  #finding the midpoint of the drag, horizontally    
            dragvary = int(drags[0].h/2 + drags[0].y)  #finding the midpoint of the drag, vertically
            dropbox = (drop.x, drop.y, int(drop.x + drop.w), int(drop.y + drop.h))  #making our box, top left corner and bottom right corner
            if dropbox[0] < dragvarx < dropbox[2] and dropbox[1] < dragvary < dropbox[3]:  #if the midpoint of the drag is within the rectangle...
                drags[0].snap(drop.x,drop.y)       #move the drag on top of the drop
        return

    def unit_dropped(fighterlist, drop, drags):
        drags[0].drag_name.pos = drop.drag_name  #the drag's drag_name is the UID of the fighter associated with the drag
        renpy.restart_interaction()
        return

    def enemy_clicked(battle, enemy, fighter, clickaction):
        battle.state = ("default", None)
        fighter.action = [clickaction, enemy]
        #fighter.update_icon
        renpy.transition(dissolve)
        renpy.restart_interaction()
        return