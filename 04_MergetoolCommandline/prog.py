import cmd
import readline
import shlex

import cowsay

class CmdLine(cmd.Cmd):
    def _print_cow(self, args, print_function):
        args_vals = shlex.split(args)
        params =  ['message',  'cow', 'eyes', 'tongue']
                #    ': cowsay.Option.eyes, 'tongue': cowsay.Option.tongue}
        default = ['default', cowsay.Option.eyes, cowsay.Option.tongue]
        
        args_vals[len(args_vals):] = default[len(args_vals) - 1:]
        pairs = dict(zip(params, args_vals))
        print(pairs)
        print(print_function(**pairs))

    
    def do_cowsay(self, args):
        '''Similar to the cowsay command. Parameters are listed with their
corresponding options in the cowsay command. Returns the resulting cowsay
string.
cowsay <message> [<cow> [<eyes> [tongue]]
'''
        print_function = cowsay.cowsay
        self._print_cow(args, print_function)

    
    def do_cowthink(self, args):
        '''Similar to the cowthink command. Parameters are listed with their
corresponding options in the cowthink command. Returns the resulting
cowthink string.
cowthink <message> [<cow> [<eyes> [tongue]]]
'''
        print_function = cowsay.cowthink
        self._print_cow(args, print_function)

        
    def do_list_cows(self, args):
        """Lists all available cow file names in your given directory
(With empty string print default available 'cows')
"""
        if param := shlex.split(args):   
            print(*cowsay.list_cows(param[0]), sep=', ')
        else:
            print(*cowsay.list_cows(), sep=', ')
    
    
    def do_make_bubble(self, arg):
        """
Set text inside a bubble
"""
        if param := shlex.split(arg):
            print(cowsay.make_bubble(text=param[0]))


    def _print_complete(self, prefix, line, start, end):
        if (l := len(shlex.split(line))) == 3:
            preds = cowsay.list_cows()
        elif l == 4:
            preds = ['00', '%%', '!!', '@@', 'xx', 'XX', 'oo']
        elif l == 5:
            preds = ['\/', '--', '__',  '**', '..'] 
        return [x for x in preds if x.startswith(prefix)]
    
    
    def complete_cowsay(self, *args):
        return self._print_complete(*args)

    
    def complete_cowthink(self, *args):
        return self._print_complete(*args)                

if __name__ == '__main__':
    cmd_line = CmdLine()
    cmd_line.cmdloop()