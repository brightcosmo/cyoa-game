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

testdata = {
    "inputs": [
        ["Val Idoty","A2 B2 C3","Di* In Me La Ac Cr"],
        ["Val Idoty, sports star","A2 B3 C2","Di In Me La Ac* Cr"],
        ["Val Idoty, speaker","A3 B1 C3","Di In Me La* Ac Cr"],
        ["Val Idoty, leech attacher","A3 B2 C2","Di In Me* La Ac Cr"],
        ["Val Idoty, tool (wielder)","A3 B3 C1","Di In Me La Ac Cr*"],
        ["Val Idoty, spy","A2 B2 C3","Di In* Me La Ac Cr"],
        ["one stat high","A5 B1 C1","Di* In Me La Ac Cr"],
        ["one stat high2","A1 B1 C5","Di* In Me La Ac Cr"],
        ["one stat low","A4 B0 C3","Di* In Me La Ac Cr"],
        ["sum low","A2 B2 C2","Di* In Me La Ac Cr"],
        ["sum low2","A1 B2 C3","Di* In Me La Ac Cr"],
        ["sum low3","A1 B1 C1","Di* In Me La Ac Cr"],
        ["sum high","A3 B3 C3","Di* In Me La Ac Cr"],
        ["sum high2","A2 B3 C3","Di* In Me La Ac Cr"],
        ["sum high3","A4 B4 C1","Di* In Me La Ac Cr"],
        ["missing prof","A2 B3 C2","Di In Me La Ac Cr"],
        ["extra profs prof","A2 B3 C2","Di In* Me La Ac Cr*"],
        ["weyard skayel","A2 B3 C2","Di In Mn La Ac Cr*"],
        ["weyard skayel2","A2 B3 C2","Di In Me Ff* Ac Cr"],
        ["check my stats","A4 B1 C2","Di In Me La* Ac Cr"],
        ["check my stats2","A4 B1 C2","Di* In Me La Ac Cr"],
        ["check my stats3","A4 B1 C2","Di In* Me La Ac Cr"],
        ["check my stats4","A4 B1 C2","Di In Me* La Ac Cr"],
        ["check my stats5","A4 B1 C2","Di In Me La Ac* Cr"],
        ["check my stats6","A4 B1 C2","Di In Me La Ac Cr*"],
    ],
    "str_format": [
        "Val Idoty [A2 B2 C3] is proficient in diplomacy",
        "Val Idoty, sports star [A2 B3 C2] is proficient in acrobatics",
        "Val Idoty, speaker [A3 B1 C3] is proficient in language",
        "Val Idoty, leech attacher [A3 B2 C2] is proficient in medicine",
        "Val Idoty, tool (wielder) [A3 B3 C1] is proficient in craft",
        "Val Idoty, spy [A2 B2 C3] is proficient in investigation",
        "-", "-", "-", "-", "-","-","-","-","-","-","-","-","-"
    ],
    "errors":[
        None,None,None,None,None,None,
        "invalid value for acumen; 5 is not in the range 1 to 4",
        "invalid value for charm; 5 is not in the range 1 to 4",
        "invalid value for body; 0 is not in the range 1 to 4",
        "A2 B2 C2 is invalid, sum of attributes does not equal 7",
        "A1 B2 C3 is invalid, sum of attributes does not equal 7",
        "A1 B1 C1 is invalid, sum of attributes does not equal 7",
        "A3 B3 C3 is invalid, sum of attributes does not equal 7",
        "A2 B3 C3 is invalid, sum of attributes does not equal 7",
        "A4 B4 C1 is invalid, sum of attributes does not equal 7",
        "Di In Me La Ac Cr is invalid; exactly one proficiency asterisk expected",
        "Di In* Me La Ac Cr* is invalid; exactly one proficiency asterisk expected",
        "Di In Mn La Ac Cr* is invalid; unexpected skill name given",
        "Di In Me Ff* Ac Cr is invalid; unexpected skill name given"
    ],
    "stats": [
        "-", "-", "-", "-", "-","-","-","-","-","-","-","-","-","-", "-", "-", "-", "-","-",
        [4,1,2,"check my stats","language"],
        [4,1,2,"check my stats","diplomacy"],
        [4,1,2,"check my stats","investigation"],
        [4,1,2,"check my stats","medicine"],
        [4,1,2,"check my stats","acrobatics"],
        [4,1,2,"check my stats","craft"],
    ],
}

chr_error_msg = lambda case : testdata["errors"][case]
chr_expect_error = lambda case : not chr_error_msg(case) is None
chr_str_out = lambda case: testdata["str_format"][case]
chr_str_out_with_quotes = lambda case: "'"+chr_str_out(case)+"'"
chr_input = lambda case : testdata["inputs"][case]
chr_failure_check_txt = lambda case : 'assert str(X) == {expected_value}' if not chr_expect_error(case) else ""
chr_failure_msg = lambda case : f'\n\ncall triggered was:\nX = Character({chr_input(case)})\n{chr_failure_check_txt(case)}\n\nexpected:\n{"ValueError("+chr_error_msg(case)+")" if chr_expect_error(case) else "str(Character({input_data}) == "+chr_str_out_with_quotes(case)}'
get_test_data = lambda case: testdata["stats"][case]

class test_Character(unittest.TestCase):
    def testCaseCreateValid1AdaptedForOthers(self, case=0):
        if chr_expect_error(case):
            success = False
            message = None
            try:
                Character(chr_input(case))
                success = False
                message = chr_failure_msg(case)+f'\nInstead no error occured'
            except ValueError as v:
                if str(v)==chr_error_msg(case):
                    success = True
                else:
                    success = False
                    message = chr_failure_msg(case)+f'\nInstead this was raised\nValueError({str(v)})'
            except Exception as e:
                success = False
                message = chr_failure_msg(case)+f'\nInstead this was raised\n{e.__class__.__name__}({str(e)})'
            self.assertTrue(success,message)
        else:
            try:
                X = Character(chr_input(case))
                self.assertTrue(str(X) == chr_str_out(case),chr_failure_msg(case)+f'\nInstead we got {str(X)}')
            except Exception as e:
                self.assertTrue(False,chr_failure_msg(case)+f'\nInstead this exception occured: {str(e)}')
    def testCreateValid2(self):
        case = 1
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateValid3(self):
        case = 2
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateValid4(self):
        case = 3
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateValid5(self):
        case = 4
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateValid6(self):
        case = 5
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateInvalidStat1(self):
        case = 6
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateInvalidStat2(self):
        case = 7
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateInvalidStat3(self):
        case = 8
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateInvalidSum1(self):
        case = 9
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateInvalidSum2(self):
        case = 10
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateInvalidSum3(self):
        case = 11
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateInvalidSum4(self):
        case = 12
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateInvalidSum5(self):
        case = 13
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateInvalidSum6(self):
        case = 14
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateInvalidSkills1(self):
        case = 15
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateInvalidSkills2(self):
        case = 16
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateInvalidSkills3(self):
        case = 17
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testCreateInvalidSkills4(self):
        case = 18
        self.testCaseCreateValid1AdaptedForOthers(case)
    def testRunGettersInitiallyAcumen(self,case=19,getter=0):
        stats = get_test_data(case)
        expected = stats[getter]
        getter_names = ["get_acumen","get_body","get_charm","get_name","get_proficient"]
        try:
            c = Character(chr_input(case))
            getters = [c.get_acumen,c.get_body,c.get_charm,c.get_name,c.get_proficient]
            observed = getters[getter]()
            if observed == expected:
                success = True
                message = None
            else:
                success = False
                message = f'\n\nExpected that Character({chr_input(case)}).{getter_names[getter]}() == {expected} but got {observed}'
        except Exception as e:
            success = False
            message = f'\n\nExpected that Character({chr_input(case)}).{getter_names[getter]}() == {expected}\n Instead the following error occurred: {e.__class__.__name__}({str(e)})'
        self.assertTrue(success,message)
    def testGetBody(self):
        case = 19
        getter = 1
        self.testRunGettersInitiallyAcumen(case,getter)
    def testGetCharm(self):
        case = 19
        getter = 2
        self.testRunGettersInitiallyAcumen(case,getter)
    def testGetName(self):
        case = 19
        getter = 3
        self.testRunGettersInitiallyAcumen(case,getter)
    def testGetProficient1(self):
        case = 19
        getter = 4
        self.testRunGettersInitiallyAcumen(case,getter)
    def testGetProficient2(self):
        case = 20
        getter = 4
        self.testRunGettersInitiallyAcumen(case,getter)
    def testGetProficient3(self):
        case = 21
        getter = 4
        self.testRunGettersInitiallyAcumen(case,getter)
    def testGetProficient4(self):
        case = 22
        getter = 4
        self.testRunGettersInitiallyAcumen(case,getter)
    def testGetProficient5(self):
        case = 23
        getter = 4
        self.testRunGettersInitiallyAcumen(case,getter)
    def testGetProficient6(self):
        case = 24
        getter = 4
        self.testRunGettersInitiallyAcumen(case,getter)

if __name__=="__main__":
    unittest.main()
