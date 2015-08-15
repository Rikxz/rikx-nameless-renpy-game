init python:
    config.screen_width = 1280  
    config.screen_height = 720

    ally1 = Fighter(pos = (0,1), name = "ally1", flag = "ally", speed = 21) # position should be set by deployment screen normally
    ally2 = Fighter(pos = (1,2), name = "ally2", flag = "ally", speed = 22)
    ally3 = Fighter(pos = (2,0), name = "ally3", flag = "ally", speed = 19)
    enemy1 = Fighter(pos = (0,0), name = "enmy1", flag = "enemy", speed = 15) #enemy AI will set positions and actions eventually (NYI)
    enemy2 = Fighter(pos = (1,1), name = "enmy2", flag = "enemy", speed = 20)
    enemy3 = Fighter(pos = (2,2), name = "enmy3", flag = "enemy", speed = 18)

    dropped_curry = renpy.curry(unit_dropped)  #the curried dropped function.  Also sounds funny.
    clicked_curry = renpy.curry(unit_clicked)  #the curried clicked function.
    enemy_curry = renpy.curry(enemy_clicked) #giant enemy curry.  strike its weak point for massive damage.

    defaultallylist = [ally1, ally2, ally3] #allylist should be set by deployment screen as well
    defaultenemylist = [enemy1, enemy2, enemy3] #enemylist should either be a function of location or the enemy AI, not sure yet

    defaultbattle = BattleInstance(allylist = defaultallylist, enemylist = defaultenemylist, location = "location")