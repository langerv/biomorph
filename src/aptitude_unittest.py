import unittest
from aptitude import AptitudeBase
from biomorph import PhysicalMorph, PsychicalMorph
import numpy as np
import matplotlib.pyplot as plt

'''
Morphs scenarios
'''
class TestAptitudes(unittest.TestCase):

    def test_Morphogen(self):
        m1 = PhysicalMorph(0, 0.75, 1.2, 0.3, 0)
        m2 = PhysicalMorph(0, 0.75, 1.2, 0.1, 0)
        m3 = PhysicalMorph(0, 0.75, 1.2, 0.05, 0)
        m4 = PhysicalMorph(0, 0.75, 1.2, 0.02, 0)

        x = np.arange(0, 60)
        n = x.shape[0]
        y1 = np.empty(n)
        y2 = np.empty(n)
        y3 = np.empty(n)
        y4 = np.empty(n)

        for i in range(0, n):
            y1[i] = m1.Mu
            y2[i] = m2.Mu
            y3[i] = m3.Mu
            y4[i] = m4.Mu
            m1.morph()
            m2.morph()
            m3.morph()
            m4.morph()

        plt.plot(x, y1, 'ro', label='Km = {}'.format(m1._km))
        plt.plot(x, y2, 'bs', label='Km = {}'.format(m2._km))
        plt.plot(x, y3, 'g^', label='Km = {}'.format(m2._km))
        plt.plot(x, y4, 'yd', label='Km = {}'.format(m3._km))
        plt.legend()
        plt.xlabel("Morphs")
        plt.title(f"Morphogene mu = {m1._mu_init} et muMax = {m1._mu_max}")
        plt.grid(True)
        plt.show()
       
    def test_Morphs(self):
        morphs_1 = [
            (2, 1000),
            (3, 1000),
            (4, 1000), 
            (5, 1000), 
            (2, 1000), 
            (5, 200), 
            (2, 200), 
            (3, 200), 
            (4, 200), 
            (5, 200), 
            (2, 1000), 
            (3, 1000), 
            (4, 1000), 
            (5, 1000), 
            (5, 1000), 
            (5, 1000), 
            (5, 1000), 
            (2, 1000), 
            (3, 1000), 
            (4, 1000),
            (5, 1000)]

        phy = PhysicalMorph(2, 0.75, 1.2, 0.1, 0.01)
        psy = PsychicalMorph(2, 0.75, 1.2, 0.05, 0.001)
        result1 = [phy.Value]
        result2 = [psy.Value]

        for (target, steps) in morphs_1:
            #target, steps = 5, 1000
            phy.morph(target)
            psy.morph(target)
            print(f"Morphogenes: {phy.Mu}, {psy.Mu}")
            for i in range(steps):
                phy.update()
                psy.update()
                result1.append(phy.Value)
                result2.append(psy.Value)

        x = np.arange(len(result1))
        y1 = np.array(result1)
        y2 = np.array(result2)
        plt.plot(x, y1, label='aptitudes physiques')
        plt.plot(x, y2, label='aptitudes psychiques')
        plt.legend()
        plt.xlabel("Morphs scenario")
        plt.grid(True)
        plt.title("Morphogene: Init={}, Max={}\nAptitudes physiques: km={}, ka={}\nAptitudes psychiques: km={}, ka={}".format(
            phy._mu_init, 
            phy._mu_max, 
            phy._km, 
            phy._ka, 
            psy._km, 
            psy._ka
            ))
        plt.show()

    def test_Dimming(self):
        def dimming_init(A, Av, T):
            return 2 * (A - Av) / T

        def dimming(A, k, dt, T):
            return A - k * (dt / T)

        A = 3
        Av = 1
        T = 1000
        plt.title(f"A = {A}, Av = {Av} et T = {T}")
        result = [A]
        Katt = dimming_init(A, Av, T)
        for dt in range(T + int(T/10)):
            A = max (dimming(A, Katt, dt, T), Av)
            result.append(A)

        x = np.arange(len(result))
        y = np.array(result)
        plt.plot(x, y, label='loi d\'affaiblissement')
        plt.legend()
        plt.xlabel("Steps (dt)")
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
	unittest.main()


'''
Sigmoid

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def morphoA(A, T, x):
    return A + (T - A) * sigmoid(x)

def morphoB(A, T, x):
    return A + (T - A) * ( 1 - sigmoid(x))

A = 3
T = 5
dt = (T - A)/T
o1 = 5 * dt
o2 = o1 + 10
x1 = np.linspace(-o1, o2, 30)
x2 = np.linspace(-o2, o1, 30)
ma = np.vectorize(morphoA)
mb = np.vectorize(morphoB)
plt.plot(x1 + o1, ma(A, T, x1), label='loi pour les aptitudes croissantes')
plt.plot(x2 + o2, mb(A, T, x2), label='loi pour les aptitudes decroissantes')
plt.grid(True)
plt.show()
'''
