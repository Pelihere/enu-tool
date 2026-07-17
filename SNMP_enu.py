from subprocess import run 
from platform import system


class Enumeration:
    def __init__(self, target):
        self.targe = target
        os = system().lower()

    def 