## TODO: Transforms and transitions for interactivity/intuitiveness

screen battle(battle, **kwargs):  
###inputs, BattleInstance object; outputs, victory or defeat
    $ _rollback = False
    # key "rollback" action [[]]     #uncomment once complete, keep as it is for testing purposes
    # key "rollforward" action [[]]    
    # textbutton "Exit Battle" xalign 1.0 action Return()

    ## Draw the actual battle screen
    use _battle_base_layer(battle)
    use _battle_state_execution(battle)

    ## Ready to Fight?
    if all(fighter.action for fighter in battle.actionlist):
        textbutton "Fight!" align (0.5, 0.5) action Function(battle.resolve_turn) at glow


screen _battle_base_layer(battle):
    frame:
        background Solid("#005c")
        foreground None # maybe use this for fog of war later
        xsize 1000
        ysize 400
        xalign 0.5
        yalign 0.1
        ypadding 0
        xpadding 0

        vbox:
            hbox:
                fixed:
                    xysize (495, 375)
                    add Solid("#0a03")
                    use _battle_ally_field(battle)
                null width 10
                fixed: 
                    xysize (495, 375)
                    add Solid("#0a03")
                    use _battle_enemy_field(battle)
            hbox:
                #Info boxes, NYI
                text "Info%" xsize 65
                fixed:
                    xsize 870
                    add Solid("#030")
                    hbox: #actionlist, implemented
                        for units in battle.actionlist:
                            if units.action:
                                add units.icon
                                null width 1
                text "Info%" xsize 65 #enemy info box, NYI

        window at top:  #displays the location of the battle at the top.  Actual location system is NYI
            background Solid("#000")
            yminimum 0
            ypadding 1
            yoffset -15
            xminimum 0
            xfill False
            vbox at truecenter:
                text "Location"
        window at top:
            background Solid("#001")
            yminimum 0
            ypadding 1
            yoffset 10
            xminimum 0
            xfill False
            vbox at truecenter:
                text "Turn " + str(battle.currentturn)




screen _battle_ally_field(battle):
    draggroup:
        for x in range(3):
            for y in range(3):
                drag:
                    draggable False
                    pos (0.9, .5)
                    xanchor 1.0
                    xoffset int(((x * 82) + 30)*-1)
                    yoffset int((y * 82) - 80)
                    dropped dropped_curry(battle.allylist)
                    drag_name (x, y)
                    add Solid("#111", xysize = (80,80))
        for val in battle.allylist:
            if val is not battle.state[1] and val.active:
                drag:
                    droppable False
                    pos (0.9, 0.5)
                    xanchor 1.0
                    xoffset int(((val.pos[0] * 82) + 30)*-1)
                    yoffset int((val.pos[1] * 82) - 80)
                    dragged unit_dragged
                    clicked clicked_curry(battle, val)
                    drag_name val
                    id val.name
                    add val.icon
                    
screen _battle_enemy_field(battle):
    draggroup:
        for x in range(3):
            for y in range(3):    
                drag:
                    draggable False
                    pos (0.1, .5)
                    xoffset int((x * 82) + 30)
                    yoffset int((y * 82) - 80)
                    drag_name (x,y)
                    add Solid("#111", xysize = (80,80))
        if battle.state[1] != "attack":
            for val in battle.enemylist:
                if val.active: #if enemy's alive
                    drag:
                        draggable False
                        droppable False
                        pos (0.1, 0.5)
                        xoffset int((val.pos[0] * 82) +30)
                        yoffset int((val.pos[1] * 82) - 80)
                        drag_name val.name
                        id val.name
                        add val.icon

screen _battle_state_execution(battle):
    #no additional layers is ("default", None)
    if battle.state[0] == "resolvingturn":
        ##Combatlog
        window id "combatlog":
            text battle.combatlog
        imagebutton idle "#0000" hover "#0000" action Function(battle.resolve_turn)

    elif battle.state[0] == "victory":
        ## Victory
        imagebutton idle "#0000" hover "#0000" action Return
        textbutton "Victory!" action Return at truecenter

    elif battle.state[0] == "defeat":
        ## Defeat
        imagebutton idle "#0000" hover "#0000" action Return
        textbutton "Defeat!" action Return at truecenter

    elif battle.state[0] == "initialclick":
        use _battle_draw_one_ally(battle)
        $clickedfighter = battle.state[1]
        frame:   #the action menu
            pos (0.5, 0.3)
            xanchor 1.0
            xoffset int(((clickedfighter.pos[0] * 82) - 85) *-1)
            yoffset int((clickedfighter.pos[1] * 82) - 47)
            vbox:
                #might use imagebuttons instead here.  still, concept is the same
                #TODO: different buttons based on the fighter
                textbutton "Attack!" action [With(dissolve), 
                                            SetField(battle, "state", ("attack", clickedfighter))]
                textbutton "Defend!" action [SetField(clickedfighter, "action", "defend"), 
                                            With(dissolve), 
                                            SetField(battle, "state", ("default", None))]  
                textbutton "GENUFLECT" action Jump("genuflect")

    elif battle.state[0] == "attack":
        use _battle_draw_one_ally(battle)
        use _battle_draw_all_enemies(battle)


screen _battle_draw_one_ally(battle):
    $clickedfighter = battle.state[1] #just so it's more readable
    imagebutton:
        idle "#0009" 
        hover "#0009" 
        action [With(dissolve), 
                SetField(battle, "state", ("default", None))] 
    #a "cancel" button if you will, so clicking off from the menu returns to normal
    add clickedfighter.icon:
        pos (0.5, 0.3)
        xanchor 1.0
        xoffset int(((clickedfighter.pos[0] * 82) + 85) *-1)
        yoffset int((clickedfighter.pos[1] * 82) - 77)

screen _battle_draw_all_enemies(battle, clickedaction = "attack"):
    for val in battle.enemylist:
        if val.active:
            drag:
                draggable False
                droppable False
                pos (0.5, 0.3)
                xoffset int((val.pos[0] * 82) + 85)
                yoffset int((val.pos[1] * 82) - 77)
                drag_name val
                id val.name
                clicked enemy_curry(battle, val, battle.state[1], clickedaction)
                add val.icon
