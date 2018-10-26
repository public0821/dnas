import sys

from cli import Command
from service.samba import SambaService, SambaConfig
import subprocess
import os

class Samba(Command):
    def __init__(self, parent, name=None):
        super().__init__(parent, name)
        self.add_child(Status(parent=self, name='status'))
        self.add_child(Install(parent=self, name='install'))
        self.add_child(Start(parent=self, name='start'))
        self.add_child(Restart(parent=self, name='restart'))
        self.add_child(Stop(parent=self, name='stop'))
        self.add_child(Info(parent=self, name='info'))
        self.add_child(Add(parent=self, name='add'))
        self.add_child(Remove(parent=self, name='rm'))
        self.add_child(Clear(parent=self, name='clear'))

    def description(self):
        return _('Configure Samba')

class Status(Command):
    def __init__(self, parent, name=None):
        super().__init__(parent, name)
#        self.add_argument('-n', '--name', required=True, help = "the tenant name you want to create")
#        self.add_argument('-u', '--user', required=True, help = "user name with system admin role")
#        self.add_argument('--password', required=True, help = "password of the user")


    def description(self):
        return _('Show the status of Samba')

    def execute(self, args):
        SambaService.status(show_detail=True)

class Install(Command):
    def __init__(self, parent, name=None):
        super().__init__(parent, name)

    def description(self):
        return _('Install Samba')

    def execute(self, args):
        SambaService.install()

class Start(Command):
    def __init__(self, parent, name=None):
        super().__init__(parent, name)

    def description(self):
        return _('Start Samba')

    def execute(self, args):
        SambaService.start()

class Restart(Command):
    def __init__(self, parent, name=None):
        super().__init__(parent, name)

    def description(self):
        return _('Restart Samba')

    def execute(self, args):
        SambaService.restart()

class Stop(Command):
    def __init__(self, parent, name=None):
        super().__init__(parent, name)

    def description(self):
        return _('Stop Samba')

    def execute(self, args):
        SambaService.stop()

class Info(Command):
    def __init__(self, parent, name=None):
        super().__init__(parent, name)

    def description(self):
        return _('Show Samba info')

    def execute(self, args):
        SambaConfig().print()

class Add(Command):
    def __init__(self, parent, name=None):
        super().__init__(parent, name)
        self.add_argument('-n', '--name', required=True, help = "the share point's name")
        self.add_argument('-p', '--path', required=True, help = "the path to share")
        self.add_argument('--readonly', required=False, action='store_true', default=False, help = "set the share point readonly")

    def description(self):
        return _('Add share point')

    def execute(self, args):
        conf = SambaConfig()
        if conf.add(args.name, args.path, args.readonly):
            conf.save()

class Remove(Command):
    def __init__(self, parent, name=None):
        super().__init__(parent, name)
        self.add_argument('-n', '--name', required=True, help = "the share point's name")

    def description(self):
        return _('Remove share point')

    def execute(self, args):
        conf = SambaConfig()
        if conf.remove(args.name):
            conf.save()

class Clear(Command):
    def __init__(self, parent, name=None):
        super().__init__(parent, name)

    def description(self):
        return _('Cleare all share point')

    def execute(self, args):
        conf = SambaConfig()
        if conf.clear():
            conf.save()
