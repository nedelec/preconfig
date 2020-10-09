#!/usr/bin/env python
#
# PRECONFIG, a versatile configuration file generator
#
# Copyright Francois J. Nedelec, EMBL 2010--2017, Cambridge University 2019--2020
# This is PRECONFIG version 1.4, last modified on 19.03.2020

"""
# SYNOPSIS

   Preconfig generates files from a template by evaluating doubly-bracketed Python code.
   
# Article:

   preconfig: A Versatile Configuration File Generator for Varying Parameters
   https://openresearchsoftware.metajnl.com/articles/10.5334/jors.156/

# DESCRIPTION

   Preconfig reads the template file from top to bottom, identifying snippets
   of code which are surrounded by double square brackets. It then executes this
   code using the python interpreter, proceeding recursively whenever multiple
   values are specified. Values are eventually converted to their string
   representation, and substituted in place of the code snippet. In this way,
   Preconfig will generate all the possible combinations following the order in
   which these combinations were specified in the file. Importantly, any ac-
   -companying text in the template file is copied verbatim to the output file,
   such that any syntax present in the configuration file can be maintained
   during the process.

   At least one template file should be specified; other arguments are optional.
   If several template files are specified, they will be processed sequentially.
   The names of the produced files are built from the name of the template
   by removing any second extension, and inserting an integer of constant width.

   Examples:

   - config.cym.tpl --> config0000.cym, config0001.cym, config0002.cym, etc.
   - config.txt.tpl --> config0000.txt, config0001.txt, config0002.txt, etc.
   - model.xml.tpl --> model0000.xml, model0001.xml, model0002.xml, etc.

   The width of the variable part (default=4) can be changed on the command line.
   For instance, to specify a width of 2 characters, invoke "preconfig -2 ...".

# SYNTAX

   preconfig [OPTIONS] [DEFINITIONS] TEMPLATE_FILE [ADDITIONAL_TEMPLATE_FILES]

# OPTIONS

    - a pattern can be specified as first argument, to define the names of
    the files to be generated, for example 'config%04i.cym'. If the pattern
    includes '/', as in 'run%04i/config.cym', the directories will be made.
    The pattern must accept integer substitution (eg. '%i' or '%4i' or '%04i').

   - if a positive integer REPEAT is specified, each template file will be
   processed REPEAT times, for example: `preconfig 3 config.cym.tpl` will parse
   the template three times and generate three times more files.

   - if the path to an existing directory is specified, files will be created
   in this directory, for example: `preconfig dir config.cym.tpl`

   - if a negative integer is specified, this will set the width of the integer
   that is used to build the file namess.
   For example: `preconfig -2 config.cym.tpl` will create 'config00.cym', etc.

   - if a '-' is specified, all accessory output is suppressed

   - if a '+' is specified, more detailed information on the parsing is provided.

   - if '++' or 'log' is specified, a file 'log.csv' will be created containing one
   line for each file created, containing the substitutions operated for this file.

   - if '--help' is specified, this documentation will be printed.
   
# DEFINITIONS

   Variables can be defined on the command line as 'name=value', with no space 
   around the '='. They are added to the dictionary used to evaluate the code 
   snippets found inside the template file.
   example: `preconfig rate=100 config.cym.tpl`

   Sequences can be defined as 'name=sequence' or 'name==sequence'. In the first
   instance, the sequence is expanded, generating new files for each value.
   However, using '==' prevents this expansion, and the variable is used verbatim.
   example: `preconfig rate=[1,10,100] config.cym.tpl`

# CODE SNIPPETS

   Any plain python code can be embedded in the file, and functions from the
   [Random Module](https://docs.python.org/library/random.html) can be used.
   It is possible to use multiple bracketed expressions in the same file, and
   to define variables in the python environment. An integer 'n', starting at
   zero and corresponding to the file being generated is automatically defined.
   Note that variables defined in embedded code are not expanded when they appear
   alone in another code (eg. [[vec]]).

## Example 1

   Generate all combinations with multiple values for 2 parameters:

    rate = [[ [1, 10, 100] ]]
    speed = [[ [-1, 0, 1] ]]

   Command: `preconfig TEMPLATE_FILE` with the appropriate file name.
   In this case, Preconfig will generate 9 files.

## Example 2

   Regularly scan 2 parameters with 10 values each,
   one according to a linear scale, and the other with a geometric scale:

    [[ x = range(10) ]]
    [[ y = range(10) ]]
    reaction_rate = [[ 1 + 0.5 * x ]]
    diffusion_rate = [[ 1.0 / 2**y ]]

   Command: `preconfig TEMPLATE_FILE`
   In this case, Preconfig will generate 100 files, one for each combination.

## Example 3

   Scan multiple parameters values randomly:

    diffusion_rate = [[ random.uniform(0,1) ]]
    binding_rate = [[ round(random.uniform(0,1), 3) ]]
    reaction_rate = [[ random.choice([1, 10, 100]) ]]
    abundance = [[ random.randint(0, 1000) ]]

   Command: `preconfig 256 TEMPLATE_FILE`
   In this case, Preconfig is instructed to generate 256 files.

## Example 4

   Randomize two parameters while keeping their ratio constant:

    [[ x = random.uniform(0,1) ]]
    binding_rate = [[ 10.0 * x ]]
    unbinding_rate = [[ x ]]

   Command: `preconfig 256 TEMPLATE_FILE` to make 256 files.

## Example 5

   Randomize one parameter, using 256 values in ascending order:

    [[ x = sorted([random.uniform(0.10, 0.25) for i in range(256)]) ]]
    binding_rate = [[ x ]]

   Command: `preconfig TEMPLATE_FILE`
   In this case, the number of files (256) is specified in the template

## Example 6

   Boolean variables can be used to introduce qualitative differences:

    [[ enable = random.choice([0, 1]) ]]
    feeback = [[ random.uniform(0, 1) if (enable) else 0  ]]

   Command: `preconfig 256 TEMPLATE_FILE` to make 256 files.

## Example 7

   Randomize a value, and print this value as a comment in the file.
   The second line below the [[...]] prints a comment, from which the value
   of 'x' can be read. This can be useful to process the results later.

    [[ x = random.uniform(0,1) ]]
    %preconfig.x= [[ x ]]
    binding_rate = [[ 10*x ]]
    unbinding_rate = [[ 2*x ]]

   Command: `preconfig 256 TEMPLATE_FILE` to make 256 files.
   Extract values:  awk '/%preconfig./{sub("%preconfig.","");print}' config0000.cym

## Example 8

   Quotations can be used to aggregate values:

    [[ vec = ['-1 0 1', '0 1 1', '-1 0 -1'] ]]
    new microtubule
    {
        position = [[vec]]
    }

## Example 9

   Cartesian sampling with filtering:

    [[ (x,y) = [ (x,y) for x in range(10) for y in range(10) if x>y ] ]]

    new particle
    {
        position = [[x]] [[y]]
    }

## Acknowledgments:

We wish to thank the members of the Nedelec group, and all users of Cytosim
for their feedback which has contributed greatly to this development.
We thanks Shaun Jackman and Steven Andrews for valuable feedback!

Copyright Francois J. Nedelec and Serge Dmitrieff
EMBL 2010--2017; Cambridge University 2019--2020
This is Free Software with no WARANTY, just hoping to be useful.
Preconfig is distributed under GPL3.0 Licence (see LICENCE)
"""

import sys

try:
    import os, io, re
    GLOBALS = { 'random': __import__('random'), 'math': __import__('math') }
except ImportError:
    sys.stderr.write("Error: Preconfig could not load necessary python modules\n")
    sys.exit()

#-------------------------------------------------------------------------------

__VERSION__="1.41"

__DATE__   ="1.10.2020"

# code snippets are surrounded by double square brackets:
CODE = '['
DECO = ']'


# A function to return version to be able to pip package it
def version():
    return __VERSION__


#-------------------------------------------------------------------------------

def pop_sequence(dic, protected):
    """
        Remove an entry in the dictionary that has multiple values
    """
    for k, v in dic.items():
        try:
            len(v)
            if not k in protected:
                dic.pop(k)
                return (k, v)
        except:
            pass
    return ('', [])


def try_assignment(arg):
    """
        Check if `arg` follows the format of a variable assignent,
        and if that succeeds, return the key and value strings in a tuple.
    """
    res = re.match(r" *([a-zA-Z]\w*) *= *(.*)", arg)
    #print("   try_assignment `%s'" % arg);
    #print(res.groups())
    if not res or not len(res.groups()) == 2:
        return ('', arg)
    k = res.group(1)
    v = res.group(2).strip()
    #print("   assigned `%s' = `%s'" % (k, v))
    return (k, v)


def get_block(file, S, E):
    """
    Extract from `file` the next block starting with DOUBLE delimiters 'SS'
        and ending with matching 'EE'.
    Returns 3 values:
        - the text found before the block start
        - the block with its delimiters
        - a boolean EOF indicator
    """
    ch = file.read(1)
    sec = 0
    pre = ''
    blk = ''
    lev = 0
    while file and ch:
        pc = ch
        ch = file.read(1)
        if ch == S:
            if sec:
                lev += 1
            if pc == S:
                sec += 1
        if sec:
            blk += pc
            #print("%c%c >  lev %i sec %i" %(pc, ch, lev, sec))
        else:
            pre += pc
        if ch == E:
            if sec:
                lev -= 1
            if pc == E:
                #print("%c%c EE lev %i sec %i" %(pc, ch, lev, sec))
                if lev == -2:
                    return (pre, blk+ch, False)
    # reaching end of file:
    return (pre, blk, True)


#-------------------------------------------------------------------------------
class Preconfig:
    """ A class container for preconfig,
    contains inner variables and methods """
    def __init__(self):
        # initialization
        self.locals = {}
        self.protected = []
        # streams for output (all output is hidden by default):
        self.out = open(os.devnull, 'w')
        self.log = []
        # motif used to compose file names
        self.pattern = ''
        # number of digits used to compose `pattern`
        self.nb_digits = 4
        # index of file being generated
        self.file_index = 0
        # list of files generated
        self.files_made = []
        # name of current input file being processed (used for error reporting)
        self.template = ''

    def evaluate(self, arg):
        """
            Evaluate `arg` and return result
        """
        res = arg
        #print("   evaluate("+arg+")")
        try:
            res = eval(arg, GLOBALS, self.locals)
        except Exception as e:
            sys.stderr.write("\033[95m")
            sys.stderr.write("Error evaluating '%s' in `%s`:\n" % (arg, self.template))
            sys.stderr.write("\033[0m")
            sys.stderr.write("    "+str(e)+'\n')
            sys.exit(1)
        if not isinstance(res, str):
            try:
                res = list(res)
            except Exception:
                pass
        #print("evaluate("+arg+") = " + repr(res))
        return res

    def operate(self, key, val, block):
        """
            either define a variable 'key'
            or return the value 'val'
        """
        if key:
            exec(key+'='+repr(val), GLOBALS, self.locals)  #self.locals[key] = v
            self.out.write("|%50s <-- %s\n" % (key, str(val)) )
            #print("%s <-- %s" % (key, str(val)) )
            return ''
        else:
            self.out.write("|%50s --> %s\n" % (block, str(val)) )
            #print("%s --> %s" % (block, str(val)) )
            if isinstance(val, str):
                return val
            return repr(val)

    def process(self, file, text):
        """
            `process()` will identify and substitute bracketed code blocks
            embedded in the input file, and generate a file at EOF.
        """
        output = text

        while file:
            (pre, block, eof) = get_block(file, CODE, DECO)
            #print("%i characters +  '%s'" % (len(pre), block))
            output += pre
            if eof:
                if block:
                    sys.stderr.write("Error: unclosed bracketted block in:\n");
                    sys.stderr.write("    "+block.split('\n', 1)[0]+'\n');
                    sys.exit(1)
                # having exhausted the input, we generate a file:
                self.make_file(output)
                return
            # remove outer brackets:
            key = ''
            cmd = block[2:-2]
            val = cmd.strip()
            # print("%4i characters... code block '%s'" % (len(pre), val))
            if val[0]==CODE and val[1]==CODE and val[-1]==DECO and val[-2]==DECO:
                # double-brackets are removed and the code not evaluated:
                pass
            elif val in self.locals:
                # a plain variable is substituted but not expanded:
                val = self.locals[val]
            else:
                # interpret command:
                (key, vals) = try_assignment(val)
                vals = self.evaluate(vals)
                try:
                    # use 'pop()' to probe if multiple values were specified...
                    # put last value aside for later:
                    val = vals.pop()
                    ipos = file.tell()
                    for v in vals:
                        #print("value("+val+")="+repr(v));
                        self.process(file, output+self.operate(key, v, block))
                        file.seek(ipos)
                except (AttributeError, IndexError):
                    # a single value was specified:
                    val = vals
            # handle remaining value:
            output += self.operate(key, val, block)

    def set_template(self, name):
        """
        Initialize variable to process template file 'name'
        """
        self.file_index = 0
        self.files_made = []
        self.template = name

    def set_pattern(self, name, path):
        """
        insert the number before the first '.' on the pattern
        """
        [main, ext] = os.path.basename(name).split('.', 1)
        ext, drop = os.path.splitext(ext)
        res = main + '%0' + repr(self.nb_digits) + 'i' + '.' + ext
        if path:
            res = os.path.join(path, res)
        self.pattern = res

    def next_file_name(self):
        """
        Generate the name of the next output file
        """
        if self.pattern:
            n = self.pattern % self.file_index
        else:
            n = 'config%04i.txt' % self.file_index
        self.file_index += 1
        # update variable
        self.locals['n'] = self.file_index
        return n

    def make_file(self, text):
        """
        Create a file with the specified text
        """
        dst = self.next_file_name()
        #make directory if name includes a non-existent directory:
        dir = os.path.dirname(dst)
        if dir and not os.path.isdir(dir):
            os.mkdir(dir)
        with open(dst, 'w') as f:
            f.write(text)
            self.files_made.extend([dst])
        # fancy ouput:
        self.out.write(' \\'+repr(self.locals)+'\n')
        self.out.write('  \\'+('> '+dst+'\n').rjust(96, '-'))
        # write log:
        if self.log:
            keys = sorted(self.locals.keys())
            if self.file_index == 1:
                self.log.write('%20s' % 'file')
                for k in keys:
                    self.log.write(', %10s' % k)
                self.log.write('\n')
            self.log.write('%20s' % dst)
            for k in keys:
                self.log.write(', %10s' % repr(self.locals[k]))
            self.log.write('\n')

    def expand(self, values, file, text):
        """
            Calls itself recursively to remove all entries of the dictionary
            that are associated with multiple values.
        """
        #print("expand("+repr(values)+")")
        (key, vals) = pop_sequence(values, self.protected)
        if key:
            ipos = file.tell()
            for v in vals:
                values[key] = v
                self.out.write("|%50s <-- %s\n" % (key, str(v)) )
                #print("|%50s <-- %s\n" % (key, str(v)) )
                self.expand(values, file, text)
                file.seek(ipos);
            # restore all values on upward recursion
            values[key] = vals
        else:
            #copy dictionary:
            for key in values:
                self.locals[key] = values[key]
            self.locals['n'] = self.file_index
            self.process(file, text)

    def parse(self, name, values, repeat=1, path=''):
        """
            process one file, and return the list of files generated
        """
        self.set_template(name)
        if not self.pattern:
            self.set_pattern(name, path)
        for x in range(repeat):
            with open(name, 'r') as f:
                self.expand(values, f, '')
        return self.files_made

    def main(self, args):
        """
            process arguments and perform corresponding task
        """
        verbose = 1
        repeat = 1
        inputs = []
        values = {}
        path = ''
        
        # first argument may define the pattern:
        arg = args[0]
        if arg.find('%') >= 0 and not os.path.isfile(arg):
            self.pattern = arg
            args.pop(0)
        
        for arg in args:
            #print("preconfig argument `%s'" % arg)
            if os.path.isdir(arg):
                path = arg
            elif os.path.isfile(arg):
                inputs.append(arg)
            elif arg.isdigit():
                repeat = int(arg)
            elif arg == '-':
                verbose = 0
            elif arg == '+':
                self.out = sys.stderr
                verbose = 0
            elif arg == '++' or arg == 'log':
                self.log = open('log.csv', 'w')
            elif arg[0] == '-' and arg[1:].isdigit():
                self.nb_digits = int(arg[1:])
            else:
                (k,v) = try_assignment(arg)
                if k:
                    # a double '==' will prevent expansion of the variable
                    if v[0] == '=':
                        values[k] = v[1:]
                        self.protected.append(k)
                    else:
                        values[k] = self.evaluate(v)
                else:
                    sys.stderr.write("  Error: unexpected argument `%s'\n" % arg)
                    sys.exit()

        if not inputs:
            sys.stderr.write("  Error: you must specify an input template file\n")
            sys.exit()

        for i in inputs:
            #out.write("Reading %s\n" % i)
            res = self.parse(i, values, repeat, path)
            if verbose == 1:
                if len(res) == 1:
                    print("generated %s" % res[0])
                else:
                    print("%i files generated: %s ... %s" % (len(res), res[0], res[-1]))


#-------------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You must specify a template file (for instructions, invoke with option '--help')")
    elif sys.argv[1].endswith("help"):
        print(__doc__)
    elif sys.argv[1]=='--version':
        print("This is PRECONFIG version %s (%s)" %(__VERSION__,__DATE__))
    else:
        preconf=Preconfig()
        preconf.main(sys.argv[1:])

