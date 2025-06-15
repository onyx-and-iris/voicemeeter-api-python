import time

import voicemeeterlib

# Creates an array of channels you want to edit
# s is the channel to start on, n is how many channels to edit
def create_channel_array(s, n):
    return list(range(s, s+n))

def main():
    KIND_ID = 'banana'

    with voicemeeterlib.api(KIND_ID) as vm:
        print( 'Check getting values' )
        print( f'Bus[0].EQ.on: {vm.bus[0].eq.on}')
        print( f'Bus[0].EQ.channel[0].cell[0].on: {vm.bus[0].eq.channel[0].cell[0].on}')

        print( 'Check sending commands (should affect your VM Banana window)')
        channels_idx = create_channel_array(0, 2)
        vm.bus[0].eq.on = True
        vm.bus[0].eq.ab = 0 # corresponds to A EQ memory slot
        vm.bus[0].mute = False
        for i in channels_idx:
            vm.bus[0].eq.channel[i].cell[0].on = True
            vm.bus[0].eq.channel[i].cell[0].f = 500
            vm.bus[0].eq.channel[i].cell[0].gain = -10
            vm.bus[0].eq.channel[i].cell[0].type = 3 # Should correspond to LPF
            vm.bus[0].eq.channel[i].cell[0].q = 10

        time.sleep(3)
        vm.bus[0].eq.on = False
        for i in channels_idx:
            vm.bus[0].eq.channel[i].cell[0].on = False
            vm.bus[0].eq.channel[i].cell[0].f = 50
            vm.bus[0].eq.channel[i].cell[0].gain = 0
            vm.bus[0].eq.channel[i].cell[0].type = 0
            vm.bus[0].eq.channel[i].cell[0].q = 3

if __name__ == '__main__':
    main()