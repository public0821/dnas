from cli import Command
from cmd.status import Status
from cmd.samba import Samba

class RootCommand(Command):
    def __init__(self, name):
        super().__init__(name=name)
        self.add_child(Test(parent=self, name='test'))
        self.add_child(Status(parent=self, name='status'))
        self.add_child(Samba(parent=self, name='samba'))

    def description(self):
        return _('''Management tool of {}''').format(self.name())

class Test(Command):
    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.add_argument('-n', '--name', required=True, help = "the tenant name you want to create")
        self.add_argument('-u', '--user', required=True, help = "user name with system admin role")
        self.add_argument('--password', required=True, help = "password of the user")

    def description(self):
        return 'used to test cli'

    def execute(self, args):
        print(self.name() + ' executed!')
