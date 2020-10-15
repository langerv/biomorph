import unittest
from metabolism import Metabolism
import numpy as np
import matplotlib.pyplot as plt

MB_EINIT = 1000              # initial energy
MB_EMIN = 600                # basal energy = minimum energy before to trigger the hungry signal
MB_RATE = 1.0                # basal burn rate
MB_PERI = 0.1               # metabolism's peristalsis

MB_EFOOD = 500               # enery per food ate
MB_EMOVE = 10                 # energy burnt per move

'''
MB_TICK = 0.1                # seconds
MB_FOOD_TICK = MB_TICK * 600 # seconds
MB_MOVE_TICK = MB_TICK * 10  # seconds
'''

class TestMetabolism(unittest.TestCase):

    def test_Metabolism(self):
        mb = Metabolism(MB_EINIT, MB_EMIN, MB_RATE, MB_PERI)
#        mb.ingest(MB_EFOOD)
        energy = []
        stomach = []
        for i in range(10000):
            energy.append(mb.Energy)
            stomach.append(mb.Stomach)

            if i % 10 == 0:
                mb.digest()

            '''
            if i % 200 == 0:
                mb.burn(MB_EMOVE)

            if mb.Hungry and i % 5000 == 0:
                mb.ingest(MB_EFOOD)
            '''

        x = np.arange(len(energy))
        y1 = np.array(energy)
        y2 = np.array(stomach)
        plt.plot(x, y1, label='Energy')
        plt.plot(x, y2, label='Stomach')
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
	unittest.main()
