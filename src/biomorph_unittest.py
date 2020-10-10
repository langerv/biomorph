import unittest
from biomorph import Biomorph
from character import Character
from aptitude import PhysicalAptitudes, PsychicalAptitudes

class TestBiomorph(unittest.TestCase):

    def test_BaseAptitude(self):
        bm = Biomorph()
        # test physical aptiude
        bm.set_aptitude(PhysicalAptitudes.MOVE, 1)
        ap = bm.get_aptitude(PhysicalAptitudes.MOVE)
        self.assertEqual(ap.Value, 1)
        # test psychical aptiude
        bm.set_aptitude(PsychicalAptitudes.INTL, 2)
        ap = bm.get_aptitude(PsychicalAptitudes.INTL)
        self.assertEqual(ap.Value, 2)

    def test_MorphAptitude(self):
        # create a biomorphcls
        bm = Biomorph()
        bm.set_aptitude(PhysicalAptitudes.PERC, 1)
        bm.set_aptitude(PhysicalAptitudes.MOVE, 1)
        bm.set_aptitude(PhysicalAptitudes.CONS, 1)
        bm.set_aptitude(PsychicalAptitudes.INTL, 1)
        bm.set_aptitude(PsychicalAptitudes.CHAR, 1)
        bm.set_aptitude(PsychicalAptitudes.ETHQ, 1)

        # add a target character
        morph_target = Character()
        morph_target.set_aptitude(PhysicalAptitudes.PERC, 5)
        morph_target.set_aptitude(PhysicalAptitudes.MOVE, 5)
        morph_target.set_aptitude(PhysicalAptitudes.CONS, 5)
        morph_target.set_aptitude(PsychicalAptitudes.INTL, 5)
        morph_target.set_aptitude(PsychicalAptitudes.CHAR, 5)
        morph_target.set_aptitude(PsychicalAptitudes.ETHQ, 5)

        # do a morph
        morph_cost = bm.morph_cost(morph_target)
        if morph_cost is not None:
            print(f"\nMorph cost = {morph_cost:.2f}")

        if bm.morph(morph_target) is False:
            print("Invalid morph!")
        else:
            for _ in range(100):
                bm.update()
                aptitudes_string = []
                for key, ap in bm.Aptitudes.items():
                    aptitudes_string.append("{} = {:.1f}".format(key.name, ap.Value))
                print(', '.join(aptitudes_string))

if __name__ == '__main__':
	unittest.main()
