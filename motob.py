"""Motob class"""
# import sys
# sys.path.append('../')
# from project6_supply.motors import Motors
# from project6_supply.zumo_button import ZumoButton
from motors import Motors



class motob:
    """Motob klasse har en motor"""

    def __init__(self):
        """Create empty list as value"""
        self.motor = Motors()
        # ("l",45,+0.5)
        self.value_drive = ["l", 0, 0]  # a list [direction, degrees, speed]
        self.value_halt = False  # The value of the halt flag
        #self.dir_list = ['l','r','f','b']

    def update(self, mot_roc):
        """sette en ny value"""
        self.value_drive = mot_roc[0]
        self.value_halt = mot_roc[1]

    def operationalize(self, dur=3):
        """apply value, r: Right, l:Left, f:Forward, b:Backward"""
        #dur = 3
        turn_speed = abs(self.value_drive[2]) + 0.2
        # cond_left_right = False
        # if self.value_drive[1] == 0:
            # If we are turning 0 degrees, cond_left_right = True
            # cond_left_right = True
        #print("I am in loop")
        if self.value_drive[0] == 'l' and self.value_drive[1] > 0 and not self.value_halt:
            # turn left and we are turning, but why not call left?
            # self.motor.set_value((self.value_drive[2], -self.value_drive[2]), turn_speed)#10 eller dur
            self.motor.left(self.value_drive[2], dur)
        elif self.value_drive[0] == 'r' and self.value_drive[1] > 0 and not self.value_halt:
            # turn right, and we are turning, try motors.right??
            # self.motor.set_value((-self.value_drive[2], self.value_drive[2]), turn_speed)#10 eller dur
            self.motor.right(self.value_drive[2], dur)
        elif self.value_drive[0] == 'f' and self.value_drive[1] == 0 and not self.value_halt:
            # Drive forward
            self.motor.forward(abs(self.value_drive[2]), dur)
        elif self.value_drive[0] == 'b' and self.value[1] == 0 and not self.value_halt:
            # Drive backwards
            self.motor.backward(abs(self.value_drive[2]), dur)
        elif self.value_halt:
            # If we are done, the haltflag is True, stop
            self.motors.stop()
        """if cond_left_right:
            # If we are not turning
            if self.value_drive[2] > 0:
                # If the speed is positive, drive forward
                self.motor.forward(abs(self.value_drive[2]), dur)
            elif self.value_drive[2] < 0:
                # If the speed is negative, drive backwards
                self.motor.backward(abs(self.value_drive[2]), dur)"""
