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
        """To set a default current behavior"""
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
                highest = act_b.weight
        print()

        if correct_behavior is None:
            print("_____________________KODEN SKULLE KRASJET PGA NONE______________")
            correct_behavior = self.default

        print("correct_behavior:", correct_behavior)
        print("correct_behavior.motor_recommondations: {}".format(
            correct_behavior.motor_recommendations))
        tupple = (
            correct_behavior.motor_recommendations,
            correct_behavior.halt_request)
        return tupple
