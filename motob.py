import sys
sys.path.append('../')
from project6_supply.motors import Motors

class motob:
    def __init__(self, recommendations):
        self.motors = [] #liste av motors
        self.value = recommendations#("l",45,+0.5) #l er left, 45 er hvor mange grader, + er fremover og 0.5 er halvparten av max fart
        self.dir_list = ['l','r','f','b']

    def update(self, mot_roc):
        self.value = mot_roc

    def operationalize(self):
        for motor in self.motors:
            if self.value[0] == 'l':
                motor.set_value((self.value[2],-self.value[2]))
            elif self.value[0] == 'r':
                motor.set_value((-self.value[2], self.value[2]))


if __name__ == "__main__":
    print("Hei hei")
    m = Motors()
    m.forward(0.25, dur=10)
