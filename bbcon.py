"""BBCON control module"""
import time
import arbitrator
import behaviour
import motob
import sensob
import sys
sys.path.append('../')
import project6_supply.zumo_button


class Bbcon:
    """BBCON klass"""

    time_step = 0.4  # må velge varighet på time_step for robot
    behaviour_objects = []  # alle behaviour_objects som finnes
    sensobs_objects = []  # alle sensobs objekter som robot har
    active_behaviours = []  # behaviours som LAGER anbefalinger basert på input fra sensobs
    motobs_objects = []  ## alle motobs objecter som snakker med hjulene
    total_time = 0

    def __init__(self, motobs_objects):
        """Initierer en instans av BBCON"""
        self.arbitrator = arbitrator.Arbitrator(self)  # Arbitrator skal ta imot selve Bbcon()
        self.motobs_objects = motobs_objects  # alle motobs objecter som snakker med hjulene

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
        for sens in self.sensobs_objects:
            # oppdaterer alle sensobs
            sens.update()
            print("Sensob :" + str(sens) + "har blitt oppdatert")

        for behav in self.behaviour_objects:
            # oppdaterer alle behaviour, s.a. de kan lese fra sensobs of sette
            # seg selv som aktive eller ikke
            behav.update()
            print("Behaviour_object :" + str(behav) + "har blitt oppdatert")

        for behav in self.behaviour_objects:  # finner ut om behaviour er aktiv eller ikke
            if behav.active_flag:
                self.activate_behaviour(behav)
                print("Behaviour_object :" + str(behav) + "aktivert")
            else:
                if behav in self.active_behaviours:
                    self.deactivate_behaviour(behav)
                    print("Behaviour_object :" + str(behav) + "deaktivert")
        action = self.arbitrator.choose_action()  #kaller arbitrator for å velge en aksjon
        print("arbitrator valgte :" + str(action))

        for mot in self.motobs_objects:
            mot.update(action)  # motobs mottar anbefalingen fra Arbitrator
            print("motob :" + str(mot) + "update action")

        time.sleep(self.time_step)  # venter en time_step
        self.total_time += 1

        for sens in self.sensobs_objects:  # resetter alle senobs før neste time_step
            sens.reset()
            print("sensob :" + str(sens) + "resettes")


if __name__ == "__main__":
    print("*****Hello there, it's I, THE BBCON!!!*****")
    BBCON = Bbcon(motob.motob())  # skrive inn motobs
    BBCON.add_behaviour(behaviours.Behavior1(sensob.LineDetector(), BBCON))  # legg til alle behaviours
    BBCON.add_behaviour(behaviours.Behavior2(sensob.MeasureDistance(), BBCON))
    BBCON.add_behaviour(behaviours.Behavior3(sensob.MeasureDistance(), sensob.Cameraob(), sensob.LineDetector(), BBCON))
    BBCON.add_behaviour(behaviours.Behavior4(sensob.MeasureDistance(), sensob.Cameraob(), BBCON))
    BBCON.add_behaviour(behaviours.Behavior5(sensob.MeasureDistance(), sensob.Cameraob(), BBCON))
    BBCON.add_behaviour(behaviours.Behavior6(BBCON))
    #BBCON.add_sensor(sensob.Proximity())  # legg til alle senobs
    BBCON.add_sensor(sensob.LineDetector())  # legg til alle senobs
    BBCON.add_sensor(sensob.MeasureDistance())  # legg til alle senobs
    BBCON.add_sensor(sensob.Cameraob())  # legg til alle senobs
    TOTAL_STEPS = 0
    BUTTON_BUTTON = True
    zumo_button.ZumoButton().wait_for_press()
    while BUTTON_BUTTON:
        TOTAL_STEPS += 1
        print('this is a step number: ' + str(TOTAL_STEPS))
        BBCON.run_one_timestep()
