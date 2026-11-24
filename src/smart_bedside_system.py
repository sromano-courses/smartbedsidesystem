from src.smart_bedside_error import SmartBedsideError

try:
    import RPi.GPIO as GPIO
except ImportError:
    from mock import GPIO

try:
    from pinpong.libs.dfrobot_max30102 import DFRobot_BloodOxygen_S
except ImportError:
    from mock.max30102 import DFRobot_BloodOxygen_S


class SmartBedsideSystem:

    BUZZER_PIN = 22
    BUTTON_PIN = 16
    O2_SERVO_PIN = 12

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # User Story 1
        self.spo2_hr_sensor = DFRobot_BloodOxygen_S()
        self.spo2_hr_sensor.begin()
        self.spo2_hr_sensor.sensor_start_collect()

        # User Story 2
        GPIO.setup(self.BUZZER_PIN, GPIO.OUT)
        self.alarm_on = False

        # User Story 3
        GPIO.setup(self.BUTTON_PIN, GPIO.IN)

        # User Story 4
        GPIO.setup(self.O2_SERVO_PIN, GPIO.OUT)
        self.o2_servo = GPIO.PWM(self.O2_SERVO_PIN, 50)
        self.o2_servo.start(5.0)

        self.o2_valve_angle = 0.0

    def read_vital_signs(self) -> int:
        """
        Read the patient's blood oxygen saturation (SpO₂).
        Returns: int: SpO₂ percentage (70–100).
        Raises: SmartBedsideError: If the sensor returns an invalid reading (-1).
        """

        spo2 = self.spo2_hr_sensor.get_spo2()

        if spo2 == -1:
            raise SmartBedsideError()

        return spo2

    def manage_alarm(self) -> None:
        spo2 = self.read_vital_signs()

        if spo2 < 88:
            GPIO.output(self.BUZZER_PIN, True)
            self.alarm_on = True
        else:
            GPIO.output(self.BUZZER_PIN, False)
            self.alarm_on = False

    def stop_alarm(self) -> None:
        if GPIO.input(self.BUTTON_PIN):
            GPIO.output(self.BUZZER_PIN, False)
            self.alarm_on = False

    def set_o2_valve_angle(self, angle: float) -> None:
        if angle < 0.0 or angle > 180.0:
            raise SmartBedsideError()

        duty_cycle = 5.0 + (angle / 180.0) * 5.0

        self.o2_servo.ChangeDutyCycle(duty_cycle)
        self.o2_valve_angle = angle

    def manage_oxygen_valve(self) -> None:
        spo2 = self.read_vital_signs()

        if spo2 < 95:
            self.set_o2_valve_angle(180.0)
        else:
            self.set_o2_valve_angle(0.0)