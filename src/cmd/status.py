import sys

from cli import Command
from service.samba import SambaService
import subprocess
import os

class Status(Command):
    def __init__(self, parent, name=None):
        super().__init__(parent, name)

    def description(self):
        return _('Show the status of each service')

    def execute(self, args):
        print("Samba:", SambaService.status())

