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

        # Call sense_and_act
        self.sense_and_act()

        # Update behaviors weight with newly calculated value for match_degree
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        """Core computations performed by the behavior that uses sensob readings
        to produce motor recommendations (and halt requests)."""

        # Calculate new value for match_degree

        pass


class Behavior1(Behavior):
    """Class for behavior that makes sure the robot backs off if border is detected."""

    def __init__(self, ir_sensob, bbcon):
        self.ir_sensob = ir_sensob
        self.priority = 1
        super(Behavior1, self).__init__(bbcon, [ir_sensob])

    def consider_activation(self):
        # Should always be active to make sure that the robot does not drive
        # past the line
        return True

    def consider_deactivation(self):
        # Should never be deactivated
        return False

    def sense_and_act(self):
        # checks if the ir-sensor sensob har detected a line

        if self.ir_sensob.value is None:

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
            self.motor_recommendations = ['left', 0, +0, ]

            return
        else:

            # if a line is detected we should really try to avoid it, so match
            # degree is superhigh
            self.match_degree = 1  # is 1 to high, or ok?

            # find which side of the robot the line is detected
            start, end, = self.ir_sensob.value
            average = (start + end) / 2

            if average < 2:  # line is on left side
                # turn rigth
                degrees = random.randint(45, 100)
                self.motor_recommendations = ['right', degrees, +0.4, ]
            elif average > 4:  # line is on right side
                # turn left
                degrees = random.randint(45, 100)
                self.motor_recommendations = ['right', degrees, +0.4, ]
            else:   # line is straight in front
                # turn a lot
                degrees = random.randint(100, 200)
                self.motor_recommendations = ['right', degrees, +0.4, ]
            return


class Behavior5(Behavior):
    """Behavior that avoids objects that are not red."""
    red_camera_sensob: object

    def __init__(self, measure_distance_sensob, red_camera_sensob,
                 bbcon):  # hope we have a sensob that checks for red colors;))
        self.priority = 0.7
        self.measure_distance_sensob = measure_distance_sensob
        self.red_camera_sensob = red_camera_sensob
        super(Behavior1, self).__init__(
            bbcon, [
                measure_distance_sensob, red_camera_sensob])

    def consider_activation(self):
        # Should only be activated if it is closer than a certain distance
        # (here 5cm)
        if self.measure_distance_sensob.value < 5 and self.red_camera_sensob.value < 0.5:  # should we check for None?
            return True
        return False

    def consider_deactivation(self):
        # Should be deactivated if it is not close to an object (checks for
        # more than 5 cm) or wrong color
        if self.measure_distance_sensob.value >= 10 or self.red_camera_sensob.value >= 0.5:  # should we check for None?
            return True
        return False

    def sense_and_act(self):
        # A red object has probably been detected
        # too high? (Set it high since it is kinda important to avoid red)'
        self.match_degree = 0.9

        # turn left
        self.motor_recommendations = ['left', random.randint(45, 100), +0.4]


class Behavior6(Behavior):
    """Behavor that keeps track of total time and declares that a run has exceeded its time limit."""

    # do we have a time-sensob?/Can we make one?
    def __init__(self, time_sensob, bbcon, time_limit=float("inf")):
        self.time_sensob = time_sensob
        self.time_limit = time_limit
        super(Behavior1, self).__init__(bbcon, [time_sensob])

    def consider_activation(self):
        # Should be active if time limit has been exceeded
        if self.time_sensob.value >= self.time_limit:
            return True
        return False

    def consider_deactivation(self):
        # Should never be deactivated
        if self.time_sensob.value < self.time_limit:
            return True
        return False

    def sense_and_act(self):

        # Request robot to end the run
        self.halt_request = True

        # the motors doesn't really have to do anything. Remove?
        self.motor_recommendations = [
            (0, 0, 'L'), (0, 0, 'R')]  # I really don't know'
