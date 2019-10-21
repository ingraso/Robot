"""BBCON control module"""
import time
import arbitrator
import motob
import sensob


class Bbcon:
    """BBCON klass"""

    time_step = 0  # må velge varighet på time_step for robot
    robot = 0

    def __init__(
            self,
            motobs_objects):
        """Initierer en instans av BBCON"""
        self.behaviour_objects = []  # alle behaviour_objects som finnes
        self.sensobs_objects = []  # alle sensobs objekter som robot har
        self.motobs_objects = motobs_objects  # alle motobs objecter som snakker med hjulene
        self.arbitrator = arbitrator.Arbitrator(self)  # Arbitrator skal ta imot selve Bbcon()
        self.active_behaviours = []  # behaviours som LAGER anbefalinger basert på input fra sensobs

    def add_behaviour(self, behaviour):
        """Funksjon for å legge ny behaviours til behaviour_objects list"""
        self.behaviour_objects.append(behaviour)

    def add_sensor(self, sensor):
        """Funksjonen for å legge ny behaviour til sensor_objects list"""
        self.sensobs_objects.append(sensor)

    def activate_behaviour(self, behaviour):
        """Funksjonen for å legge ny behaviour til active_behaviour list"""
        if behaviour in self.behaviour_objects:
            self.active_behaviours.append(behaviour)
        else:
            print("this behaviour is not in the list")

    def deactivate_behaviour(self, behaviour):
        """Funksjonen for å fjerne behaviour fra active_behaviour list """
        self.active_behaviours.remove(behaviour)

    def run_one_timestep(self):
        """Kjøre en runde med viss timestap"""
        for sensob in self.sensobs_objects:
            # oppdaterer alle sensobs
            sensob.update()
        for behaviour in self.behaviour_objects:
            # oppdaterer alle behaviour, s.a. de kan lese fra sensobs of sette
            # seg selv som aktive eller ikke
            behaviour.update()  ################### SPØRSMÅL, er dette nok for behaviours å få tak i sensob data?
        for behaviour in self.behaviour_objects:  # finner ut om behaviour er aktiv eller ikke
            if behaviour.active_flag:
                self.activate_behaviour(behaviour)
            else:
                if behaviour in self.active_behaviours:
                    self.deactivate_behaviour(behaviour)
        action = arbitrator.choose_action()  #################### kaller arbitrator for å velge en aksjon. Skal det være flere anbefalinger per time_step?
        for motob in self.motobs_objects:  #################### Usikker på dette
            motob.motob.update(action)  # motobs mottar anbefalingen fra Arbitrator
        time.sleep(self.time_step)  # venter en time_step
        for sensob in self.sensobs_objects:  # resetter alle senobs før neste time_step
            sensob.reset()


if __name__ == "__main__":
    print("Hello there!")
    BBCON = Bbcon()  # skrive inn motobs
    BBCON.add_behaviour("")  # legg til alle behaviours
    BBCON.add_sensor("")  # legg til alle senobs
    while True:
        BBCON.run_one_timestep()
