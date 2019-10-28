"""This file contains the arbitrator-class"""

import random


class Arbitrator:
    """An arbitrator-object will decide which
    behaviour wins at every timestep"""

    def __init__(self, bbcon):
        """Initializes the arbitrator-object,
        which must have a pointer to it's bbcon"""
        self.bbcon = bbcon

    def choose_action(self):
        """This method will decide which action should be activated, and return
        the tuple """
        active_behaviors = self.bbcon.active_behaviors
        print(active_behaviors)
        interval = []
        current_num = 0
        for behavior in active_behaviors:
            # Creates a list containing all the intervals for the behaviours
            current_num += behavior.weight
            interval.append(round(current_num, 2))
        print(interval)
        # Choose a random num in the full interval:
        random_number = random.uniform(0, interval[-1])
        print(random_number)
        correct_behavior = None
        for i in range(0, len(interval)):
            print("Nå er vi i for-løkken, runde: ", i)
            if random_number < interval[i]:
                print("Nå er vi i if-steningen")
                # Find correct behaviour and end the for-loop
                correct_behavior = active_behaviors[i]
                break
        tupple = (correct_behavior.motor_recommendations, correct_behavior.halt_request)
        return tupple
