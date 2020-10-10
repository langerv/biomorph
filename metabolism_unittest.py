import unittest
#import time
#from datetime import timedelta
#from timer import Timer
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

        '''
        def move(e):
            mb.burn(e)
            print("burning {} energy".format(e))

        def eat(e):
            mb.ingest(e)
            print("eating {} energy".format(e))

        def execute():
            mb.digest()
            energy.append(mb.Energy)
            print("Energy = {:.0f}, Stomach = {:.0f}, Capacity = {:.1f}, Hungry = {}".format(
                mb.Energy, 
                mb.Stomach, 
                mb.Capacity,
                mb.Hungry))

        timer = Timer()
        timer.add_task(interval=timedelta(seconds=MB_TICK), execute=execute)
        timer.add_task(interval=timedelta(seconds=MB_FOOD_TICK), execute=eat, e=MB_EFOOD)
        timer.add_task(interval=timedelta(seconds=MB_MOVE_TICK), execute=move, e=MB_EMOVE)
        timer.start()

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                timer.stop()
                break
        '''

if __name__ == '__main__':
	unittest.main()
