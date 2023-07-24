from story_class_structures import *
from choose_your_own_adventure import read_file
from contextlib import contextmanager
import sys, os
import unittest
from unittest import mock
from unittest.mock import patch

x_txt_extender = lambda chr_txt : "\n".join(chr_txt)
expected_maker = lambda chr_txt,scn_txt : f'CHARACTERS\n{x_txt_extender(chr_txt)}\nSCENES\n{x_txt_extender(scn_txt)}'
get_scene_pres = lambda scene_id : story_data["scene_user_print"][scene_id]
get_scn_data = lambda scn_count : story_data["scenes"][:scn_count]
chr_joiners = lambda characters : flatten([char + ["----"] for char in characters])[:-1]
get_chr_data = lambda chr_count : chr_joiners(story_data["characters"][:chr_count])
get_exp_scn = lambda scn_count : story_data["expected_scn"][:scn_count]
get_exp_chr = lambda chr_count : story_data["chr_strs"][:chr_count]
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
        ["a flailing set of limbs","A4 B1 C2","Di In* Me La Ac Cr"],
        ["staying put for 15 years to claim adverse possession","A2 B3 C2","Di In Me La Ac* Cr"],
        ["crocs (the shoe)","A3 B3 C1","Di In Me* La Ac Cr"]
    ],
    "chr_strs":[
        "a flailing set of limbs [A4 B1 C2] is proficient in investigation",
        "staying put for 15 years to claim adverse possession [A2 B3 C2] is proficient in acrobatics",
        "crocs (the shoe) [A3 B3 C1] is proficient in medicine"
    ]
}
scene_motion_data = {
    "scene_data":scenes_maker(get_scn_data(11)),
    "char_data":get_chr_data(3),
    "calls_str": [
        "test = Story(read_file('fake_test_file.txt'),list_of_character_data)\noutput = str(test)\nassert output == expected",
        "test = Story(list_of_scene_data,read_file('fake_test_file.txt'))\noutput = str(test)\nassert output == expected",
    ],
}


class test_Story_from_file(unittest.TestCase):
    def testReadFileForStoryScenes(self):
        case = 0
        scene_data = scene_motion_data["scene_data"]
        chr_data = scene_motion_data["char_data"]
        str_expect = str_expect = expected_maker(get_exp_chr(3),get_exp_scn(11))
        msg_base = f'\n\nattempting to create a StoryBest with 11 scenes and 3 characters\nRan the functions:\n{scene_motion_data["calls_str"][case]}\n\nExpectation was \n{str_expect}\n\n'
        try:
            with patch('builtins.open', mock.mock_open(read_data="\n".join(scene_data)), create=True) as m:
                tried_data = read_file("fake_file.txt")
            #tried_data = scene_data
            S = Story(tried_data,chr_data)
            observed = str(S)
            if observed == str_expect:
                success = True
                msg = ""
            else:
                success = False
                msg = msg_base+f'however we got as below\nstring representation of story:\n{observed}'
        except Exception as e:
            success = False
            msg = msg_base+f'however the error below was raised\n{e.__class__.__name__}({str(e)})'
        self.assertTrue(success,msg)

    def testReadFileForStoryCharacters(self):
        case = 1
        scene_data = scene_motion_data["scene_data"]
        chr_data = scene_motion_data["char_data"]
        str_expect = str_expect = expected_maker(get_exp_chr(3),get_exp_scn(11))
        msg_base = f'\n\nattempted to create a StoryBest with 11 scenes and 3 characters\n\nand ran the functions:\n{scene_motion_data["calls_str"][case]}\n\nExpectation was \n{str_expect}\n\n'
        try:
            with patch('builtins.open', mock.mock_open(read_data="\n".join(chr_data)), create=True) as m:
                tried_data = read_file("fake_file.txt")
            #tried_data = scene_data
            S = Story(scene_data,tried_data)
            observed = str(S)
            if observed == str_expect:
                success = True
                msg = ""
            else:
                success = False
                msg = msg_base+f'however we got as below\nstring representation of story:\n{observed}'
        except Exception as e:
            success = False
            msg = msg_base+f'however the error below was raised\n{e.__class__.__name__}({str(e)})'
        self.assertTrue(success,msg)


if __name__=="__main__":
    unittest.main()
