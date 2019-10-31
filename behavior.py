"""Module for the behavior class."""
import random


class Behavior:
    """Class for the behaviors themselves."""

    def __init__(self, bbcon, sensobs):
        # Pointer to the controller that uses this behavior.
        self.bbcon = bbcon

        # List of all sensobs that this behavior uses
        self.sensobs = sensobs

        # List of recommendations, one per motob, that this behavior provides
        # to the arbitrator
        self.motor_recommendations = []

        # Boolean variable indicating that the behavior is currently active or
        # inactive
        self.active_flag = False

        # Some behaviors can request the robot to completely halt activity and
        # thus end the run
        self.halt_request = False

        # Static, pre-defined value indicating the importance of this behavior.
        self.priority = 0

        # Real number in the range [0, 1] indicating the degree to which
        # current conditions warrant the performance of this behavior.
        # Match degrees are calculated by every active behavior.
        # Indicates a combination of the urgency and appropriateness of performing the given
        # behavior at the given time.
        self.match_degree = 0

        # The product of the priority and the match degree, which the
        # arbitrator uses as the basis for selecting the winning behavior for a
        # timestep.
        self.weight = self.priority * self.match_degree

    def consider_deactivation(self):
        """Test whether the behavior should deactivate whenever active."""
        return True

    def consider_activation(self):
        """Test wheter the behavior should activate whenever inactive."""
        return True

    def update(self):
        """Main interface between the bbcon and the behavior."""

        # Update activity status:
        if self.active_flag:  # If behavior is active, consider deactivation
            # Active status will be the opposite of the testanswer
            self.active_flag = not self.consider_deactivation()
        else:  # If behavior is inactive consider activation
            # Active status will equal testanswer
            self.active_flag = self.consider_activation()

        # ********Should sensobs be informed of the status change here?******
        
        if self.active_flag:
            # Call sense_and_act
            self.sense_and_act()

        # Update behaviors weight with newly calculated value for match_degree
        self.weight = self.priority * self.match_degree
        #print(self, "priority:", self.priority, " match_degree:", self.match_degree)
        #print(self, "weight:", self.weight)

    def sense_and_act(self):
        """Core computations performed by the behavior that uses sensob readings
        to produce motor recommendations (and halt requests)."""

        # Calculate new value for match_degree



class Behavior1(Behavior):
    """Class for behavior that makes sure the robot backs off if border is detected."""
    
    def __repr__(self):
        return "Behavior1"

    def __init__(self, ir_sensob, bbcon):
        self.ir_sensob = ir_sensob
        
        super(Behavior1, self).__init__(bbcon, [ir_sensob])
        self.priority = 1

    def consider_activation(self):
        # Should always be active to make sure that the robot does not drive
        # past the line
        return True

    def consider_deactivation(self):
        # Should never be deactivated
        return False

    def sense_and_act(self):
        # checks if the ir-sensor sensob har detected a line
        # print("get_value til ir sensob er", self.ir_sensob.get_value())
        # print("summen er", sum(self.ir_sensob.get_value()))
        # print("lengden er:", len(self.ir_sensob.get_value()))
        if sum(self.ir_sensob.get_value()) / len(self.ir_sensob.get_value()) > 0.4:
            print("B1's average of line:", sum(self.ir_sensob.get_value()) / len(self.ir_sensob.get_value()))
            # if a line is detected we should really try to avoid it, so match
            # degree is superhigh
            self.match_degree = 1  # is 1 to high, or ok?

            # find which side of the robot the line is detected

            degrees = 100
            product_values = []

            for value_index in range(len(self.ir_sensob.get_value())):
                product_values.append(self.ir_sensob.get_value()[value_index] * (value_index + 1))
            
            print("(behavior1) sensorlist:", self.ir_sensob.get_value(), "product_values:", product_values)
            average = 0
            if sum(self.ir_sensob.get_value())>0.9:
                average = 3
            else:
                average = sum(product_values) / sum(self.ir_sensob.get_value()) - 1

            if average < 2:  # line is on left side
                # turn rigth
                print("(behavior1) line on left side")
                #degrees = random.randint(45, 100)
                degrees = 110
                self.motor_recommendations = ['r', degrees, +0.5]
            elif average > 4:  # line is on right side
                # turn left
                degrees = 110
                print("(behavior1) line on right side")
                #degrees = random.randint(45, 100)
                self.motor_recommendations = ['l', degrees, +0.5]
            else:  # line is straight in front
                # turn a lot
                print("(behavior1) line in front")
                #degrees = random.randint(100, 200)
                degrees = 150
                self.motor_recommendations = ['r', degrees, +0.5]
            return
            
            
            

        # match degree is low since no line is detected
        # ok to set to 0? Then this will never be chosen, and we don't have
        # to set motors:)
        self.match_degree = 0

        # if no line is detected the robot should just keep going
        # therefore the motor recommondation will be to go straight

        # Guessing that first element in list is for left wheel, second element is for right.
        # Can be changed later
        # dont' think this is the right way to recommend, but we will fix
        # (I hope;))
        self.motor_recommendations = ['l', 0, +0, ]

        return


        


class Behavior2(Behavior):
    """Class for behavior that drive around searching for objects"""
    
    def __repr__(self):
        return "Behavior2"

    def __init__(self, measure_distance, bbcon):
        """Initializes behaviour2"""
        self.sensobs = [measure_distance]
        super().__init__(bbcon, self.sensobs)
        self.priority = 0.3  # This behaviour isn't very important.
        self.motor_recommendations.append("f")  # Which direction the robot should turn
        self.motor_recommendations.append(0)  # How many degrees the robot should turn
        self.motor_recommendations.append(0.2)  # The speed (if max-speed is 1)

    def consider_deactivation(self):
        """Method that checks if we should deactivate the behavior. This behaviour
        should always be active. """
        return False

    def consider_activation(self):
        """Method that checks if the behavior should be activated.
        Should always be activated"""
        return True

    def sense_and_act(self):
        """will update the match_degree. The motor_recommendations
        are always the same for this behavior"""
        if self.sensobs[0].get_value() > 10:
            self.match_degree = 0.6
        else:
            self.match_degree = 0
        """for sensob in self.sensobs:
            # The ultrasound-sensobs value represents the distance in cm (float)
            if sensob.get_value() > 10:
                # Before we find the object, the match_degree should be high
                self.match_degree = 0.6
            else:
                # If we are closer than 10 cm we should use the camera
                self.match_degree = """


class Behavior3(Behavior):
    """This behavior will check if the object is pushed outside of the tape"""
    
    def __repr__(self):
        return "Behavior3"

    def __init__(self, measure_distance, camera_ob, line_detector, bbcon):
        """This object should keep track of the line, distance to object,
        and the color of the object"""
        self.sensobs = [measure_distance, camera_ob, line_detector]
        self.bbcon = bbcon
        super().__init__(bbcon, self.sensobs)
        # This object should have high priority, because we have to stop:
        self.priority = 1

    def consider_activation(self):
        """We should activate the behavior if the object is pushed out of line"""
        # and self.sensobs[1].get_value() >= 0.5 \
        if self.sensobs[0].get_value() < 5 and (sum(self.sensobs[2].get_value()) / len(self.sensobs[2].get_value()) <= 0.4):
            print("Gjennomsnitt ala Karro:", sum(self.sensobs[2].get_value()) / len(self.sensobs[2].get_value()))

            return True
        return False

    def consider_deactivation(self):
        """Should usually be deactivated"""
         # and self.sensobs[1].get_value() >= 0.5 \
        if self.sensobs[0].get_value() >= 5 or (sum(self.sensobs[2].get_value()) / len(self.sensobs[2].get_value()) > 0.4):
            # Switched for and to or
            print("Gjennomsnitt ala Karro:", sum(self.sensobs[2].get_value()) / len(self.sensobs[2].get_value()))

            return True
        return False

    def sense_and_act(self):
        self.sensobs[1].update()
        if self.sensobs[1].value >= 0.5:
            self.match_degree = 1
            self.halt_request = True
            self.motor_recommendations = ['l', 0, 0]
        else:
            self.match_degree = 0
            self.motor_recommendations = ['l', 60, 0.2]
"""
class Behavior4(Behavior):

    def __init__(self, measure_distance, camera_ob, bbcon):
        
        self.sensobs = [measure_distance, camera_ob]
        self.bbcon = bbcon
        super().__init__(bbcon, self.sensobs)
        self.priority = 0.7  # This behaviour is sort of important
        self.motor_recommendations.append("f")  # Which direction the robot should turn
        self.motor_recommendations.append(0)  # How many degrees the robot should turn
        self.motor_recommendations.append(0.4)  # The speed (if max-speed is 1)

    def consider_activation(self):
        if self.sensobs[0].get_value() <= 10 and self.sensobs[1].get_value() >= 0.5:
            return True
        return False

    def consider_deactivation(self):
        if self.sensobs[0].get_value() > 10 or self.sensobs[1].get_value() < 0.5:
            return True
        return False

    def sense_and_act(self):
        self.match_degree = 0.9
        self.motor_recommendations = ['l', 0, 0.2]
        # We can't come here unless the requirements are met, so this
        # should work.


class Behavior5(Behavior):
    # red_camera_sensob = object

    def __init__(self, measure_distance_sensob, red_camera_sensob,
                 bbcon):  # hope we have a sensob that checks for red colors;))
        self.priority = 0.7
        self.measure_distance_sensob = measure_distance_sensob
        self.red_camera_sensob = red_camera_sensob
        super(Behavior5, self).__init__(bbcon, [measure_distance_sensob, red_camera_sensob])

    def consider_activation(self):
        # Should only be activated if it is closer than a certain distance
        # (here 5cm)
        if self.measure_distance_sensob.get_value() <= 10 and \
                self.red_camera_sensob.get_value() < 0.5:  # should we check for None?
            return True
        return False

    def consider_deactivation(self):
        # Should be deactivated if it is not close to an object (checks for
        # more than 5 cm) or wrong color
        print("self.measure_distance_sensob.get_value():", self.measure_distance_sensob.get_value())
        if self.measure_distance_sensob.get_value() >= 10 or \
                self.red_camera_sensob.get_value() >= 0.5:  # should we check for None?
            return True
        return False

    def sense_and_act(self):
        # A red object has probably been detected
        # too high? (Set it high since it is kinda important to avoid red)'
        self.match_degree = 0.9

        # turn left
        self.motor_recommendations = ['l', random.randint(45, 100), +0.2]
"""

class Behavior5(Behavior):
    """Behavior that avoids objects that are not red."""
    # red_camera_sensob = object
    
    def __repr__(self):
        return "Behavior5"

    def __init__(self, measure_distance_sensob, red_camera_sensob,
                 bbcon):  # hope we have a sensob that checks for red colors;))
        
        self.measure_distance_sensob = measure_distance_sensob
        self.red_camera_sensob = red_camera_sensob
        super(Behavior5, self).__init__(bbcon, [measure_distance_sensob, red_camera_sensob])
        self.priority = 0.7

    def consider_activation(self):
        # Should only be activated if it is closer than a certain distance
        # (here 5cm)
        print("In consider_activation -> distance:", self.measure_distance_sensob.get_value()) 
        if self.measure_distance_sensob.get_value() <= 10: #and \
                #self.red_camera_sensob.get_value() < 0.5:  # should we check for None?
            return True
        return False

    def consider_deactivation(self):
        # Should be deactivated if it is not close to an object (checks for
        # more than 5 cm) or wrong color
        print("In consider_deactivation -> distance:", self.measure_distance_sensob.get_value())
        if self.measure_distance_sensob.get_value() > 10: #or \
                #self.red_camera_sensob.get_value() >= 0.5:  # should we check for None?
            return True
        return False

    def sense_and_act(self):
        # A red object has probably been detected
        # too high? (Set it high since it is kinda important to avoid red)'
        print("(behavior5) return form update of camera sendob:", self.sensobs[1].update())
        print("If we come here a pic should be taken")
        self.match_degree = 0.9
        if self.red_camera_sensob.get_value() >= 0.5:
            # keep going
            print("self.motor_recommendations = ", ['f', 0, +0.4])
            self.motor_recommendations = ['f', 0, +0.4]
        else:
            # turn left
            number_degrees = random.randint(45, 90)
            print("self.motor_recommendations = ", ['l', number_degrees, +0.4])
            self.motor_recommendations = ['l', number_degrees, +0.4]

        # turn left
        #self.motor_recommendations = ['l', random.randint(45, 100), +0.4]



class Behavior6(Behavior):
    """Behavor that keeps track of total time and declares that a
    run has exceeded its time limit."""
    
    def __repr__(self):
        return "Behavior6"

    # do we have a time-sensob?/Can we make one?
    def __init__(self, bbcon, time_limit=120):
        self.time_limit = time_limit
        super(Behavior6, self).__init__(bbcon, [])
        self.priority = 1
        self.match_degree = 1

    def consider_activation(self):
        # Should be active if time limit has been exceeded
        if self.bbcon.total_time >= self.time_limit:
            return True
        return False

    def consider_deactivation(self):
        # Should never be deactivated
        if self.bbcon.total_time < self.time_limit:
            return True
        return False

    def sense_and_act(self):

        # Request robot to end the run
        self.halt_request = True

        # the motors doesn't really have to do anything. Remove?
        self.motor_recommendations = ['l', 0, 0]  # I really don't know'
