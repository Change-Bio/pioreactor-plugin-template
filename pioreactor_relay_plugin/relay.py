# -*- coding: utf-8 -*-
from __future__ import annotations

from pioreactor.background_jobs.base import BackgroundJobWithDodgingContrib
from pioreactor.config import config
from pioreactor.hardware import PWM_TO_PIN
from pioreactor.utils.pwm import PWM
from pioreactor.whoami import get_latest_experiment_name
from pioreactor.whoami import get_unit_name


class Relay(BackgroundJobWithDodgingContrib):

    published_settings = {
        "on": {"datatype": "boolean", "settable": True},
    }

    job_name = "relay"

    def __init__(self, unit, experiment, start_on=True):
        super().__init__(unit=unit, experiment=experiment, plugin_name="relay")
        if start_on:
            self.duty_cycle = 100
            self.on = True
        else:
            self.duty_cycle = 0
            self.on = False

        self.pwm_pin = PWM_TO_PIN[config.get("PWM_reverse", "relay")]
        # looks at config.ini/configuration on UI to match
        # changed PWM channel 2 to "relay" on leader
        # whatevers connected to channel 2 will turn on/off

        self.pwm = PWM(
            self.pwm_pin, hz=10
        )  # since we also go 100% high or 0% low, we don't need hz.
        self.pwm.lock()

    def set_on(self, value: bool):
        if value == self.on:
            return
        if value:
            self.set_duty_cycle(100)
            self.on = True
        else:
            self.set_duty_cycle(0)
            self.on = False

    def set_duty_cycle(self, new_duty_cycle: float):
        self.duty_cycle = new_duty_cycle
        self.pwm.change_duty_cycle(self.duty_cycle)

    def on_init_to_ready(self):
        self.logger.debug(f"Starting relay {'ON' if self.on else 'OFF'}.")
        self.pwm.start(self.duty_cycle)

    def on_ready_to_sleeping(self):
        self.set_on(False)

    def on_sleeping_to_ready(self):
        self.set_on(True)

    def on_disconnected(self):
        self.set_on(False)
        self.pwm.cleanup()

    def action_to_do_before_od_reading(self):
        self.set_on(False)

    def action_to_do_after_od_reading(self):
        self.set_on(True)


import click


@click.command(name="relay")
@click.option("--start-off", is_flag=True)
def click_relay(start_off):
    """
    Start the relay
    """
    job = Relay(
        unit=get_unit_name(), experiment=get_latest_experiment_name(), start_on=not start_off
    )
    job.block_until_disconnected()


if __name__ == "__main__":
    click_relay()
