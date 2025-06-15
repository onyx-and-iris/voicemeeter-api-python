import time

import voicemeeterlib


def main():
    KIND_ID = 'banana'
    BUS_INDEX = 0  # Index of the bus to edit, can be changed as needed
    CHANNEL_INDEX = 0  # Index of the channel to edit, can be changed as needed

    with voicemeeterlib.api(KIND_ID) as vm:
        print(f'Bus[{BUS_INDEX}].EQ.on: {vm.bus[BUS_INDEX].eq.on}')
        print(
            f'Bus[{BUS_INDEX}].EQ.channel[{CHANNEL_INDEX}].cell[0].on: {vm.bus[BUS_INDEX].eq.channel[CHANNEL_INDEX].cell[0].on}'
        )

        print('Check sending commands (should affect your VM Banana window)')

        vm.bus[BUS_INDEX].eq.on = True
        vm.bus[BUS_INDEX].eq.ab = 0  # corresponds to A EQ memory slot
        vm.bus[BUS_INDEX].mute = False

        for j, cell in enumerate(vm.bus[BUS_INDEX].eq.channel[CHANNEL_INDEX].cell):
            cell.on = True
            cell.f = 500
            cell.gain = -10
            cell.type = 3  # Should correspond to LPF
            cell.q = 10

            print(
                f'Channel {CHANNEL_INDEX}, Cell {j}: on={cell.on}, f={cell.f}, type={cell.type}, gain={cell.gain}, q={cell.q}'
            )

            time.sleep(1)  # Sleep to simulate processing time

            cell.on = False
            cell.f = 50
            cell.gain = 0
            cell.type = 0
            cell.q = 3

            print(
                f'Channel {CHANNEL_INDEX}, Cell {j}: on={cell.on}, f={cell.f}, type={cell.type} , gain={cell.gain}, q={cell.q}'
            )

        vm.bus[BUS_INDEX].eq.on = False


if __name__ == '__main__':
    main()
