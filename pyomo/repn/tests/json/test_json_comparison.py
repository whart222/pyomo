#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright 2017 National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and 
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain 
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________
#
# Test the Pyomo BAR writer
#
import itertools
import re
import glob
import os
from os.path import abspath, dirname, join
currdir = dirname(abspath(__file__))+os.sep
datadir = abspath(join(currdir, "..", "ampl"))+os.sep

import pyutilib.th as unittest

import pyomo.scripting.pyomo_main as main


class Tests(unittest.TestCase):

    def pyomo(self, cmd):
        os.chdir(currdir)
        output = main.main(['convert', '--logging=quiet', '-c']+cmd)
        return output

class BaselineTests(Tests):
    def __init__(self, *args, **kwds):
        Tests.__init__(self, *args, **kwds)

#
#The following test generates an BAR file for the test case
#and checks that it matches the current pyomo baseline BAR file
#
@unittest.nottest
def json_writer_baseline_test(self, name):
    baseline = currdir+name+'.pyomo.json'
    output = currdir+name+'.test.json'
    if not os.path.exists(baseline):
        self.skipTest("baseline file (%s) not found" % (baseline,))

    if os.path.exists(datadir+name+'_testCase.py'):
        testDir = datadir
    else:
        testDir = currdir
    testCase = testDir+name+'_testCase.py'

    if os.path.exists(testDir+name+'.dat'):
        self.pyomo(['--output='+output,
                    '--file-determinism=3',
                    '--symbolic-solver-labels',
                    testCase,
                    testDir+name+'.dat'])
    else:
        self.pyomo(['--output='+output,
                    '--file-determinism=3',
                    '--symbolic-solver-labels',
                    testCase])

    # Check that the pyomo JSON file matches its own baseline
    self.assertMatchesJsonBaseline(output, baseline, tolerance=1e-7)


class ASLTests(Tests):

    def __init__(self, *args, **kwds):
        Tests.__init__(self, *args, **kwds)


# add test methods to classes
for f in itertools.chain(glob.glob(datadir+'*_testCase.py'),
                         glob.glob(currdir+'*_testCase.py')):
    name = re.split('[._]',os.path.basename(f))[0]
    BaselineTests.add_fn_test(fn=json_writer_baseline_test, name=name)
    #ASLTests.add_fn_test(fn=nlwriter_asl_test, name=name)

if __name__ == "__main__":
    unittest.main()
