""" modoule for sensob class """
from irproximity_sensor import IRProximitySensor
# from irproximity_sensor import *
from ultrasonic import Ultrasonic
from reflectance_sensors import ReflectanceSensors
from camera import Camera
# from camera import *
from imager2 import Imager
from PIL import Image


class Sensob:
    """ class Sensob is an interface between the sensors and
        bbcon's behaviours """

    def __init__(self, sensors=[]):
        """ initialize """
        # associated sensors [ex. IR sensors]
        self.sensors = sensors
        # its value [ex. (0, 2)]
        self.value = None

    def update(self):
        """ fetch relevant sensor value(s) and convert them
            into the pre-processed sensob value. Only do this
            once each timestep, even if several behaviours
            share the same sensob.
            For each sensor in self.sensors, append the
            updated raw data to an array 'sensor_data'.
            Then run 'process_sensor_data' with the array
            as an argument.
            return - self.value"""
        sensor_data = []
        for sensor in self.sensors:
            sensor_data.append(sensor.update())
        self.process_sensor_data(sensor_data)
        print("self.value: ", self.value)
        return self.value

    def process_sensor_data(self, sensor_data):
        """ every instance has its own way of processing
            the raw data. 'sensor_data' is an array of
            arguments."""


class Proximity(Sensob):
    """ Proximity is an instance of Sensob which
        determines what the distance to the nearest
        object is. Both the IRProximitySensor and the
        Ultrasonic sensor is used. The IR looks for a
        line, and the US looks for objects. """

    def __init__(self):
        """ Initialize IR and US sensors and add them
            as sensors in a Sensob as well. """
        ir_ = IRProximitySensor()
        us_ = Ultrasonic()
        super().__init__(sensors=[ir_, us_])

    def process_sensor_data(self, sensor_data):
        """ processes the data from both IR and US
            to detect any object within 5 cm, if
            there is any.
            returns True if an object is less than
                5 cm away or a line is detected,
                and False if opposite. """
        ir_data = sensor_data[0]
        us_data = sensor_data[1]
        too_close = False

        for measurement in ir_data:
            if measurement:
                too_close = True
        if us_data < 5:
            too_close = True
        self.value = too_close


class LineDetector(Sensob):
    """ LineDetector is an instance of Sensob which
        processes the data from the IRProximitySensor
        and sets self.value to the distance from where
        we get the strongest indication of a line.
        """

    def __init__(self):
        """ initialize IRProximitySensor """
        rs_ = ReflectanceSensors()
        super(LineDetector, self).__init__(sensors=[rs_])

    def process_sensor_data(self, sensor_data):
        """ process the data from the IR sensor. """
        self.value = sensor_data[0]


class MeasureDistance(Sensob):
    """ MeasureDistance measures the distance to an object
        in front of the robot. Uses ultrasonic sensor to
        measure the distance. """

    def __init__(self):
        """ initialize """
        self.us_ = Ultrasonic()
        super().__init__(sensors=[self.us_])

    def process_sensor_data(self, sensor_data):
        """ sets the value to sensor_data[0] """
        self.value = sensor_data[0]


class Cameraob(Sensob):
    """ Cameraob is an instance of Sensob which connects
        with the camera-sensor. """

    def __init__(self):
        """ initialize """
        self.image_width = 128
        self.image_height = 96
        self.image_size = self.image_width * self.image_height

        cam = Camera(self.image_width, self.image_height, img_rot=0)

        # defines the min and max values that counts as red
        self.min = (256, 40, 0)
        self.max = (50, 0, 0)

        super().__init__(sensors=[cam])

    def process_sensor_data(self, sensor_data):
        """ process the data from the camera sensor. """
        img = sensor_data[0]
        image = Imager(image=img)
        # excuse me
        image = image.map_color_wta()
        red_pixels = 0

        for pixel in image.image.getdata():
            if pixel[0] > 200 and pixel[1] == 0 and pixel[2] == 0:
                red_pixels += 1

        print("The amount of red pixels are:", red_pixels)
        self.value = red_pixels / self.image_size
