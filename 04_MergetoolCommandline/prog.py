import cmd
import readline
import shlex

import cowsay

class CmdLine(cmd.Cmd):
    def do_cowsay(self, arg):
        cmd = shlex.split(arg)
        params_names =  {'--message': 'message', '--cow': 'cow', '--eyes': 'eyes', '--tongue': 'tongue'}
        params_vals =  {'message': '', 'cow': 'default', 'eyes': 'oo', 'tongue': '  '}
        i = 0
        while i < len(cmd):
            if cmd[i] in params_names and i < len(cmd) - 1 and cmd[i + 1] not in params_names:
                params_vals[params_names[cmd[i]]] = cmd[i + 1]
                i += 2
            else:
                assert KeyError('There is no such argument')
        print(cowsay.cowsay(**params_vals))


if __name__ == '__main__':
    cmd_line = CmdLine()
    cmd_line.cmdloop()