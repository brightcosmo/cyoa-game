from story_class_structures_chosenchar import *
from story_class_structures import Character
from contextlib import contextmanager
import sys, os
import unittest

get_scene_pres = lambda scene_id : story_data["scene_user_print"][scene_id]
get_scn_data = lambda scn_count : story_data["scenes"][:scn_count]
chr_joiners = lambda characters : flatten([char + ["----"] for char in characters])[:-1]
get_chr_data = lambda chr_count : chr_joiners(story_data["characters"][:chr_count])
get_exp_scn = lambda scn_count : story_data["expected_scn"][:scn_count]
get_exp_chr = lambda chr_count : story_data["chr_strs"][:chr_count]
scene_maker = lambda id,body, options : ["----",id]+body+["===="]+options+["----"]
flatten = lambda outer : [item for inner in outer for item in inner]
scenes_maker = lambda all_scene : flatten([scene_maker(scene[0],scene[1],scene[2])+['\n'] for scene in all_scene])[:-1]
make_char_class = lambda char_num : Character(story_data["characters"][char_num])
story_data = {
    "scenes":[
        ["S",["{C2} and {C1} are really cool dudes","{C3} not so much"],["1. [diplomacy 10] {C2} must convince +2 -1 --10","2. do not try +5","3. [charm 0] {C1} must be a human to {C2} +1 ++4 -10"]],
        ["2",["oh that's good {C2} knows their stuff"],["1. [craft 5] {C1} build a thing +3 --10","2. [body 4] you are just a tough dude +1 -E~1"]],
        ["10",["oh no bad stuff is about to happen because of that"],["1. [language 1] use your words +E*1","2. [acumen 2] think carefully -E~1 +E*1","3. [medicine 6] give them a bandaid +E*2 --E~1","4. [investigation 5] can you find the thing? +E*1 -E~2","5. [acrobatics 4] do a backflip -E~2 +E*2","6. [craft 3] make a paper plane --E~1 -E~2 ++E*1"]],
        ["1",["scene 1 here"],["1. [language 3] {C1} communicate a need to XYZ +4 --2"]],
        ["3",["scene 3 here"],["1. go to four -4"]],
        ["4",["scene 4 here"],["1. go to five ++5"]],
        ["5",["scene 5 here"],["1. [body 2] good or bad 1 +E*1 -E~1","2. [charm 2] good or bad 2 +E*2 -E~2"]],
        ["E~1",["bad ending 1"],[]],
        ["E~2",["bad ending 2"],[]],
        ["E*1",["good ending 1"],[]],
        ["E*2",["good ending 2"],[]],
    ],
    "scene_user_print":{
        "S":'Scene S\nstaying put for 15 years to claim adverse possession and a flailing set of limbs are really cool dudes\ncrocs (the shoe) not so much\n====\n1. staying put for 15 years to claim adverse possession must convince\n2. do not try\n3. a flailing set of limbs must be a human to staying put for 15 years to claim adverse possession\n----',
        "2":"Scene 2\noh that's good staying put for 15 years to claim adverse possession knows their stuff\n====\n1. a flailing set of limbs build a thing\n2. you are just a tough dude\n----",
        "10":'Scene 10\noh no bad stuff is about to happen because of that\n====\n1. use your words\n2. think carefully\n3. give them a bandaid\n4. can you find the thing?\n5. do a backflip\n6. make a paper plane\n----',
        "1":'Scene 1\nscene 1 here\n====\n1. a flailing set of limbs communicate a need to XYZ\n----',
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
        "1 > [1. language3 +4 --2]",
        "3 > [1. -4]",
        "4 > [1. ++5]",
        "5 > [1. body2 +E*1 -E~1] [2. charm2 +E*2 -E~2]",
        "E~1 >",
        "E~2 >",
        "E*1 >",
        "E*2 >",
    ],
    "characters":[
        ["a flailing set of limbs","A4 B1 C2","Di In* Me La Ac Cr"],
        ["staying put for 15 years to claim adverse possession","A2 B3 C2","Di In Me La Ac* Cr"],
        ["crocs (the shoe)","A3 B1 C3","Di In Me* La Ac Cr"]
    ],
    "chr_strs":[
        "a flailing set of limbs [A4 B1 C2] is proficient in investigation",
        "staying put for 15 years to claim adverse possession [A2 B3 C2] is proficient in acrobatics",
        "crocs (the shoe) [A3 B1 C3] is proficient in medicine"
    ]
}
option_chars = lambda case, all_chars : sublist_from_index(all_chars,scene_motion_data["opt_pres"][case])
scene_chars = lambda case, all_chars : sublist_from_index(all_chars,scene_motion_data["scene_pres"][case])
sublist_from_index = lambda base_list, indices: [base_list[included] for included in indices]
scene_motion_data = {
    "scene_data":scenes_maker(get_scn_data(11)),
    "char_data":get_chr_data(3),
    "char_base_bonus":{
        "A4 B1 C2 Di2 In6 Me4 La2 Ac1 Cr1":"a flailing set of limbs",
        "A2 B3 C2 Di2 In2 Me2 La2 Ac5 Cr3":"staying put for 15 years to claim adverse possession",
        "A3 B1 C3 Di3 In3 Me5 La3 Ac1 Cr1":"crocs (the shoe)"
    },
    "calls_str": [
        "test = StoryChosen(test_data)\noutput = test.show_current_scene()\nassert output == expected",
        "test = StoryChosen(test_data)\nassert test.select_character_for_check('diplomacy',scene_characters,option_characters).get_name()==expected_name\ntest.select_option(1,7)\noutput = test.show_current_scene()\nassert output == expected",
        "test = StoryChosen(test_data)\nassert test.select_character_for_check('charm',scene_characters,option_characters).get_name()==expected_name\ntest.select_option(3,-3)\noutput = test.show_current_scene()\nassert output == expected",
        "test = StoryChosen(test_data)\nassert test.select_character_for_check('body',scene_characters,option_characters).get_name()==expected_name\ntest.select_option(1,10)\ntest.select_option(2,1)\noutput = test.show_current_scene()\nassert output == expected",
        "test = StoryChosen(test_data)\nassert test.select_character_for_check('craft',scene_characters,option_characters).get_name()==expected_name\ntest.select_option(1,10)\ntest.select_option(1,3)\noutput = test.show_current_scene()\nassert output == expected",
        "test = StoryChosen(test_data)\nassert test.select_character_for_check('medicine',scene_characters,option_characters).get_name()==expected_name\ntest.select_option(3,-3)\ntest.select_option(4,1)\noutput = test.show_current_scene()\nassert output == expected",
        "test = StoryChosen(test_data)\nassert test.select_character_for_check('language',scene_characters,option_characters).get_name()==expected_name\ntest.select_option(3,0)\ntest.select_option(1,2)\noutput = test.show_current_scene()\nassert output == expected",
    ],
    "last_op":[
        None,'diplomacy','charm','body','craft','medicine','language'
    ],
    "expected":[
        get_scene_pres("S"), get_scene_pres("1"),get_scene_pres("10"),
        get_scene_pres("1"),get_scene_pres("10"),get_scene_pres("E*2"),
        get_scene_pres("4"),
    ],
    "run_args":[
        [],
        [[1,7]],
        [[3,-3]],
        [[1,10],[2,1]],
        [[1,10],[1,3]],
        [[1,-10],[3,1]],
        [[3,0],[1,2]],
    ],
    "scene_pres": [[1,2,3],[1,2,3],[1,2,3],[2],[2],[],[]],
    "opt_pres": [[],[2],[1,2],[],[1],[],[1]],
    "expected_chr": [
        None,"staying put for 15 years to claim adverse possession","a flailing set of limbs",
        "staying put for 15 years to claim adverse possession","a flailing set of limbs","crocs (the shoe)",
        "a flailing set of limbs"
    ]
}


class test_Story_SceneDisplaySelect(unittest.TestCase):
    def setup_class_data(self,case):
        scene_data = scene_motion_data["scene_data"]
        chr_data = scene_motion_data["char_data"]
        str_expect = scene_motion_data["expected"][case]
        expected_char = scene_motion_data["expected_chr"][case]
        msg_base = f'\n\nattempted to create a StoryBest with 11 scenes and 3 characters\n\nThen ran the functions:\n{scene_motion_data["calls_str"][case]}\n\nExpectation was \nCharacter chosen: {expected_char}\nand final scene of {str_expect}\n\n'
        try:
            S = StoryChosen(scene_data,chr_data)
            all_chars = [None]+[make_char_class(i) for i in range(3)]
            if not scene_motion_data["last_op"][case] is None:
                observed_char = S.select_character_for_check(scene_motion_data["last_op"][case],scene_chars(case,all_chars),option_chars(case,all_chars)).get_name()
            else:
                observed_char = None
            for instruction in scene_motion_data["run_args"][case]:
                S.select_option(instruction[0],instruction[1])
            observed = S.show_current_scene()
            if ((observed == str_expect) and (observed_char == expected_char)):
                success = True
                msg = ""
            else:
                success = False
                msg = msg_base+f'however we got as below\nChosen character: {observed_char}\nfinal Scene:\n{observed}'
        except Exception as e:
            success = False
            msg = msg_base+f'however the error below was raised\n{e.__class__.__name__}({str(e)})'
        self.assertTrue(success,msg)
    def testReplacingSceneAndOptions(self):
        self.setup_class_data(0)
    def testOneInOptionAllInScene(self):
        self.setup_class_data(1)
    def testMultInOption(self):
        self.setup_class_data(2)
    def testSceneOnly(self):
        self.setup_class_data(3)
    def testOneSceneOneOption(self):
        self.setup_class_data(4)
    def testNoneChosen(self):
        self.setup_class_data(5)
    def testNoSceneJustOption(self):
        self.setup_class_data(6)

if __name__=="__main__":
    unittest.main()
