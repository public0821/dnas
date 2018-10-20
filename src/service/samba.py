import shell
import subprocess
import configparser

class SambaService(object):

    @classmethod    
    def status(cls, show_detail=False):
        has_samba = cls.has_installed()
        if not has_samba:
            return "not installed"
        if show_detail:
            shell.system("service samba status")
        else:
            started = shell.check_command("service samba status")
            if not started:
                return "not started"
            return "running..."

    @classmethod    
    def start(cls):
        has_samba = cls.has_installed()
        if not has_samba:
            print("Samba has not been installed")
            return
        shell.system("service samba start")

    @classmethod    
    def stop(cls):
        has_samba = cls.has_installed()
        if not has_samba:
            print("Samba has not been installed")
            return
        shell.system("service samba stop")

    @classmethod    
    def restart(cls):
        has_samba = cls.has_installed()
        if not has_samba:
            print("Samba has not been installed")
            return
        shell.system("service samba restart")

    @classmethod    
    def install(cls):
        has_samba = cls.has_installed()
        if has_samba:
            print("Smaba has already been installed")
            return
        shell.system("apt-get install -y samba")

    @classmethod
    def has_installed(cls):
        return shell.check_command("which samba")        

class SambaConfig(object):
    def __init__(self, path=None):
        self._path = path
        self._config = None
        if path is None:
            self._path = "/etc/samba/smb.conf"
        self._load()

    def _load(self):
        self._config = configparser.RawConfigParser()
        self._config.read(self._path)

    def save(self):
        with open(self._path, 'w') as configfile:
            self._config.write(configfile)

    def print(self):
        for section in self._config.sections():
            print("[{}]".format(section))
            for k in self._config[section]:
                print("{0} = {1}".format(k, self._config[section][k]))
            print()

    #clear all share point
    def clear(self):
        sections = self._config.sections()
        removed = False
        for s in sections:
            if s != "global":
                self._config.remove_section(s)
                removed = True
        return removed

    def add(self, name, path, readonly):
        if self._config.has_section(name):
            print("section '{}' already exists".format(name))
            return False
        self._config.add_section(name)
        self._config.set(name, "path", path)
        self._config.set(name, "writable", "no" if readonly else "yes")
        self._config.set(name, "browsable", "yes")
        self._config.set(name, "guest ok", "yes")
        if not readonly:
            self._config.set(name, "create mask", "0660")
            self._config.set(name, "directory mask", "0771")
        return True

    def remove(self, name):
        if not self._config.has_section(name):
            print("section '{}' does not exist".format(name))
            return False
        return self._config.remove_section(name)
