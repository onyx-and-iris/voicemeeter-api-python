import voicemeeterlib


class ManyThings:
    def __init__(self, vm):
        self.vm = vm

    def things(self):
        self.vm.strip[0].label = "podmic"
        self.vm.strip[0].mute = True
        print(
            f"strip 0 ({self.vm.strip[0].label}) label has been set to {self.vm.strip[0].mute}"
        )

    def other_things(self):
        info = (
            f"bus 3 gain has been set to {self.vm.bus[3].gain}",
            f"bus 4 eq has been set to {self.vm.bus[4].eq}",
        )
        self.vm.bus[3].gain = -6.3
        self.vm.bus[4].eq = True
        print("\n".join(info))


def main():
    with voicemeeterlib.api(kind_id) as vm:
        do = ManyThings(vm)
        do.things()
        do.other_things()

        # set many parameters at once
        vm.apply(
            {
                "strip-2": {"A1": True, "B1": True, "gain": -6.0},
                "bus-2": {"mute": True},
                "button-0": {"state": True},
                "vban-in-0": {"on": True},
                "vban-out-1": {"name": "streamname"},
            }
        )


if __name__ == "__main__":
    kind_id = "banana"

    main()
