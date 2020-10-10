import math
from character import Character
from aptitude import PhysicalAptitudes, PsychicalAptitudes, AptitudeBase

'''
Create biomorph related child classes for aptitudes
'''

class AptitudeMorph(AptitudeBase):
    def __init__(self, value, mu, mu_max, km, ka):
        super().__init__(value)
        self._target_value = value
        self._innate_value = value
        self._last_valid = value
        self._mu = mu
        self._mu_init = mu
        self._mu_max = mu_max
        self._km = km
        self._ka = ka

    @property
    def Morphogen(self):
        return self._mu

    def morph(self, target=0):
        self._target_value = target * self._mu
        self._mu = self._mu + self._km * (self._mu_max - self._mu)

    def update(self):
        self._value = self._value + self._ka * (self._target_value - self._value)

class PhysicalMorph(AptitudeMorph):

    def update(self):
        super().update()
        self._value = max(self._value, self._innate_value)

class PsychicalMorph(AptitudeMorph):

    def update(self):
        value = self._value
        super().update()
        self._value = max(self._value, value)



'''
Biomorph class
'''

class Biomorph(Character):

    '''
    Biomorph Constants
    '''
    MU = 0.75
    MU_MAX = 1.2
    PHY_KM = 0.1
    PHY_KA = 0.01
    PSY_KM = 0.05
    PSY_KA = 0.001
    MORPH_COST_ENERGY = 1000

    def __init__(self):
        super().__init__()
        self._morph_cost = 0

    def set_aptitude(self, key, value):
        if PhysicalAptitudes.has_key(key.name):
            self._aptitudes[key] = PhysicalMorph(
                value, 
                Biomorph.MU, 
                Biomorph.MU_MAX, 
                Biomorph.PHY_KM, 
                Biomorph.PHY_KA)

        elif PsychicalAptitudes.has_key(key.name):
            # Ethique does not morph, so just a regular aptitude
            if key == PsychicalAptitudes.ETHQ:
                super().set_aptitude(key, value)
                return # do not add to morph cost

            else:
                self._aptitudes[key] = PsychicalMorph(
                    value, 
                    Biomorph.MU, 
                    Biomorph.MU_MAX, 
                    Biomorph.PSY_KM, 
                    Biomorph.PSY_KA)

        # recompute morph cost
        self._morph_cost = Biomorph.MORPH_COST_ENERGY / math.sqrt(len(self._aptitudes) * 25)
#        print(f"old: {Biomorph.MORPH_COST_ENERGY / math.sqrt(5*25):0.1f}, new: {self._morph_cost:0.1f}")

    def morph_cost(self, morph_target):
        sum = 0
        for key in self._aptitudes.keys():
            if key == PsychicalAptitudes.ETHQ:
                continue
            morph_target_apt = morph_target.get_aptitude(key)
            if morph_target_apt is None:
                # need to have the same number of aptitudes to succeed
                # example are blts with less or different aptitudes... 
                return None
            diff = morph_target_apt.Value - self._aptitudes[key].Value
            sum += diff * diff

        return math.sqrt(sum) * self._morph_cost # compute and return total morph cost


    def morph(self, morph_target):
        for key, apt in self._aptitudes.items():
            if key == PsychicalAptitudes.ETHQ:
                continue

            morph_target_apt = morph_target.get_aptitude(key)
            if morph_target_apt is None:
                # need to have the same number of aptitudes to succeed
                # example are blts with less or different aptitudes... 
                return False

            apt.morph(morph_target_apt.Value)

        return True
