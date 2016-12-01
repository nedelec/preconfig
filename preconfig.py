#!/usr/bin/env python
#
# PRECONFIG, a versatile configuration file generator
#
# Copyright Francois J. Nedelec, EMBL 2010--2016
# Last modified on 1.12.2016

"""
# Synopsis

   Generates files from a template by evaluating doubly-bracketed python code.

# Syntax:

   preconfig.py [OPTIONS] TEMPLATE_FILE [ADDITIONAL_TEMPLATE_FILES]
   
# Description
   
   preconfig.py reads the template file from top to bottom, identifying snippets
   of code which are surrounded by double square brackets. It then executes this
   code using the python interpreter, forking recursively whenever multiple
   values are specified. Values are eventually converted to their string
   representation, and substituted in place of the code snippet. In this way,
   preconfig will generate all the possible combinations following the order in
   which these combinations were specified in the file. Importantly, any ac-
   -companying text in the template file is copied verbatim to the output file,
   such that any syntax present in the configuration file can be maintained
   during the process.
   
# Usage

   At least one template file should be specified, and other arguments are optional.
   If several template files are specified, they will be processed sequentially.
   The names of the produced files are built from the name of the template
   by removing any second extension, and inserting an integer of constant-width.
   
   For examples:
   
   - config.cym.tpl --> config0000.cym, config0001.cym, config0002.cym, etc.
   - config.txt.tpl --> config0000.txt, config0001.txt, config0002.txt, etc.
   - model.xml.tpl --> model0000.xml, model0001.xml, model0002.xml, etc.
   
   The width of the variable part (default=4) can be specified as an option (eg "-3").
   
# OPTIONS
   
   - if a positive integer REPEAT is specified, each template file will be
   processed REPEAT times, for example: `preconfig 3 config.cym.tpl` will parse
   the template three times and generate three times more files.
   
   - if the name of an existing directory is specified, files will be created
   in this directory, for example: `preconfig config_dir config.cym.tpl`
   
   - DEFINITIONS can be specified on the command line as 'name=value' or 
   'name=sequence', with no space around the '='. They are added to the 
   dictionary used to evaluate the code snippets found inside the template file,
   for example: `preconfig n_molecules=100 config.cym.tpl`
   
   - if a negative integer is specified, this will affect the naming of the files,
   for example: `preconfig -3 config.cym.tpl` will create 'config001.cym', etc.
   
   - if a '-' is specified, this will suppress all accessory output
   
   - if a '+' is specified, more detailed information on the parsing is provided.
   
   - if 'log' is specified, a file 'log.csv' will be created containing one line
   for each file made, with a list of substitutions operated for this file.
   
   - if 'help' is specified, this documentation will be printed.
   
# CODE SNIPPETS
   
   Any plain python code can be embedded in the file, and functions from the
   [Random Module](https://docs.python.org/library/random.html) can be used.
   It is possible to use multiple bracketed expressions in the same file, and
   to define variables in the python environment. An integer 'n', starting at
   zero and corresponding to the file being generated is automatically defined.
   
##Example 1
   
   Generate all combinations with multiple values for 2 parameters
   
    rate = [[ [1, 10, 100] ]]
    speed = [[ [-1, 0, 1] ]]
   
   Command: `preconfig.py config.cym.tpl`
   
##Example 2

   Scan multiple parameters values randomly
   
    diffusion_rate = [[ random.uniform(0,1) ]]
    reaction_rate = [[ random.choice([1, 10, 100]) ]]
    abundance = [[ random.randint(0, 1000) ]]
   
   Command: `preconfig.py 100 config.cym.tpl`
   
##Example 3
   
   Regularly scan 2 parameters with 10 values each,
   one according to a linear scale, and the other with a geometric scale
   
    [[ x = range(10) ]]
    [[ y = range(10) ]]
    reaction_rate = [[ 1 + 0.5 * x ]]
    diffusion_rate = [[ 1.0 / 2**y ]]
   
   Command: `preconfig.py config.cym.tpl`
   
##Example 4
   
   Randomize two parameters while keeping their ratio constant.
   
    [[ x = random.uniform(0,1) ]]
    binding_rate = [[ 10.0 * x ]]
    unbinding_rate = [[ x ]]
   
   Command: `preconfig.py 100 config.cym.tpl`
   
##Example 5
   
   Generate piecewise linear distributions with conditional expressions
   
    [[ x = random.uniform(1,10) ]]
    diffusion_rate = [[ x ]]
    reaction_rate = [[ 5-x if x < 5 else x-5 ]]
   
   Command: `preconfig.py 100 config.cym.tpl`
   
##Example 6
   
   Randomize a value, and print this value as a comment in the file.
   The second line below constructs a string, from the value of 'x'.
   
    [[ x = random.uniform(0,1) ]]
    [[ "%set x= " + str(x) ]]
   
   Command: `preconfig.py 100 config.cym.tpl`

Francois J. Nedelec, 2010--2016
"""


import sys

try:
    import os, io
    libraries = { 'random': __import__('random'), 'math': __import__('math') }
except ImportError:
    sys.stderr.write("Error: preconfig could not load necessary python modules\n")
    sys.exit()

#-------------------------------------------------------------------------------

# code snippets are surrounded by double square brackets:
CODE_IN = '['
CODE_OUT = ']'

# all output is hidden by default:
out = open(os.devnull, 'w')
log = []

# directory in which files are generated:
target_dir = ''

# motif used for make file names
name_motif = 'config%04i.txt'

# number of digits used in name_motif
nb_digits = 4

# index of file being generated
file_index = 0

#list of files generated
files_made = []

#current file in process
template_name = ''

#-------------------------------------------------------------------------------

def set_name_motif(name):
    """
        Extract the root and the extension of the file
        """
    global file_motif, nb_digit, target_dir
    file = os.path.basename(name)
    [main, ext] = os.path.splitext(file)
    if '.' in main:
        [main, ext] = os.path.splitext(main)
    file_motif = main + '%0' + str(nb_digits) + 'i' + ext;
    if target_dir:
        file_motif = os.path.join(target_dir, file_motif)


def next_file_name():
    """
        Generate the name of the next output file
        """
    global file_index, file_motif
    n = file_motif % file_index
    file_index += 1
    return n


def make_file(text, values):
    """
        Create a file with the specified text
        """
    global files_made, file_index
    fname = next_file_name()
    file = open(fname, 'w')
    file.write(text)
    file.close()
    files_made.extend([fname]);
    # fancy ouput:
    out.write("\\"+repr(values)+'\n')
    out.write(" \\"+('> '+fname).rjust(78, '-')+'\n')
    # write log:
    if log:
        keys = sorted(values.keys())
        if file_index == 1:
            log.write('%20s' % 'file')
            for k in keys:
                log.write(', %10s' % k)
            log.write('\n')
        log.write('%20s' % fname)
        for k in keys:
            log.write(', %10s' % repr(values[k]))
        log.write('\n')
    values['n'] = file_index


#-------------------------------------------------------------------------------

def pop_sequence(dic):
    """
        Remove an entry in the dictionary that has multiple values
    """
    for k in dic:
        v = dic[k]
        try:
            len(v)
            if not isinstance(v, str):
                dic.pop(k)
                return (k, v)
        except:
            pass
    return ('', [])


def try_assignment(cmd):
    """
        Try to evaluate `cmd` as a variable assignent,
        and if that succeeds, expand dictionary`values`
    """
    [k, e, v] = cmd.partition('=')
    if k and v and e=='=':
        k = k.strip()
        v = v.strip()
        return (k, v)
    return ('', cmd)


def evaluate(cmd, values):
    """
        Evaluate `cmd` and return the result
    """
    res = cmd
    try:
        res = eval(cmd, libraries, values)
    except Exception as e:
        sys.stderr.write("\033[95m")
        sys.stderr.write("Error in file `%s`:\n" % template_name)
        sys.stderr.write("\033[0m")
        sys.stderr.write("    Could not evaluate [[%s]]\n" % cmd)
        sys.stderr.write("    "+str(e)+'\n')
    return res


def get_block(file, s, e):
    """
    Extract the next block starting with DOUBLE delimiters 'ss' and ending with 'ee'
    Returns a set with 3 values:
        - the text found before the block
        - the block with its delimiters
        - EOF (True or False)
    """
    ch = file.read(1)
    pre = ''
    blk = ''
    dep1 = (ch==s)
    dep2 = 0
    while ch:
        pc = ch
        ch = file.read(1)
        if not ch:
            break;
        if ch == s:
            dep1 += 1
            if pc == s:
                dep2 = 1
        if dep2:
            blk += pc
        else:
            pre += pc
        #print("%c dep1 %i dep2 %i" %(ch, dep1, dep2))
        if ch == e:
            dep1 -= 1
            if dep1 < 0:
                out.write("Error: unbalanced brackets\n");
            if pc == e and dep1 == 0:
                return (pre, blk+ch, False)
    if blk:
        out.write("Error: EOF encoutered within bracketted block\n");
    return (pre, '', True)


#-------------------------------------------------------------------------------

def process(ifile, values, text):
    """
        process() will identify and substitute bracketed code blocks
        embedded in the input file, and generate a file at EOF.
    """
    output = text

    while ifile:
        (pre, code, eof) = get_block(ifile, CODE_IN, CODE_OUT)
        #print("text `", pre[0:32], "' of size ", len(pre))
        #print("code [[", code, "]]", eof)
        output += pre
        if eof:
            # having exhausted the input, we generate a file:
            make_file(output, values)
            return
        # remove outer brackets:
        cmd = code[2:-2]
        #print("embedded code '%s'" % code)
        # interpret command:
        (key, vals) = try_assignment(cmd)
        vals = evaluate(vals, values)
        #print("key", key, "values", vals)
        try:
            # use 'pop()' to test if multiple values were specified...
            # keep last value aside for later:
            val = vals.pop()
            ipos = ifile.tell()
            for v in vals:
                # fork recursively for all subsequent values:
                #print("forking", v)
                if key:
                    values[key] = v
                    out.write("|%50s <-- %s\n" % (key, str(v)) )
                    process(ifile, values, output)
                else:
                    out.write("|%50s --> %s\n" % (code, str(v)) )
                    process(ifile, values, output+str(v))
                ifile.seek(ipos)
        except (AttributeError, IndexError):
            # a single value was specified:
            val = vals
        # handle remaining value:
        # print("handling", key, val)
        if key:
            values[key] = val
            out.write("|%50s <-- %s\n" % (key, str(val)) )
        else:
            output += str(val)
            out.write("|%50s --> %s\n" % (code, str(val)) )



def expand_values(ifile, values, text):
    """
        Call self recursively to remove all entries of the dictionary
        'values' that are associated with multiple keys
    """
    (key, vals) = pop_sequence(values)
    if key:
        ipos = ifile.tell()
        for v in vals:
            values[key] = v
            #out.write("|%50s <-- %s\n" % (key, str(v)) )
            expand_values(ifile, values, text)
            ifile.seek(ipos)
        # restore multiple values on upward recursion
        values[key] = vals
    else:
        process(ifile, values, text)


def parse(iname, values={}, repeat=1):
    """
        process one file, and return the list of files generated
    """
    values['n'] = 0
    global files_made, template_name
    set_name_motif(iname)
    files_made = []
    template_name = iname
    for x in range(repeat):
        f = open(iname, 'r')
        expand_values(f, values, '')
        f.close()
    return files_made


#-------------------------------------------------------------------------------


def main(args):
    global out, log, nb_digits, target_dir
    inputs = []
    values = {}
    repeat = 1
    verbose = 1
    
    for arg in args:
        if os.path.isdir(arg):
            target_dir = arg
        elif os.path.isfile(arg):
            inputs.append(arg)
        elif arg.isdigit():
            repeat = int(arg)
        elif arg == '-':
            verbose = 0
        elif arg == '+':
            out = sys.stderr
            verbose = 0
        elif arg == 'log':
            log = open('log.csv', 'w')
        elif arg[0] == '-' and arg[1:].isdigit():
            nb_digits = int(arg[1:])
        else:
            (k,v)=try_assignment(arg)
            if k:
                values[k] = evaluate(v, values)
            else:
                sys.stderr.write("  Error: unexpected argument `%s'\n" % arg)
                sys.exit()
    
    if not inputs:
        sys.stderr.write("  Error: you must specify an input template file\n")
        sys.exit()

    for i in inputs:
        #out.write("Reading %s\n" % i)
        res = parse(i, values, repeat)
        if verbose == 1:
            #print("%i files generated from %s:" % (len(res), i))
            for f in res:
                print(f)


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1]=='help':
        print(__doc__)
    else:
        main(sys.argv[1:])


