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

        try:
            while True:
                cmd = input("Press Return to exit\n")
                if not cmd:
                    break
        except KeyboardInterrupt as e:
            SystemExit(e)


if __name__ == "__main__":
    kind_id = "banana"

    main()
