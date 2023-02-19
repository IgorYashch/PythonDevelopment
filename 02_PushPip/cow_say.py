import cowsay
import argparse

PRESETS = 'bdgpstwy'


def main():
    cowparser = argparse.ArgumentParser(description='My cowsay program')

    cowparser.add_argument('message', nargs='*')
    cowparser.add_argument('-e', '--eye_string', dest='eyes', default=cowsay.Option.eyes)
    cowparser.add_argument('-T', '--tongue_string', dest='tongue', default=cowsay.Option.tongue)
    cowparser.add_argument('-W', '--column', dest='width', default=40, type=int)
    cowparser.add_argument('-n', action='store_false', dest='wrap_text')
    cowparser.add_argument('-f', '--cowfile')
    cowparser.add_argument('-l', '--list', action='store_true')
    
    for c in PRESETS:
        cowparser.add_argument(f'-{c}', action='store_true')
    
    cowargs = cowparser.parse_args()
    
    preset = ''.join([c for c in PRESETS if vars(cowargs)[c]])
    
    if cowargs.list:
        print(', '.join(cowsay.list_cows()))
    else:
        message = ' '.join(cowargs.message) or input()
        print(cowsay.cowsay(
            message,
            eyes=cowargs.eyes,
            tongue=cowargs.tongue,
            width=cowargs.width,
            wrap_text=cowargs.wrap_text,
            preset=preset,
            cowfile=cowargs.cowfile
        ))


if __name__ == '__main__':
    main()