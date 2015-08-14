init -1 python:
    class Fighter:
        """You are ze fightermans.
        'pos' is what grid the fighter is on, 'action' is what they will do this turn (attack, defend, etc).  
        Stats are self-explanatory."""
        def __init__(self, name, flag, attack = 20, defense = 20, organization = 20, speed = 20, pos = None, action = None): #called when class is initialized
            self.attack = attack
            self.defense = defense
            self.organization = organization
            self.speed = speed
            self.troop = self.organization * 25
            self.currenttroop = self.troop
            self.pos = pos
            self.action = action
            self.name = name
            self.active = True
            if flag == "ally":
                self.icon = Fixed(
                    DynamicDisplayable(self.unit_action_icon), 
                    DynamicDisplayable(self.unit_health_bar),
                    Text(text = str(name), ypos = 10), 
                    At(Text(text = str(self.currenttroop)), right),
                    xysize = (80,80))
            elif flag == "enemy":
                self.icon = Fixed(
                    Solid("#300"), 
                    DynamicDisplayable(self.unit_health_bar),
                    Text(text = str(name), ypos = 10), 
                    At(Text(text = str(self.currenttroop)), right),
                    xysize = (80,80))
        def unit_action_icon(self, st, at):
            if self.action is None:
                return Solid("#030"), None
            else:
                return Solid("#060"), None

        def unit_health_bar(self, st, at):
            return Bar(style = style.health_bar, 
                value = AnimatedValue(value = self.currenttroop, range = self.troop)), None


    class BattleInstance:
        """object to hold allylist, enemylist, and location, as well as anything else I guess."""
        def __init__(self, allylist, enemylist, location, turns = 5):
            self.allylist = allylist
            self.enemylist = enemylist
            self.location = location
            self.state = ("default", None)
            self.maxturns = 5
            self.currentturn = 1
            self.newturn = True
            self.actionlist = allylist + enemylist
            self.actionlist.sort(key=lambda unit: unit.speed, reverse = True)

        def __str__():
            "I dunno lol"
        def resolve_turn(self):
            # work through list of actions

            for unit in self.actionlist:
                if unit.action is "defend":
                    store.battleresult.append(unit.name + " defends.")
                elif unit.action[0] is "attack":
                    damage = int(unit.attack * unit.currenttroop / 50)
                    store.battleresult.append(unit.name + " deals " + str(damage) + " damage to " + unit.action[1].name + "!")
                    unit.action[1].currenttroop = unit.action[1].currenttroop - damage
                    if unit.action[1].currenttroop < 1:
                        store.battleresult.append(unit.action[1].name + " is dead.")

            # for unit in self.actionlist:
            #     if unit.active:    
            #         if unit.action is "defend":
            #             renpy.say(who = None, what = unit.name + " defends.")
            #         elif unit.action[0] is "attack":
            #             if unit.action[1].active:
            #                 damage = int(unit.attack * unit.currenttroop / 50)                   
            #                 renpy.say(who = None, what = unit.name + " deals " + str(damage) + " damage to " + unit.action[1].name + "!")
            #                 unit.action[1].currenttroop = unit.action[1].currenttroop - damage
            #                 if unit.action[1].currenttroop < 1:
            #                     renpy.say(who = None, what = unit.action[1].name + " is dead.")
            #                     unit.action[1].active = False
            #     unit.action = None


            # clean all actions, increment new turn
            for val in self.actionlist:
                val.action = None
                if val.currenttroop < 1:
                    val.active = False
            self.currentturn += 1
            self.newturn = True
            renpy.restart_interaction()
            return