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
        active_behaviours = self.bbcon.active_behaviours
        print(active_behaviours)
        interval = []
        current_num = 0
        for behaviour in active_behaviours:
            # Creates a list containing all the intervals for the behaviours
            current_num += behaviour.weight
            interval.append(round(current_num, 2))
        print(interval)
        # Choose a random num in the full interval:
        random_number = random.uniform(0, interval[-1])
        print(random_number)
        for i in range(0, len(interval)):
            if random_number < interval[i]:
                # Find correct behaviour and end the for-loop
                correct_behaviour = active_behaviours[i]
                break
        tupple = (correct_behaviour.motor_recommendations, correct_behaviour.halt_request)
        return tupple
