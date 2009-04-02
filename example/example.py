'''A sample application for cmd2.'''

from cmd2 import Cmd, make_option, options, Cmd2TestCase
import unittest, optparse, sys

class CmdLineApp(Cmd):
    multilineCommands = ['orate']
    Cmd.shortcuts.update({'&': 'speak'})
    maxrepeats = 3
    Cmd.settable.append('maxrepeats')

    @options([make_option('-p', '--piglatin', action="store_true", help="atinLay"),
              make_option('-s', '--shout', action="store_true", help="N00B EMULATION MODE"),
              make_option('-r', '--repeat', type="int", help="output [n] times")
             ])
    def do_speak(self, arg, opts=None):
        """Repeats what you tell me to."""
        arg = ''.join(arg)
        if opts.piglatin:
            arg = '%s%say' % (arg[1:], arg[0])
        if opts.shout:
            arg = arg.upper()
        repetitions = opts.repeat or 1
        for i in range(min(repetitions, self.maxrepeats)):
            self.stdout.write(arg)
            self.stdout.write('\n')
            # self.stdout.write is better than "print", because Cmd can be
            # initialized with a non-standard output destination

    do_say = do_speak     # now "say" is a synonym for "speak"
    do_orate = do_speak   # another synonym, but this one takes multi-line input

class TestMyAppCase(Cmd2TestCase):
    CmdApp = CmdLineApp
import logging
logging.basicConfig(level=logging.DEBUG,
                    filename='exlog.txt',
                    filemode='w')
parser = optparse.OptionParser()
parser.add_option('-t', '--test', dest='test', metavar='FILE', 
                  help='''Test against transcript(s) in FILE (wildcards OK)''')                  
(callopts, callargs) = parser.parse_args()
logging.error(callopts)
if callopts.test:
    CmdLineApp.testfile = callopts.test
    logging.error(CmdLineApp.testfile)
    sys.argv = [sys.argv[0]] # the --test argument upsets unittest.main()
    unittest.main()
else:
    CmdLineApp().cmdloop()