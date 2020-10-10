from aptitude import AptitudeBase


class CharacterAptitude(AptitudeBase):
    def update(self):
        pass

class Character():
    def __init__(self):
        self._aptitudes = {} # characters have aptitudes

    @property
    def Aptitudes(self):
        return self._aptitudes

    def get_aptitude(self, key):
        if key in self._aptitudes:
            return self._aptitudes[key]
        else:
            None

    def set_aptitude(self, key, value):
        self._aptitudes[key] = CharacterAptitude(value)

    def update(self):
        for apt in self._aptitudes.values():
            apt.update()
