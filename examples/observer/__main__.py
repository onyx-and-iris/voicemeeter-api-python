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
                "levels changed:",
                f"[strip 0 {self.vm.strip[0].levels.is_updated}]",
                f"[strip 1 {self.vm.strip[1].levels.is_updated}]",
                f"[strip 2 {self.vm.strip[2].levels.is_updated}]",
                f"[strip 3 {self.vm.strip[3].levels.is_updated}]",
                f"[strip 4 {self.vm.strip[4].levels.is_updated}]",
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
