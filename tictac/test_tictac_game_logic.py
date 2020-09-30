
import sys
print(sys.path)
print()
import unittest
from tictac_game_logic import add_o_if_two_in_row

class Test_tictac_game_logic(unittest.TestCase):

    def test_add_o_if_two_in_row(self):
        buttons = ['X', '_', 'O',
                   'X', 'O', '_',
                   '_', '_', '_']
        text = 'O'
        res = add_o_if_two_in_row(buttons, text)
        res_buttons = ['X', '_', 'O',
                       'X', 'O', '_',
                       'O', '_', '_']
        self.assertEqual(res, res_buttons)


    def test2_add_o_if_two_in_row(self):
        buttons = ['X', '_', 'O',
                   'X', '_', 'O',
                   '_', '_', '_']
        text = 'O'
        res = add_o_if_two_in_row(buttons, text)
        res_buttons = ['X', '_', 'O',
                       'X', '_', 'O',
                       '_', '_', 'O']
        self.assertEqual(res, res_buttons)


    def test3_add_o_if_two_in_row(self):
        buttons = ['X', '_', 'O',
                   'X', '_', '_',
                   '_', '_', '_']
        text = 'X'
        res = add_o_if_two_in_row(buttons, text)
        res_buttons = ['X', '_', 'O',
                       'X', '_', '_',
                       'O', '_', '_']
        self.assertEqual(res, res_buttons)


    def test4_add_o_if_two_in_row(self):
        buttons = ['_', '_', 'O',
                   '_', 'X', '_',
                   '_', 'O', 'X']
        text = 'X'
        res = add_o_if_two_in_row(buttons, text)
        res_buttons = ['O', '_', 'O',
                       '_', 'X', '_',
                       '_', 'O', 'X']
        self.assertEqual(res, res_buttons)
    

    def test5_add_o_if_two_in_row(self):
        buttons = ['O', '_', '_',
                   'O', 'X', '_',
                   'X', '_', '_']
        text = 'X'
        res = add_o_if_two_in_row(buttons, text)
        res_buttons = ['O', '_', 'O',
                       'O', 'X', '_',
                       'X', '_', '_']
        self.assertEqual(res, res_buttons)
    

    def test6_add_o_if_two_in_row(self):
        buttons = ['X', 'X', 'O',
                   'X', 'X', 'O',
                   'O', '_', 'O']
        text = 'X'
        res = add_o_if_two_in_row(buttons, text)
        res_buttons = ['X', 'X', 'O',
                       'X', 'X', 'O',
                       'O', 'O', 'O']
        self.assertEqual(res, res_buttons)
    

    def test7_add_o_if_two_in_row(self):
        buttons = ['X', 'O', 'O',
                   'X', 'O', '_',
                   '_', '_', '_']
        text = 'O'
        res = add_o_if_two_in_row(buttons, text)
        res_buttons = ['X', 'O', 'O',
                       'X', 'O', '_',
                       '_', 'O', '_']
        self.assertEqual(res, res_buttons)


    def test8_add_o_if_two_in_row(self):
        buttons = ['X', '_', 'O',
                   'X', '_', 'O',
                   'O', '_', 'O']
        text = 'O'
        res = add_o_if_two_in_row(buttons, text)
        res_buttons = ['X', '_', 'O',
                       'X', '_', 'O',
                       'O', 'O', 'O']
        self.assertEqual(res, res_buttons)





if __name__ == "__main__":
    unittest.main()