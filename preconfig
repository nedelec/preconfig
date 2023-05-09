#!/usr/bin/env python3
#
# PRECONFIG, a versatile configuration file generator for varying parameters
#
# Copyright Francois J. Nedelec and  Serge Dmitrieff, 
# EMBL 2010--2017, Cambridge University 2019--2022
# This is PRECONFIG version 1.59, last modified on 03.02.2023

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

   By default, indexing starts at zero, but this can be changed with 'n=INTEGER'.

# SYNTAX

   preconfig [OPTIONS] [DEFINITIONS] TEMPLATE_FILE [ADDITIONAL_TEMPLATE_FILES]

# OPTIONS

    - a pattern can be specified as 'path=STRING', to define the names of
    the files to be generated, for example 'config%04i.cym'. If the pattern
    includes '/', as in 'run%04i/config.cym', the directories will be made.
    The pattern must accept integer substitution (eg. '%i' or '%4i' or '%04i').

   - if a positive integer REPEAT is specified, each template file will be
   processed REPEAT times, for example: `preconfig 3 config.cym.tpl` will parse
   the template three times and generate three times more files.

   - if the path to an existing directory is specified, files will be created
   in this directory, for example: `preconfig dir config.cym.tpl`
   
   - if 'path=FILENAME' is specified, Preconfig will use this name for the first
   file that it generates. If this file already exists, it will be overwritten.

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
   to define variables in the python environment.
   The index of the file being generated is defined as variable 'n'.

   Note that variables defined in embedded code are not expanded when they appear
   alone in another code (eg. [[vec]]). Furthermore, Preconfig will keep any code
   that it cannot evaluate verbatim, which happens for example if they contain
   a variable that is not defined, or some syntax error.

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
    %config.x= [[ x ]]
    binding_rate = [[ 10*x ]]
    unbinding_rate = [[ 2*x ]]

   Command: `preconfig 256 TEMPLATE_FILE` to make 256 files.
   To get values: awk '/%config./{sub("%config.","");print}' config0000.cym

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
EMBL 2010--2017; Cambridge University 2019--2022
This is Free Software with no WARANTY, just hoping to be useful.
Preconfig is distributed under GPL3.0 Licence (see LICENCE)
"""

import sys

try:
    import os, io, re, time
    GLOBALS = { 'random': __import__('random'), 'math': __import__('math') }
except ImportError as e:
    sys.stderr.write("Preconfig could not load `%s`\n"%str(e))
    sys.exit(7)

#-------------------------------------------------------------------------------

__VERSION__="1.58"

__DATE__ ="29.09.2022"

# code snippets are surrounded by double square brackets:
CODE = '['
DECO = ']'


# A function to return version to be able to pip package it
def version():
    return __VERSION__


#-------------------------------------------------------------------------------

def cannonical_pattern(arg):
    """check for repeated '%' character, replacing printf syntax: %04i """
    c = arg.count('%')
    for n in range(c,1,-1):
        if arg.find('%'*n) > 0:
            return arg.replace('%'*n, '%0'+str(n)+'i', 1)
    return arg


def pop_sequence(dic, protected):
    """
        Remove an entry in the dictionary that has multiple values
    """
    for k, v in dic.items():
        if not isinstance(v, str):
            try:
                if len(v) > 1 and not k in protected:
                    dic.pop(k)
                    #print(" pop %s : %s" %(k, str(v)))
                    return (k, v)
            except:
                pass
    return ('', [])


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
    """ A class container for preconfig """
    def __init__(self):
        self.verbose = 2
        # local dictionary with index of file being generated
        self.locals = { 'n' : 0 }
        # variables for which expension is disabled:
        self.protected = []
        # streams for output (all output is hidden by default):
        self.out = open(os.devnull, 'w')
        self.log = []
        self.log_doc = 1
        # motif used to compose file names
        self.pattern = ''
        # number of digits used to compose `pattern`
        self.nb_digits = 4
        # list of files generated
        self.files_made = []
        # name of first output file (only one file can be made with this name)
        self.file_name = ''
        # name of current input file being processed (used for error reporting)
        self.template = ''
    
    def write_log(self, name):
        """ record some info in the log """
        keys = sorted(self.locals.keys())
        # write column headers
        if self.log_doc:
            self.log.write('%20s' % 'file')
            for k in keys:
                self.log.write(', %10s' % k)
            self.log.write('\n')
            self.log_doc = 0
        # write a line of data:
        self.log.write('%20s' % name)
        for k in keys:
            self.log.write(', %10s' % repr(self.locals[k]))
        self.log.write('\n')

    def report(self, code, key, val):
        """ print some info to output """
        if key:
            self.out.write("|%50s <-- %s\n" % (key, repr(val)) )
        else:
            self.out.write("|%50s --> %s\n" % (code, repr(val)) )

    def evaluate(self, arg):
        """ Return evaluation of `arg', checking for syntax error"""
        try:
            #print("Preconfig:evaluate " + arg)
            res = eval(arg, GLOBALS, self.locals)
        except NameError as e:
            #sys.stderr.write("NameError in `%s': %s\n" % (arg, str(e)))
            raise e
        except Exception as e:
            sys.stderr.write("\033[93m")
            sys.stderr.write("Preconfig Syntax Error in `%s': %s" % (arg, str(e)))
            sys.stderr.write("\033[0m")
            sys.stderr.write("\n")
            sys.exit(2)
        if not isinstance(res, str):
            try:
                res = list(res)
            except Exception:
                pass
        return res
    
    def try_assignment(self, code, blok):
        """
            Check if `arg` follows the format of a variable definition (X=RHS),
            and in that case return (key, self.evaluate(RHS)).
            Check for (X==RHS) with a double '==', returning (key, RHS) in that case.
            If `arg` is not an assignment, return ('', self.evaluate(arg))
        """
        k = ''
        v = code
        res = re.match(r" *([a-zA-Z]\w*) *= *(.*)", code)
        #print(" preconfig:try_assignment(%s): %s" % (code, res.groups()))
        if res and len(res.groups()) > 1:
            k = res.group(1)
            v = res.group(2).strip()
            if v[0] == '=':
                # with '==' use raw right-hand side 
                v = v[1:]
                self.protected.append(k)
                print("   protected `%s == %s'" % (k, v))
                return (k, v)
            #print("   identified `%s <- %s'" % (k, v))
        try:
            res = self.evaluate(v)
        except NameError as e:
            if self.verbose > 1:
                sys.stderr.write("\033[1m\033[96m")
                sys.stderr.write("Preconfig kept `%s' verbatim since %s" % (code, str(e)))
                sys.stderr.write("\033[0m")
                sys.stderr.write("\n")
            exit_code = 1
            #print(self.locals)
            self.report(blok, '', blok)
            return ('', blok)
        self.report(code, k, res)
        return (k, res)
    
    def process(self, file, text):
        """
            Identify and recursively substitute bracketed code blocks embedded
            in the input `file`. Generate output file evetytime EOF is reached.
        """
        output = text

        while file:
            (pre, blok, eof) = get_block(file, CODE, DECO)
            #print("%i characters +  '%s'" % (len(pre), blok))
            output += pre
            if eof:
                if blok:
                    sys.stderr.write("Preconfig Error: unclosed bracketted block in:\n")
                    sys.stderr.write("    "+blok.split('\n', 1)[0]+'\n')
                    sys.exit(2)
                # having exhausted the input, we generate a file:
                self.make_file(output)
                return
            # remove outer brackets:
            key = ''
            code = blok[2:-2].strip()
            # print("%4i characters... " % len(pre), end='')
            if code[0]==CODE and code[1]==CODE and code[-1]==DECO and code[-2]==DECO:
                # any further level of bracketting is not evaluated:
                val = code
            elif code in self.locals:
                # a defined variable is substituted but not expanded:
                val = repr(self.locals[code])
            else:
                # check the code for assigment, and evaluate code:
                key, vals = self.try_assignment(code, blok)
                # print("code block `%s' -> %s" % (blok, vals))
                if key:
                    self.locals[key] = vals
                try:
                    # use 'pop()' to probe if multiple values were specified...
                    # setting last value aside for later:
                    val = vals.pop()
                    ipos = file.tell()
                    for v in vals:
                        self.report(code, key, v)
                        if key:
                            self.locals[key] = v
                            self.process(file, output)
                        else:
                            self.process(file, output+str(v))
                        file.seek(ipos)
                    self.report(code, key, val)
                except (AttributeError, IndexError):
                    # a single value was specified:
                    val = vals
            # handle remaining value:
            if key:
                self.locals[key] = val
            else:
                output += str(val)
    
    def set_template(self, name):
        """
        Initialize variable to process template file 'name'
        """
        self.files_made = []
        self.template = name

    def set_pattern(self, name, path):
        """
        insert the number before the first '.' on the pattern
        """
        name = os.path.basename(name)
        [main, ext] = os.path.splitext(name)
        if ext == '.tpl':
            main, ext = main.split('.', 1)
            ext = '.' + ext
        self.pattern = main + '%0' + repr(self.nb_digits) + 'i' + ext
        if os.path.isdir(path):
            self.pattern = os.path.join(path, self.pattern)

    def next_file_name(self):
        """
        Generate the name of the next output file
        """
        if self.file_name:
            n = self.file_name
            self.file_name = ''
        elif self.pattern:
            n = self.pattern % self.locals['n']
        else:
            n = 'config%04i.txt' % self.locals['n']
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
            self.write_log(dst)
        # get ready for next file:
        self.locals['n'] += 1

    def clear_locals(self):
        n = self.locals['n']
        self.locals.clear()
        self.locals['n'] = n

    def expand(self, values, file, text):
        """
            Calls itself recursively to remove all entries of the `values`
            dictionary that are associated with multiple values.
        """
        (key, vals) = pop_sequence(values, self.protected)
        if key:
            #print("cytosim:expand "+key+" = "+repr(vals))
            ipos = file.tell()
            for v in vals:
                values[key] = v
                self.report('', key, v)
                #print("|%50s <-- %s\n" % (key, str(v)) )
                self.expand(values, file, text)
                file.seek(ipos)
            # restore all values on upward recursion
            values[key] = vals
        else:
            #copy variables to local dictionnary:
            for k, v in values.items():
                self.locals[k] = v
            #the file index should only be copied once:
            values.pop('n', 0)
            self.process(file, text)

    def parse(self, name, file, values, repeat=1, path=''):
        """
            process one file, and return the list of files generated
        """
        self.set_template(name)
        if not self.pattern:
            self.set_pattern(name, path)
        if not os.path.isdir(path):
            self.file_name = path
        for x in range(repeat):
            try:
                self.expand(values, file, '')
            except IOError:
                sys.stderr.write("Preconfig could not load `%s`\n"%name)
                break
            self.clear_locals()
            file.seek(0)
        return self.files_made

    def main(self, args):
        """
            process arguments and perform corresponding task
        """
        repeat = 1
        inputs = []
        values = {}
        path = ''
        
        # first argument may define the pattern:
        if args[0].find('%') >= 0 and not os.path.isfile(args[0]):
            self.pattern = cannonical_pattern(args[0])
            args = args[1 :]
        
        # parse arguments:
        for arg in args:
            #print("Preconfig argument `%s'" % arg)
            if os.path.isdir(arg):
                path = arg
            elif arg.startswith("out="):
                path = arg[4:]
            elif arg.startswith("path="):
                path = arg[5:]
            elif os.path.isfile(arg):
                inputs.append(arg)
            elif arg.isdigit():
                repeat = int(arg)
            elif arg == '{{}}':
                CODE = '{'
                DECO = '}'
            elif arg == '<<>>':
                CODE = '<'
                DECO = '>'
            elif arg == '-':
                self.verbose = 0
            elif arg == '+':
                self.out = sys.stderr
                self.verbose = 0
            elif arg == '++' or arg == 'log':
                self.verbose = 2
                self.log = open('log.csv', 'w')
            elif arg.startswith('-') and arg[1:].isdigit():
                self.nb_digits = int(arg[1:])
            elif arg.find('=', 1) > 0:
                k, v = self.try_assignment(arg, 0)
                values[k] = v
            elif arg:
                sys.stderr.write("Preconfig does not understand argument `%s'\n" % arg)
                sys.exit(4)
        
        # path argument may define the pattern:
        if path.find('%') >= 0 and not os.path.isfile(path):
            self.pattern = cannonical_pattern(path)
            path = ''

        if not inputs:
            sys.stderr.write("Preconfig expects an input template file\n")
            sys.exit(3)

        for i in inputs:
            #out.write("Reading %s\n" % i)
            with open(i, 'r') as f:
                res = self.parse(i, f, values, repeat, path)
            if self.verbose > 0:
                if len(res) == 1:
                    print("generated %s" % res[0])
                else:
                    print("%i files generated: %s ... %s" % (len(res), res[0], res[-1]))


#-------------------------------------------------------------------------------

def parse(name, values, repeat=1, path=''):
    """
    Process one file, and return the list of files generated
    """
    try:
        with open(name, 'r') as file:
            return Preconfig().parse(name, file, values, repeat, path)
    except FileNotFoundError:
        print("No such file `%s`" % name)
    return []


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You must specify a template file (for instructions, invoke with option '--help')")
    elif sys.argv[1].endswith("help"):
        print(__doc__)
    elif sys.argv[1]=='--version':
        print("This is PRECONFIG version %s (%s)" %(__VERSION__,__DATE__))
    elif sys.argv[1]=='--pipe':
        object=Preconfig()
        while 1:
            time.sleep(0.1)
            line = sys.stdin.readline()[:-1]
            if line:
                args = line.split(' ')
                object.main(args)
    else:
        object=Preconfig()
        object.main(sys.argv[1:])

