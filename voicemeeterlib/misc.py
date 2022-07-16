from .iremote import IRemote


class FX(IRemote):
    @property
    def identifier(self) -> str:
        return "FX"

    @property
    def reverb(self) -> bool:
        return self.getter("reverb.On") == 1

    @reverb.setter
    def reverb(self, val: bool):
        self.setter("reverb.On", 1 if val else 0)

    @property
    def reverb_ab(self) -> bool:
        return self.getter("reverb.ab") == 1

    @reverb_ab.setter
    def reverb_ab(self, val: bool):
        self.setter("reverb.ab", 1 if val else 0)

    @property
    def delay(self) -> bool:
        return self.getter("delay.On") == 1

    @delay.setter
    def delay(self, val: bool):
        self.setter("delay.On", 1 if val else 0)

    @property
    def delay_ab(self) -> bool:
        return self.getter("delay.ab") == 1

    @delay_ab.setter
    def delay_ab(self, val: bool):
        self.setter("delay.ab", 1 if val else 0)
