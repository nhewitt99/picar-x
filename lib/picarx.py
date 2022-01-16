import time
import atexit
import logging
from logdecorator import log_on_start, log_on_end, log_on_error
logging.basicConfig(level=logging.DEBUG, datefmt ="%H:%M:%S")

# use rpi as test to import sim or hardware
try:
    import RPi.GPIO
    from hardware.pwm import PWM
    from hardware.pin import Pin
    from hardware.adc import ADC
    from hardware.servo import Servo
except (ImportError, RuntimeError):
    print('Could not import one or more hardware classes. Defaulting to simulation classes. TODO: dump stack trace')
    from simulation.pwm import PWM
    from simulation.pin import Pin
    from simulation.adc import ADC
    from simulation.servo import Servo
    # import simulation

from filedb import fileDB


class Picarx(object):
    PERIOD = 4095
    PRESCALER = 10
    TIMEOUT = 0.02

    @log_on_start(logging.DEBUG, 'Initializing a Picarx...')
    @log_on_error(logging.ERROR, 'Unexpected error in Picarx init!', reraise=True)
    @log_on_end(logging.DEBUG, 'Initialized a Picarx.')
    def __init__(self):
        self.dir_servo_pin = Servo(PWM('P2'))
        self.camera_servo_pin1 = Servo(PWM('P0'))
        self.camera_servo_pin2 = Servo(PWM('P1'))

#        self.config_flie = fileDB('/home/pi/.config')
        self.config_flie = fileDB('/home/nhewitt/.picarx_config')

        self.dir_cal_value = int(self.config_flie.get("picarx_dir_servo", default_value=0))
        self.cam_cal_value_1 = int(self.config_flie.get("picarx_cam1_servo", default_value=0))
        self.cam_cal_value_2 = int(self.config_flie.get("picarx_cam2_servo", default_value=0))
        self.dir_servo_pin.angle(self.dir_cal_value)
        self.camera_servo_pin1.angle(self.cam_cal_value_1)
        self.camera_servo_pin2.angle(self.cam_cal_value_2)

        self.left_rear_pwm_pin = PWM("P13")
        self.right_rear_pwm_pin = PWM("P12")
        self.left_rear_dir_pin = Pin("D4")
        self.right_rear_dir_pin = Pin("D5")


        self.S0 = ADC('A0')
        self.S1 = ADC('A1')
        self.S2 = ADC('A2')

        self.motor_direction_pins = [self.left_rear_dir_pin, self.right_rear_dir_pin]
        self.motor_speed_pins = [self.left_rear_pwm_pin, self.right_rear_pwm_pin]
        self.cali_dir_value = self.config_flie.get("picarx_dir_motor", default_value="[1,1]")
        self.cali_dir_value = [int(i.strip()) for i in self.cali_dir_value.strip("[]").split(",")]
        self.cali_speed_value = [0, 0]
        self.dir_current_angle = 0

        for pin in self.motor_speed_pins:
            pin.period(self.PERIOD)
            pin.prescaler(self.PRESCALER)

        atexit.register(self.stop)


    @log_on_start(logging.DEBUG, 'Setting motor {motor} to speed {speed}...')
    @log_on_error(logging.ERROR, 'Unexpected error when setting motor speed!', reraise=True)
    @log_on_end(logging.DEBUG, 'Set motor {motor} to speed {speed}.')
    def set_motor_speed(self,motor,speed):
        # global cali_speed_value,cali_dir_value
        motor -= 1
        if speed >= 0:
            direction = 1 * self.cali_dir_value[motor]
        elif speed < 0:
            direction = -1 * self.cali_dir_value[motor]
        speed = abs(speed)
        if speed != 0:
            speed = int(speed /2 ) + 50
        speed = speed - self.cali_speed_value[motor]
        if direction < 0:
            self.motor_direction_pins[motor].high()
            self.motor_speed_pins[motor].pulse_width_percent(speed)
        else:
            self.motor_direction_pins[motor].low()
            self.motor_speed_pins[motor].pulse_width_percent(speed)

    def motor_speed_calibration(self,value):
        # global cali_speed_value,cali_dir_value
        self.cali_speed_value = value
        if value < 0:
            self.cali_speed_value[0] = 0
            self.cali_speed_value[1] = abs(self.cali_speed_value)
        else:
            self.cali_speed_value[0] = abs(self.cali_speed_value)
            self.cali_speed_value[1] = 0

    def motor_direction_calibration(self,motor, value):
        # 0: positive direction
        # 1:negative direction
        # global cali_dir_value
        motor -= 1
        if value == 1:
            self.cali_dir_value[motor] = -1 * self.cali_dir_value[motor]
        self.config_flie.set("picarx_dir_motor", self.cali_dir_value)

    def dir_servo_angle_calibration(self,value):
        # global dir_cal_value
        self.dir_cal_value = value
        print("calibrationdir_cal_value:",self.dir_cal_value)
        self.config_flie.set("picarx_dir_servo", "%s"%value)
        self.dir_servo_pin.angle(value)

    def set_dir_servo_angle(self,value):
        # global dir_cal_value
        self.dir_current_angle = value
        angle_value  = value + self.dir_cal_value
        print("angle_value:",angle_value)
        # print("set_dir_servo_angle_1:",angle_value)
        # print("set_dir_servo_angle_2:",dir_cal_value)
        self.dir_servo_pin.angle(angle_value)

    def camera_servo1_angle_calibration(self,value):
        # global cam_cal_value_1
        self.cam_cal_value_1 = value
        self.config_flie.set("picarx_cam1_servo", "%s"%value)
        print("cam_cal_value_1:",self.cam_cal_value_1)
        self.camera_servo_pin1.angle(value)

    def camera_servo2_angle_calibration(self,value):
        # global cam_cal_value_2
        self.cam_cal_value_2 = value
        self.config_flie.set("picarx_cam2_servo", "%s"%value)
        print("picarx_cam2_servo:",self.cam_cal_value_2)
        self.camera_servo_pin2.angle(value)

    def set_camera_servo1_angle(self,value):
        # global cam_cal_value_1
        self.camera_servo_pin1.angle(-1*(value + -1*self.cam_cal_value_1))
        # print("self.cam_cal_value_1:",self.cam_cal_value_1)
        print((value + self.cam_cal_value_1))

    def set_camera_servo2_angle(self,value):
        # global cam_cal_value_2
        self.camera_servo_pin2.angle(-1*(value + -1*self.cam_cal_value_2))
        # print("self.cam_cal_value_2:",self.cam_cal_value_2)
        print((value + self.cam_cal_value_2))

    def get_adc_value(self):
        adc_value_list = []
        adc_value_list.append(self.S0.read())
        adc_value_list.append(self.S1.read())
        adc_value_list.append(self.S2.read())
        return adc_value_list

    def set_power(self,speed):
        self.set_motor_speed(1, speed)
        self.set_motor_speed(2, speed) 

    @log_on_start(logging.DEBUG, 'Starting to move backward at speed {speed}...')
    @log_on_error(logging.ERROR, 'Unexpected error moving backward!', reraise=True)
    @log_on_end(logging.DEBUG, 'Moving backward at speed {speed}.')
    def backward(self,speed):
        current_angle = self.dir_current_angle
        if current_angle != 0:
            abs_current_angle = abs(current_angle)
            # if abs_current_angle >= 0:
            if abs_current_angle > 40:
                abs_current_angle = 40
            power_scale = (100 - abs_current_angle) / 100.0 
            print("power_scale:",power_scale)
            if (current_angle / abs_current_angle) > 0:
                self.set_motor_speed(1, -1*speed)
                self.set_motor_speed(2, speed * power_scale)
            else:
                self.set_motor_speed(1, -1*speed * power_scale)
                self.set_motor_speed(2, speed )
        else:
            self.set_motor_speed(1, -1*speed)
            self.set_motor_speed(2, speed)  

    @log_on_start(logging.DEBUG, 'Starting to move forward at speed {speed}...')
    @log_on_error(logging.ERROR, 'Unexpected error moving forward!', reraise=True)
    @log_on_end(logging.DEBUG, 'Moving forward at speed {speed}.')
    def forward(self,speed):
        current_angle = self.dir_current_angle
        if current_angle != 0:
            abs_current_angle = abs(current_angle)
            # if abs_current_angle >= 0:
            if abs_current_angle > 40:
                abs_current_angle = 40
            power_scale = (100 - abs_current_angle) / 100.0 
            print("power_scale:",power_scale)
            if (current_angle / abs_current_angle) > 0:
                self.set_motor_speed(1, speed)
                self.set_motor_speed(2, -1*speed * power_scale)
            else:
                self.set_motor_speed(1, speed * power_scale)
                self.set_motor_speed(2, -1*speed )
        else:
            self.set_motor_speed(1, speed)
            self.set_motor_speed(2, -1*speed)

    @log_on_start(logging.DEBUG, 'Stopping...')
    @log_on_error(logging.ERROR, 'Unexpected error while stopping!', reraise=True)
    @log_on_end(logging.DEBUG, 'Stopped.')
    def stop(self):
        self.set_motor_speed(1, 0)
        self.set_motor_speed(2, 0)

    @log_on_start(logging.DEBUG, 'Starting to move at speed {speed} with angle {angle}...')
    @log_on_error(logging.ERROR, 'Unexpected error moving!', reraise=True)
    @log_on_end(logging.DEBUG, 'Moving at speed {speed} with angle {angle}.')
    def move(self, speed, angle):
        self.set_dir_servo_angle(angle)
        if speed >= 0:
            self.forward(speed)
        else:
            self.backward(-speed)

    @log_on_start(logging.DEBUG, 'Parallel parking...')
    @log_on_error(logging.ERROR, 'Unexpected error parking!', reraise=True)
    @log_on_end(logging.DEBUG, 'Parked.')
    def parallel_park(self, speed, left=True):
        # Reverse only
        speed = -abs(speed)

        # First turn left or turn right
        angle = 60 if left else -60

        self.move(speed, angle)
        time.sleep(1.5)
        self.stop()
        self.move(speed, -angle)
        time.sleep(1.5)
        self.stop()

    @log_on_start(logging.DEBUG, 'Starting k-turn...')
    @log_on_error(logging.ERROR, 'Unexpected error turning!', reraise=True)
    @log_on_end(logging.DEBUG, 'Finished k-turn.')
    def k_turn(self, speed, left=True):
        speed = abs(speed)
        angle = 60 if left else -60

        self.move(speed, angle)
        time.sleep(0.5)
        self.stop()
        self.move(speed, -angle)
        time.sleep(1.5)
        self.stop()
        self.move(-speed, angle)
        time.sleep(2.0)
        self.stop()

    def forward_demo(self, speed):
        self.move(speed, 0)
        time.sleep(1.0)
        self.stop()

    def Get_distance(self):
        timeout=0.01
        trig = Pin('D8')
        echo = Pin('D9')

        trig.low()
        time.sleep(0.01)
        trig.high()
        time.sleep(0.000015)
        trig.low()
        pulse_end = 0
        pulse_start = 0
        timeout_start = time.time()
        while echo.value()==0:
            pulse_start = time.time()
            if pulse_start - timeout_start > timeout:
                return -1
        while echo.value()==1:
            pulse_end = time.time()
            if pulse_end - timeout_start > timeout:
                return -2
        during = pulse_end - pulse_start
        cm = round(during * 340 / 2 * 100, 2)
        #print(cm)
        return cm


def print_options():
    print('Please enter one of the following:')
    print('1: Drive forward')
    print('2: Parallel park')
    print('3: K-turn')
    print('Q: Exit')


if __name__ == "__main__":
    px = Picarx()

    print_options()

    options = {1: px.forward_demo,
               2: px.parallel_park,
               3: px.k_turn}
    speed = 50

    while True:
        print('Enter your choice:')
        choice = input()

        if choice in ['q', 'Q', 'exit', 'quit']:
            print('Exiting!')
            break
        elif int(choice) in options.keys():
            print(f'Executing option {choice}!\n')
            options[int(choice)](speed)
        else:
            print('Invalid choice!\n')
            print_options()