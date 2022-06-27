import voicemeeterlib


class Observer:
    def __init__(self, vm):
        self.vm = vm

    def on_update(self, subject):
        print(subject)


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
