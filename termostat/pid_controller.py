from simple_pid import PID

from loguru import logger


class PidController(PID):
    def __init__(
        self,
        target_temperature: float,
        max_power=100.0,
        min_power=0.0,
        proportional_gain=4,
        integral_gain=0.01,
        derivative_gain=0.01,
    ) -> None:
        super().__init__(
            proportional_gain, integral_gain, derivative_gain, target_temperature
        )
        self.max_power = max_power
        self.min_power = min_power
        self.logger = logger.bind(name=type(self).__name__)

    def get_power_value(self, temperature: float) -> float:
        power = self(temperature)
        self.logger.debug(
            "Power value for temperature {:.2f}: {:.2f}",
            temperature,
            power,
            feature="f-strings",
        )
        power = max(self.min_power, min(self.max_power, power))
        return power
