import voicemeeterlib


class Observer:
    def __init__(self, vm):
        self.vm = vm

    def on_update(self, subject):
        if subject == "pdirty":
            print("pdirty!")
        if subject == "mdirty":
            print("mdirty!")
        if subject == "ldirty":
            info = (
                f"[{self.vm.bus[0]} {self.vm.bus[0].levels.isdirty}]",
                f"[{self.vm.bus[1]} {self.vm.bus[1].levels.isdirty}]",
                f"[{self.vm.bus[2]} {self.vm.bus[2].levels.isdirty}]",
                f"[{self.vm.bus[3]} {self.vm.bus[3].levels.isdirty}]",
                f"[{self.vm.bus[4]} {self.vm.bus[4].levels.isdirty}]",
            )
            print(" ".join(info))


def main():
    with voicemeeterlib.api(kind_id) as vm:
        obs = Observer(vm)
        vm.subject.add(obs)

        while cmd := input("Press <Enter> to exit\n"):
            if not cmd:
                break


if __name__ == "__main__":
    kind_id = "banana"

    main()
