"""Motob class"""
# import sys
# sys.path.append('../')
# from project6_supply.motors import Motors
# from project6_supply.zumo_button import ZumoButton
import Motors



class motob:
    """Motob klasse har en motor"""

    def __init__(self):
        """Create empty list as value"""
        self.motor = Motors()
        # ("l",45,+0.5)
        self.value = ["l", 0, 0]
        #self.dir_list = ['l','r','f','b']

    def update(self, mot_roc):
        """sette en ny value"""
        self.value = mot_roc

    def operationalize(self, dur=3):
        """apply value, r: Right, l:Left, f:Forward, b:Backward"""
        #dur = 3
        turn_speed = abs(self.value[2]) + 0.2
        cond_left_right = False
        if self.value[1] == 0:
            cond_left_right = True
        #print("I am in loop")
        if self.value[0] == 'l' and self.value[1] > 0:
            #cond_left_right = True
            self.motor.set_value((self.value[2], -self.value[2]), turn_speed)
        elif self.value[0] == 'r' and self.value[1] > 0:
            #cond_left_right = True
            self.motor.set_value((-self.value[2], self.value[2]), turn_speed)
        elif self.value[0] == 'f' and self.value[1] == 0:
            self.motor.forward(abs(self.value[2]), dur)
        elif self.value[0] == 'b' and self.value[1] == 0:
            self.motor.backward(abs(self.value[2]), dur)
        if cond_left_right:
            if self.value[2] > 0:
                self.motor.forward(abs(self.value[2]), dur)
            elif self.value[2] < 0:
                self.motor.backward(abs(self.value[2]), dur)
