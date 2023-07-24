from story_class_structures import *
from contextlib import contextmanager
import sys, os
import unittest

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

x_txt_extender = lambda chr_txt : "\n".join(chr_txt)
expected_maker = lambda chr_txt,scn_txt : f'CHARACTERS\n{x_txt_extender(chr_txt)}\nSCENES\n{x_txt_extender(scn_txt)}'
scene_maker = lambda id,body, options : ["----",id]+body+["===="]+options+["----"]
flatten = lambda outer : [item for inner in outer for item in inner]
scenes_maker = lambda all_scene : flatten([scene_maker(scene[0],scene[1],scene[2])+['\n'] for scene in all_scene])[:-1]

class test_Character_checks(unittest.TestCase):
    def testChecks(self):
        attribs_skills = ["acumen","body","charm","diplomacy","investigation","medicine","language","acrobatics", "craft"]
        test_stats = ["test humanoid","A4 B1 C2","Di In Me La Ac* Cr"]
        test_stats_revised = ["test humanoid2","A4 B1 C2","Di In Me* La Ac Cr"]
        expected_bonus = [4,1,2,2,4,4,2,1+2,1]
        expected_bonus_revised = [4,1,2,2,4,4+2,2,1,1]
        difficulties = [2]
        expected_results = ["+","+","++","-","-","--"]
        get_overrides = lambda bonus, diff : [diff-bonus,diff-bonus+2,diff-bonus+3,diff-bonus-1,diff-bonus-3,diff-bonus-4]
        test_describe = lambda tried,diff,override : f'Character(test_data).make_check({tried,diff,override})'
        try:
            test_person = Character(test_stats)
            test_person_2 = Character(test_stats_revised)
            success = True
            msg = None
        except Exception as e:
            success = False
            msg = f'tried to instantiate a character with the data {test_stats} but it failed'
        self.assertTrue(success,msg)
        for check_id in range(len(attribs_skills)):
            check = attribs_skills[check_id]
            for diff_id in range(len(difficulties)):
                this_diff = difficulties[diff_id]
                overs = get_overrides(expected_bonus[check_id],this_diff)
                for over_id in range(len(overs)):
                    over = overs[over_id]
                    with self.subTest(msg=test_describe(check,this_diff,over)):
                        try:
                            expected = expected_results[over_id]
                            observed = test_person.make_check(check,this_diff,over)
                            if expected == observed:
                                success = True
                                msg = ""
                            else:
                                success = False
                                msg = test_describe(check,this_diff,over)+f'\n\nExpected: {expected} \n but got \n {observed}'
                        except Exception as e:
                            success = False
                            msg = test_describe(check,this_diff,over)+f'\n\nExpected: {expected} \n however an error was raised as below \n {e.__class__.__name__}({str(e)})'
                        self.assertTrue(success,"\n\nWe ran the function as below\n"+msg)

        this_skill = "acrobatics"
        this_diff =  6
        this_over = 5
        this_expect = "+"
        with self.subTest(test_describe(this_skill,this_diff,this_over)):
            try:
                observed = test_person_2.make_check(this_skill,this_diff,this_over)
                if this_expect == observed:
                    success = True
                    msg = ""
                else:
                    success = False
                    msg = test_describe(this_skill,this_diff,this_over)+f'\n\nExpected: {this_expect} \n but got \n {observed}'
            except Exception as e:
                success = False
                msg = test_describe(this_skill,this_diff,this_over)+f'\n\nExpected: {this_expect} \n however an error was raised as below \n {e.__class__.__name__}({str(e)})'
            self.assertTrue(success,"\n\nWe ran the function as below\n"+msg)

if __name__=="__main__":
    unittest.main()
