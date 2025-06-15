import time

import voicemeeterlib

def main():
    KIND_ID = 'banana'

    with voicemeeterlib.api(KIND_ID) as vm:
        vm.bus[0].eq.on = True
        vm.bus[0].eq.channel[0].cell[0].on = True
        vm.bus[0].eq.channel[0].cell[0].f = 500
        vm.bus[0].eq.channel[0].cell[0].type = 3 # Should correspond to LPF

        time.sleep(3)
        vm.bus[0].eq.on = False
        vm.bus[0].eq.channel[0].cell[0].on = False
        vm.bus[0].eq.channel[0].cell[0].f = 50
        vm.bus[0].eq.channel[0].cell[0].type = 0

if __name__ == '__main__':
    main()