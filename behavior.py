"""Module for the behavior class."""


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
            self.active_flag = not self.consider_deactivation()  # Active status will be the opposite of the testanswer
        else:  # If behavior is inactive consider activation
            self.active_flag = self.consider_activation()  # Active status will equal testanswer

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
    """Class for behavior that makes sure the robot stops if border is detected."""

    def __init__(self, ir_sensob, bbcon):
        sensobs = [ir_sensob]
        super(Behavior1, self).__init__(bbcon, sensobs)

    def consider_activation(self):
        # Should always be active to make sure that the robot does not drive past the line
        return True

    def consider_deactivation(self):
        # Should never be deactivated
        return False

    def sense_and_act(self):
        pass
