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
story_data = {
    "scenes":[
        ["S",["body of scene","next line of body"],["1. [diplomacy 10] convince +2 -1 --10","2. do not try +5","3. [charm 0] be a human +1 ++4 -10"]],
        ["2",["oh that's good"],["1. [craft 5] build a thing +3 --10","2. [body 4] you are just a tough dude +1 -E~1"]],
        ["10",["oh no bad stuff is about to happen because of that"],["1. [language 1] use your words +E*1","2. [acumen 2] think carefully -E~1 +E*1","3. [medicine 6] give them a bandaid +E*2 --E~1","4. [investigation 5] can you find the thing? +E*1 -E~2","5. [acrobatics 4] do a backflip -E~2 +E*2","6. [craft 3] make a paper plane --E~1 -E~2 ++E*1"]],
        ["1",["scene 1 here"],["1. go to two --2"]],
        ["3",["scene 3 here"],["1. go to four -4"]],
        ["4",["scene 4 here"],["1. go to five ++5"]],
        ["5",["scene 5 here"],["1. [body 2] good or bad 1 +E*1 -E~1","2. [charm 2] good or bad 2 +E*2 -E~2"]],
        ["E~1",["bad ending 1"],[]],
        ["E~2",["bad ending 2"],[]],
        ["E*1",["good ending 1"],[]],
        ["E*2",["good ending 2"],[]],
    ],
    "scene_user_print":{
        "S":'Scene S\nbody of scene\nnext line of body\n====\n1. convince\n2. do not try\n3. be a human\n----',
        "2":"Scene 2\noh that's good\n====\n1. build a thing\n2. you are just a tough dude\n----",
        "10":'Scene 10\noh no bad stuff is about to happen because of that\n====\n1. use your words\n2. think carefully\n3. give them a bandaid\n4. can you find the thing?\n5. do a backflip\n6. make a paper plane\n----',
        "1":'Scene 1\nscene 1 here\n====\n1. go to two\n----',
        "3":'Scene 3\nscene 3 here\n====\n1. go to four\n----',
        "4":'Scene 4\nscene 4 here\n====\n1. go to five\n----',
        "5":'Scene 5\nscene 5 here\n====\n1. good or bad 1\n2. good or bad 2\n----',
        "E~1":'Scene E~1\nbad ending 1\n====\n----',
        "E~2":'Scene E~2\nbad ending 2\n====\n----',
        "E*1":'Scene E*1\ngood ending 1\n====\n----',
        "E*2":'Scene E*2\ngood ending 2\n====\n----'
     },
    "expected_scn":[
        "S > [1. diplomacy10 +2 -1 --10] [2. +5] [3. charm0 ++4 +1 -10]",
        "2 > [1. craft5 +3 --10] [2. body4 +1 -E~1]",
        "10 > [1. language1 +E*1] [2. acumen2 +E*1 -E~1] [3. medicine6 +E*2 --E~1] [4. investigation5 +E*1 -E~2] [5. acrobatics4 +E*2 -E~2] [6. craft3 ++E*1 -E~2 --E~1]",
        "1 > [1. --2]",
        "3 > [1. -4]",
        "4 > [1. ++5]",
        "5 > [1. body2 +E*1 -E~1] [2. charm2 +E*2 -E~2]",
        "E~1 >",
        "E~2 >",
        "E*1 >",
        "E*2 >",
    ],
    "characters":[
        ["Marian Croak","A4 B1 C2","Di In* Me La Ac Cr"],
        ["Hero","A2 B3 C2","Di In Me La Ac* Cr"],
        ["doctorb","A3 B3 C1","Di In Me* La Ac Cr"]
    ],
    "chr_strs":[
        "Marian Croak [A4 B1 C2] is proficient in investigation",
        "Hero [A2 B3 C2] is proficient in acrobatics",
        "doctorb [A3 B3 C1] is proficient in medicine"
    ]
}
get_scn_data = lambda scn_count : story_data["scenes"][:scn_count]
chr_joiners = lambda characters : flatten([char + ["----"] for char in characters])[:-1]
get_chr_data = lambda chr_count : chr_joiners(story_data["characters"][:chr_count])
get_exp_scn = lambda scn_count : story_data["expected_scn"][:scn_count]
get_exp_chr = lambda chr_count : story_data["chr_strs"][:chr_count]
class test_Story(unittest.TestCase):
    def testOneCharOneSceneExtensible(self,chr_count = 1,scn_count = 1):
        scene_data_base = get_scn_data(scn_count)
        chr_data = get_chr_data(chr_count)
        scene_data = scenes_maker(scene_data_base)
        str_expect = expected_maker(get_exp_chr(chr_count),get_exp_scn(scn_count))
        msg_base = f'\n\nattempted to create a Story with {scn_count} scene(s) and {chr_count} character(s)\n\nExpected str(Story(input_data)) would be as below\n{str_expect}\n\n'
        try:
            S = Story(scene_data,chr_data)
            observed = str(S)
            if observed == str_expect:
                success = True
                msg = ""
            else:
                success = False
                msg = msg_base+f'however we got as below\n{observed}'
        except Exception as e:
            success = False
            msg = msg_base+f'however the error below was raised\n{e.__class__.__name__}({str(e)})'
        self.assertTrue(success,msg)
    def testThreeCharOneScene(self):
        self.testOneCharOneSceneExtensible(chr_count=3)
    def testOneCharTwoScene(self):
        self.testOneCharOneSceneExtensible(scn_count=2)
    def testManyCharManyScene(self):
        self.testOneCharOneSceneExtensible(chr_count=3,scn_count=11)
    def testSceneNum(self):
        scene_data_base = get_scn_data(1)
        chr_data = get_chr_data(1)
        scene_data = scenes_maker(scene_data_base)
        str_expect = "S"
        msg_base = f'\n\nattempted to create a Story with 1 scene(s) and 1 character(s)\nExpected to start at Scene S\n\n'
        try:
            S = Story(scene_data,chr_data)
            observed = S.get_scene_id()
            if observed == str_expect:
                success = True
                msg = ""
            else:
                success = False
                msg = msg_base+f'however the scene currently at is as below\n{observed}'
        except Exception as e:
            success = False
            msg = msg_base+f'however the error below was raised\n{e.__class__.__name__}({str(e)})'
        self.assertTrue(success,msg)

get_scene_pres = lambda scene_id : story_data["scene_user_print"][scene_id]
scene_motion_data = {
    "scene_data":scenes_maker(get_scn_data(11)),
    "char_data":get_chr_data(1),
    "char_base_bonus":["A4 B1 C2 Di2 In6 Me4 La2 Ac1 Cr1"],
    "calls_str": [
        "test = Story(test_data)\noutput = test.show_current_scene()\nassert output == expected",
        "test = Story(test_data)\ntest.select_option(1,8)\noutput = test.show_current_scene()\nassert output == expected",
        "test = Story(test_data)\ntest.select_option(1,11)\noutput = test.show_current_scene()\nassert output == expected",
        "test = Story(test_data)\ntest.select_option(1,7)\noutput = test.show_current_scene()\nassert output == expected",
        "test = Story(test_data)\ntest.select_option(1,3)\noutput = test.show_current_scene()\nassert output == expected",
        "test = Story(test_data)\ntest.select_option(2,None)\noutput = test.show_current_scene()\nassert output == expected",
        "test = Story(test_data)\ntest.select_option(2,None)\ntest.select_option(2,0)\noutput = test.show_current_scene()\nassert output == expected",
        "test = Story(test_data)\ntest.select_option(2,None)\ntest.select_option(2,0)\ntest.select_option(1,None)\noutput = test.show_current_scene()\nassert output == expected",
        "test = Story(test_data)\ntest.select_option(1,3)\ntest.select_option(6,5)\noutput = test.show_current_scene()\nassert output == expected",
        "test = Story(test_data)\ntest.select_option(1,3)\ntest.select_option(2,-6)\noutput = test.show_current_scene()\nassert output == expected",
        "test = Story(test_data)\ntest.select_option(1,8)\ntest.select_option(1,3)\noutput = test.show_current_scene()\nassert output == expected",
    ],
    "run_args":[
        [],
        [[1,8]],
        [[1,11]],
        [[1,7]],
        [[1,3]],
        [[2,None]],
        [[2,None],[2,0]],
        [[2,None],[2,0],[1,None]],
        [[1,3],[6,5]],
        [[1,3],[2,-6]],
        [[1,8],[1,3]],
    ],
    "expected": [
        get_scene_pres("S"),
        get_scene_pres("2"),
        get_scene_pres("2"),
        get_scene_pres("1"),
        get_scene_pres("10"),
        get_scene_pres("5"),
        get_scene_pres("E*2"),
        None,
        get_scene_pres("E*1"),
        get_scene_pres("E~1"),
        get_scene_pres("10"),
    ],
    "errors":[
        None,None,None,None,None,None,None,StopIteration("the game is over"),None,None,None
    ]
}


class test_Story_SceneDisplaySelect(unittest.TestCase):
    def setup_class_data(self,case):
        scene_data = scene_motion_data["scene_data"]
        chr_data = scene_motion_data["char_data"]
        str_expect = scene_motion_data["expected"][case]
        errors_expect = scene_motion_data["errors"][case]
        msg_base = f'\n\nattempted to create a Story with 11 scenes and 1 character\n\nThen ran the functions:\n{scene_motion_data["calls_str"][case]}\n\nExpectation was \n{errors_expect if not errors_expect is None else str_expect}\n\n'
        try:
            S = Story(scene_data,chr_data)
            for instruction in scene_motion_data["run_args"][case]:
                S.select_option(instruction[0],instruction[1])
            observed = S.show_current_scene()
            #put stuff here to display a scene and others to move between them and check the scene number
            if ((observed == str_expect) and (errors_expect is None)):
                success = True
                msg = ""
            else:
                success = False
                msg = msg_base+f'however we got as below\n{observed}'
        except Exception as e:
            failure_msg_wrong_error = msg_base+f'however the error below was raised\n{e.__class__.__name__}({str(e)})'
            if errors_expect is None:
                success = False
                msg = failure_msg_wrong_error
            elif (errors_expect.__class__.__name__ == e.__class__.__name__) and (str(errors_expect) == str(e)):
                success = True
                msg = ""
            else:
                success = False
                msg = failure_msg_wrong_error

        self.assertTrue(success,msg)
    def testBasic(self):
        self.setup_class_data(0)
    def testSelectPlus(self):
        self.setup_class_data(1)
    def testSelectPlusPlusRoundDown(self):
        self.setup_class_data(2)
    def testSelectMinusTop(self):
        self.setup_class_data(3)
    def testSelectMinusMinus(self):
        self.setup_class_data(4)
    def testSelectNoRollOrOverride(self):
        self.setup_class_data(5)
    def testSelectToEnd(self):
        self.setup_class_data(6)
    def testSelectSelectAtEnd(self):
        self.setup_class_data(7)
    def testSelectPlusPlus(self):
        self.setup_class_data(8)
    def testSelectNegNegRoundUp(self):
        self.setup_class_data(9)
    def testSelectMinusRoundDown(self):
        self.setup_class_data(10)

if __name__=="__main__":
    unittest.main()
