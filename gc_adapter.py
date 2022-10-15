import os
import subprocess
from abc import ABC, abstractmethod
import time
from queue import Queue
from threading import Thread
from measurement import Measurement


class AbstractAdapter(ABC):
    email: str
    passw: str

    @abstractmethod
    def run(self, payload: Measurement):
        pass


class QueueHandler(Thread):
    queue: Queue
    adapter: AbstractAdapter

    def __init__(self, payload_list: list[Measurement], queue: Queue, adapter: AbstractAdapter):
        super().__init__()
        self.queue = queue
        self.adapter = adapter
        self.payload_list = payload_list
        self.running = False
        self.progress: int = 0

    def run(self):
        self.running = True
        counter = 0
        self.progress = 0
        for payload in self.payload_list:
            result = self.adapter.run(payload)
            self.queue.put(result)
            counter += 1
            progress_float = (counter / len(self.payload_list))*100
            self.progress = progress_float.__floor__()

        self.running = False
        self.progress = 100


class GarminResult:
    def __init__(self, payload: Measurement, std_out: str, std_err: str, code: int):
        self.payload: Measurement = payload
        self.std_out: str = std_out
        self.std_err: str = std_err
        self.code: int = code


class GarminAdapter(AbstractAdapter):
    def __init__(self, email: str, passw: str):
        super().__init__()
        self.email: str = email
        self.passw: str = passw

    def run(self, payload: Measurement):
        if payload.weight is not None and payload.muscleRate is not None:
            process = subprocess.Popen(self._generate_gc_payload(payload), stderr=subprocess.PIPE,
                                       stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            exit_code = process.wait()
            result = GarminResult(payload=payload,
                                  std_out=stdout.decode("utf-8").strip(),
                                  std_err=stderr.decode("utf-8").strip(),
                                  code=exit_code)
        else:
            result = GarminResult(payload=payload,
                                  std_out="",
                                  std_err="Export not possible: Weight or Muscle rate not available",
                                  code=1)
        return result

    def _generate_gc_payload(self, item: Measurement) -> str:
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


class FakeAdapter(AbstractAdapter):

    def __init__(self, email: str, passw: str):
        super().__init__()
        self.email: str = email
        self.passw: str = passw

    def run(self, payload: Measurement):
        if payload.weight is not None and payload.muscleRate is not None:
            time.sleep(3)
            result = GarminResult(payload=payload,
                                  std_out="",
                                  std_err="Dupa 8",
                                  code=0)
        else:
            result = GarminResult(payload=payload,
                                  std_out="",
                                  std_err="Export not possible: Weight or Muscle rate not available",
                                  code=1)
        return result
