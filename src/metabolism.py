import math

""" model constants """

class Metabolism():
    def __init__(self, energy, energy_min, rate, peri):
        self._energy = energy
        self._energy_min = energy_min
        self._rate = rate
        self._peri = peri
        self._stomach = 0

    @property
    def Energy(self):
        return self._energy

    @property
    def Stomach(self):
        return self._stomach

    @property
    def Capacity(self):
        return min(self._energy / self._energy_min, 1)

    @property
    def Hungry(self):
        return (self._energy + self._stomach) < self._energy_min

    def ingest(self, e):
        self._stomach += e

    def digest(self):
        bolus = self._stomach * self._peri
        self._energy = max(self._energy + bolus - self._rate, 0)
        self._stomach = max(self._stomach - bolus, 0)
        return self._energy == 0

    def burn(self, e):
        self._energy = max(self._energy - e , 0)
