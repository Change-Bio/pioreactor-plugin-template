# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name="pioreactor_relay_plugin",
    version="0.1.0",
    license="MIT",
    description="Turn the PWM channels into a simple on/off relay for additional hardware.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author_email="cam@pioreactor.com",
    author="Kelly Tran, Cam Davidson-Pilon",
    url="https://github.com/CamDavidsonPilon/pioreactor-relay-plugin",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "pioreactor.plugins": "pioreactor_relay_plugin = pioreactor_relay_plugin"
    },
)