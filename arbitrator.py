"""This file contains the arbitrator-class"""

import random


class Arbitrator:
    """An arbitrator-object will decide which
    behaviour wins at every timestep"""

    def __init__(self, bbcon):
        """Initializes the arbitrator-object,
        which must have a pointer to it's bbcon"""
        self.bbcon = bbcon
        self.default = None
    
    def set_default_current_behavior(self, default):
        self.default = default

    def choose_action(self):
        """This method will decide which action should be activated, and return
        the tuple """
        active_behaviors = self.bbcon.active_behaviors
        print(active_behaviors)
        
        # finner behavior med høyest weight
        highest = 0
        correct_behavior = None
        print("Weights for active behaviors:", end="")
        for act_b in active_behaviors:
            print(str(act_b.weight), end=", ")
            if act_b.weight > highest:
                correct_behavior = act_b
        print()
        
        if correct_behavior == None:
            print("_____________________KODEN SKULLE KRASJET PGA NONE______________")
            correct_behavior = self.default
        
        """
        interval = []
        current_num = 0
        for behavior in active_behaviors:
            # print("the weight of this behavior is:", behavior.weight)
            # Creates a list containing all the intervals for the behaviours
            current_num += behavior.weight
            interval.append(round(current_num, 2))
        print("intervallet er:", interval)
        # Choose a random num in the full interval:
        random_number = random.uniform(0, interval[-1])
        print("Random number er:", random_number)
        correct_behavior = self.default
        for i in range(0, len(interval)):
            # print("Nå er vi i for-løkken, runde: ", i)
            if random_number < interval[i]:
                print("Nå er vi i if-setningen")
                # Find correct behaviour and end the for-loop
                correct_behavior = active_behaviors[i]
                break
            else:
                print("(arbitrator)Kom ikke in i if (arbitrator)")
        # print("Nå er motor_recomendation", correct_behavior.motor_recommendations)
        # print("Nå er halt_request", correct_behavior.halt_request)
        """
        
        print("correct behavior: {}".format(correct_behavior.motor_recommendations))
        tupple = (correct_behavior.motor_recommendations, correct_behavior.halt_request)
        return tupple
