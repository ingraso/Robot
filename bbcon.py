"""BBCON control module"""
import time
import arbitrator
import behavior
import motob
import sensob
import zumo_button
#import sys
#sys.path.append('../')
#import project6_supply.zumo_button


class Bbcon:
    """BBCON klass"""

    def __init__(self, motobs_objects):
        """Initierer en instans av BBCON"""
        self.time_step = 0.4  # må velge varighet på time_step for robot
        self.behavior_objects = []  # alle behaviour_objects som finnes
        self.sensobs_objects = []  # alle sensobs objekter som robot har
        self.active_behaviors = []  # behaviours som LAGER anbefalinger basert på input fra sensobs
        self.total_time = 0
        self.motobs_objects = []  # alle motobs objecter som snakker med hjulene
        self.arbitrator = arbitrator.Arbitrator(self)  # Arbitrator skal ta imot selve Bbcon()
        self.motobs_objects.append(motobs_objects)  # alle motobs objecter som snakker med hjulene

    def add_behavior(self, behavior):
        """Funksjon for å legge ny behaviours til behaviour_objects list"""
        self.behavior_objects.append(behavior)

    def add_sensor(self, sensor):
        """Funksjonen for å legge ny behaviour til sensor_objects list"""
        self.sensobs_objects.append(sensor)

    def activate_behavior(self, behavior):
        """Funksjonen for å legge ny behaviour til active_behaviour list"""
        if behavior in self.behavior_objects:
            self.active_behaviors.append(behavior)
        else:
            print("this behaviour is not in the list")

    def deactivate_behavior(self, behavior):
        """Funksjonen for å fjerne behaviour fra active_behaviour list """
        self.active_behaviors.remove(behavior)

    def run_one_timestep(self):
        """Kjøre en runde med viss timestap"""
        for sens in self.sensobs_objects:
            # oppdaterer alle sensobs
            sens.update()
            # print("Sensob :" + str(sens) + "har blitt oppdatert")

        for behav in self.behavior_objects:
            # oppdaterer alle behaviour, s.a. de kan lese fra sensobs of sette
            # seg selv som aktive eller ikke
            behav.update()
            # print("Behavior_object :" + str(behav) + "har blitt oppdatert")

        for behav in self.behavior_objects:  # finner ut om behaviour er aktiv eller ikke
            if behav.active_flag:
                self.activate_behavior(behav)
                # print("Behavior_object :" + str(behav) + "aktivert")
            else:
                if behav in self.active_behaviors:
                    self.deactivate_behavior(behav)
                    # print("Behavior_object :" + str(behav) + "deaktivert")
        action = self.arbitrator.choose_action()  # kaller arbitrator for å velge en aksjon
        print("arbitrator valgte :" + str(action))

        for mot in self.motobs_objects:
            mot.update(action)  # motobs mottar anbefalingen fra Arbitrator
            mot.operationalize()  # roboten bør kjøre
            # print("motob :" + str(mot) + "update action")

        time.sleep(self.time_step)  # venter en time_step
        self.total_time += 1

        for sens in self.sensobs_objects:  # resetter alle senobs før neste time_step
            sens.reset()
            # print("sensob :" + str(sens) + "resettes")




def main():
		print("*****Hello there, it's I, THE BBCON!!!*****")
		BBCON = Bbcon(motob.motob())  # skrive inn motobs
		BBCON.add_sensor(sensob.LineDetector())  # legg til alle senobs
		BBCON.add_sensor(sensob.MeasureDistance())  # legg til alle senobs
		BBCON.add_sensor(sensob.Cameraob())  # legg til alle senobs
		BBCON.add_behavior(behavior.Behavior1(BBCON.sensobs_objects[0], BBCON))  # legg til alle behaviours
		BBCON.add_behavior(behavior.Behavior2(BBCON.sensobs_objects[1], BBCON))
		BBCON.add_behavior(behavior.Behavior3(BBCON.sensobs_objects[1], BBCON.sensobs_objects[2], BBCON.sensobs_objects[0], BBCON))
		BBCON.add_behavior(behavior.Behavior4(BBCON.sensobs_objects[1], BBCON.sensobs_objects[2], BBCON))
		BBCON.add_behavior(behavior.Behavior5(BBCON.sensobs_objects[1], BBCON.sensobs_objects[2], BBCON))
		BBCON.add_behavior(behavior.Behavior6(BBCON))
		TOTAL_STEPS = 0
		BUTTON_BUTTON = True
		zumo_button.ZumoButton().wait_for_press()
		while BUTTON_BUTTON:
			TOTAL_STEPS += 1
			print('this is a step number: ' + str(TOTAL_STEPS))
			BBCON.run_one_timestep()			
		


if __name__ == "__main__":
    main()

