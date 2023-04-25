import unittest
from edax_wrapper.edax import Edax

edax_binary = r'G:\edax-ms-windows\edax-4.4'

class EdaxChooseMoveTest(unittest.TestCase):

    def test_pass(self):
        engine = Edax(edax_binary, level=60)
        pos = 'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOX- X'

        moves = engine.choose_move(pos)

        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0], 64)

    def test_game_over(self):
        engine = Edax(edax_binary, level=60)
        pos = 'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO-- X'

        moves = engine.choose_move(pos)

        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0], 64)


if __name__ == '__main__':
    unittest.main(verbosity=2)
