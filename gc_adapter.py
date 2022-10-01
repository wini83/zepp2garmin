import os
import subprocess

from measurement import Measurement


class GarminAdapter:
    email: str
    passw: str

    def __init__(self, email: str, passw: str):
        self.email = email
        self.passw = passw

    def log_measurement(self, item: Measurement):
        if item.weight is not None and item.muscleRate is not None:
            process = subprocess.Popen(self.generate_gc_payload(item), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            exit_code = process.wait()
            return stdout.decode("utf-8").strip(), stderr.decode("utf-8").strip(), exit_code
        else:
            return None, "Export not possible: Weight or Muscle rate not available", 1

    def generate_gc_payload(self, item: Measurement) -> str:
        command_path = os.path.dirname(__file__)
        message = command_path + '/bodycomposition upload '
        if item.boneMass is not None:
            message += '--bone-mass ' + "{:.2f}".format(item.boneMass) + ' '
        if item.bmi is not None:
            message += '--bmi ' + "{:.2f}".format(item.bmi) + ' '
        message += '--email ' + self.email + ' '
        if item.fatRate is not None:
            message += '--fat ' + "{:.2f}".format(item.fatRate) + ' '
        if item.bodyWaterRate is not None:
            message += '--hydration ' + "{:.2f}".format(item.bodyWaterRate) + ' '
        # message += '--metabolic-age ' + "{:.0f}".format(lib.getMetabolicAge()) + ' '
        if item.muscleRate is not None:
            message += '--muscle-mass ' + "{:.2f}".format(item.muscleRate) + ' '
        message += '--password ' + self.passw + ' '
        # message += '--physique-rating ' + "{:.2f}".format(lib.getBodyType()) + ' '
        message += '--unix-timestamp ' + int(item.timestamp.timestamp()).__str__() + ' '
        if item.visceralFat is not None:
            message += '--visceral-fat ' + "{:.2f}".format(item.visceralFat) + ' '
        if item.weight is not None:
            message += '--weight ' + "{:.2f}".format(item.weight) + ' '
        return message
