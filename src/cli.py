import atexit
import os
import sys
import traceback
import logging
import readline
import argparse

from texttable import TextTable
from exceptions import Error

class Command(object):
    def __init__(self, parent=None, name=None):
        self.__parent = parent
        self.__children = {}
        self.__args = {}  #arg short name to supported values
        self.__arg_f2s_names = {}#arg full name to short name
        self.__name = name
        self.__parser = None
        if parent:
            parent.add_child(self)

    def parent(self):
        return self.__parent

    def add_child(self, child):
        self.__children[child.name()] = child

    def has_child(self):
        return len(self.__children) > 0

    def child(self, name):
        return self.__children.get(name)

    def start(self, args):
        logging.debug("invoke {}.execute with args: {}".format(self.class_name(), args))

        if '--help' in args or ('-h' in args and '-h' not in self.__args):
            print(self.help())
            return

        if self.has_child() and args:  #command has children does not support args by now
            raise Error(_("Unsupported subcommand '{}'").format(args[0]))
        if self.has_child() and not args:
            print(self.help())
            return

        try:
            if self.__parser:
                return self.execute(self.__parser.parse_args(args))
            else:
                return self.execute(None)
        except SystemExit:
            return


    def execute(self, args):
        raise NotImplementedError("Should implement 'execute' function in class '{}'".format(self.class_name()))

    def description(self):
        raise NotImplementedError("Should implement 'description' function in class '{}'".format(self.class_name()))

    def name(self):
        if self.__name:
            return self.__name
        return self.class_name()

    def class_name(self):
        return type(self).__name__.lower()

    def matching_words(self, args, text):
        if self.has_child():
            return self.matching_children(args, text)
        else:
            return self.matching_args(args, text)

    def matching_children(self, args, text):
        if args:    #command has children should not have args
            return []

        return [w for w in self.__children.keys() if w.startswith(text)]

    def __get_match_args(self, args, text):
        available_args = set(self.__args.keys())
        for arg in args:
            if arg in available_args:
                available_args.remove(arg)
        return [w for w in available_args if w.startswith(text)]

    def __get_match_arg_values(self, arg, text):
        values = self.__args[arg]
        return [w for w in values if w.startswith(text)]

    def __validate_args(self, args):
        return True

    def matching_args(self, args, text):
        if not self.__validate_args(args):
            return []

        last_arg = args[-1] if args and args[-1][0] == '-' else None
        if last_arg and self.__args[last_arg] is not None:
            return self.__get_match_arg_values(last_arg, text)

        return self.__get_match_args(args, text)

    def help(self):
        if self.has_child():
            return self.children_help()
        elif self.__parser:
            return self.__parser.format_help()
        else:
            raise NotImplementedError("Should implement 'help' function in class '{}'".format(self.class_name()))

    def children_help(self):
        helpstr = self.help_template()
        table = TextTable([_('Name'), _('Description')])
        for child in self.__children.values():
            table.add_row(('  ' + child.name(), child.description()))
        return helpstr.format(description=self.description(), linesep=os.linesep, emptyline=os.linesep*2, 
            command=self.full_name(), commands=table.to_string(ignore_field_names=True))

    def help_template(self):
        helpstr = _('{description}{emptyline}Usage: {command} [command]{emptyline}Available Commands:{linesep}{commands}{emptyline}')
        helpstr += _('''Use "{command} [command] --help" for more information about a command.''')
        return helpstr

    # def add_args(self, args):
    #     for arg in args:
    #         self.__args[arg] = []
    def __init_argparse(self):
        self.__parser = argparse.ArgumentParser(prog=self.full_name(),
                description=self.description(), add_help=False)
        self.__parser.add_argument('--help',  help=argparse.SUPPRESS)

    def add_argument(self, *args, **kwargs):
        if not self.__parser:
            self.__init_argparse()
        short_name = args[0]
        full_name = args[1] if len(args) > 1 else None
        if full_name:
            self.__arg_f2s_names[full_name] = short_name
        self.__args[short_name] = []
        self.__parser.add_argument(*args, **kwargs)

    def full_name(self):
        if self.parent():
            fullname = '{} {}'.format(self.parent().full_name(), self.name())
            return fullname
        else:
            return self.name()

    def set_values(self, arg, values):
        if arg.startswith("--"):
            self.__args[self.__arg_f2s_names[arg]] = values
        else:
            self.__args[arg] = values

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


def save_history(prev_h_len, histfile):
    new_h_len = readline.get_history_length()
    readline.set_history_length(1000)
    # readline.append_history_file(new_h_len - prev_h_len, histfile)

class CommandLine(object):
    def __init__(self, root_command):
        self.__root = root_command
        self.__delims = ' \t\n'
        self.__name = root_command.name().lower()

    def get_prompt(self):
        is_root_user = (os.geteuid() == 0)
        prompt = self.__name
        if is_root_user:
            prompt += '#'
        else:
            prompt += '$'
        return prompt

    def execute(self, line):
        success, command, args = self.parse_command(line)
        if not success:
            print(_("can't find command {}").format(args[0]))
            return False

        try:
            command.start(args)
        except Exception:
            print(traceback.format_exc())
            return False

        return True
           
    def input_loop(self):
        prompt = self.get_prompt()
        while True:
            try:
                line = input(prompt + ' ')
            except KeyboardInterrupt:
                print()
                continue
            if len(line) == 0:
                continue
            if line in ('q', 'quit', 'e', 'exit'):
                sys.exit(0)
            elif line in ('hi', 'history'):
                self.__print_history()
                continue
            elif line in ('?', 'h', 'help'):   
                logging.debug(self.__root.help())                
                print(self.__root.help())
                continue

            readline.add_history(line)
            self.execute(line)

    def __print_history(self):
        hi_len = readline.get_current_history_length()
        offset = hi_len - 10 if hi_len > 10 else 0
        for i in range(offset, hi_len):
            item = readline.get_history_item(i)
            if item:
                print(item)

    def start(self, args):
        histfile = os.path.join(os.path.expanduser("~"), ".{}_history".format(self.__name))
        try:
            readline.read_history_file(histfile)
            h_len = readline.get_history_length()
        except FileNotFoundError:
            open(histfile, 'wb').close()
            h_len = 0
        atexit.register(save_history, h_len, histfile)

        readline.parse_and_bind('tab: complete')
        readline.set_completer(self.complete)
        readline.set_completer_delims(self.__delims)
        try:
            self.input_loop()
        except (KeyboardInterrupt, EOFError):
            print()
            sys.exit(-1)

    def complete(self, text, state):
        try:
            if state == 0:
                self.matching_words = []
                origline = readline.get_line_buffer()
                endswith_space = origline.endswith(' ')
                if endswith_space:
                    need_complete = '' 
                    status, command, args = self.parse_command(origline)
                else:
                    words = origline.split()
                    need_complete = words[-1] if words else ''
                    status, command, args = self.parse_command(' '.join(words[:-1]))

                logging.debug("command:%s, args:%s", command.name(), ' '.join(args))
                if status == False:
                    return None
                logging.debug("args:%s, text:%s", ' '.join(args), need_complete)
                self.matching_words = command.matching_words(args, need_complete)
                logging.debug("matching words:%s", ' '.join(self.matching_words))
                if len(self.matching_words) == 1:
                    return self.matching_words[0] + ' '

            try:
                return self.matching_words[state]
            except IndexError:
                return None
        except:
            print(traceback.format_exc())

    def parse_command(self, line):
        words = line.split()
        command = self.__root
        index = 0
        try:
            for word in words:
                if not word.startswith('-'):
                    child = command.child(word)
                    if not child:
                        return False, command, words[index:]
                    index += 1
                    command = child
                else:
                    break
        except KeyError:
            pass

        return True, command, words[index:]
