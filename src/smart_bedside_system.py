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

        # User Story #1
        self.spo2_hr_sensor = DFRobot_BloodOxygen_S()
        self.spo2_hr_sensor.begin()
        self.spo2_hr_sensor.sensor_start_collect()

        # Leave these unchanged for now
        self.alarm_on = None
        self.o2_servo = None
        self.o2_valve_angle = None

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
        # See User Story #3.
        pass

    def set_o2_valve_angle(self, angle: float) -> None:
        # See User Story #4.
        pass

    def manage_oxygen_valve(self) -> None:
        # See User Story #5.
        pass
