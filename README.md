# PRECONFIG, a versatile configuration file generator

# Overview

Preconfig generates multiple files from a single template,
where variations are specified within doubly-bracketed Python code, for example:

	rate = [[ [1, 10, 100] ]]

Preconfig is Open Source and free to use and has no other dependency than Python itself.

# Description

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

# Syntax

From the command line:

	preconfig [OPTIONS] [DEFINITIONS] TEMPLATE_FILE [ADDITIONAL_TEMPLATE_FILES]

# Options

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
   
# Definitions

   Variables can be defined on the command line as 'name=value', with no space 
   around the '='. They are added to the dictionary used to evaluate the code 
   snippets found inside the template file.
   example: `preconfig rate=100 config.cym.tpl`

   Sequences can be defined as 'name=sequence' or 'name==sequence'. In the first
   instance, the sequence is expanded, generating new files for each value.
   However, using '==' prevents this expansion, and the variable is used verbatim.
   example: `preconfig rate=[1,10,100] config.cym.tpl`

# Code snippets

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

   Quotations can be used to aggregate values:

    [[ vec = ['-1 0 1', '0 1 1', '-1 0 -1'] ]]
    new microtubule
    {
        position = [[vec]]
    }

## Example 8

   Cartesian sampling with filtering:

    [[ (x,y) = [ (x,y) for x in range(10) for y in range(10) if x>y ] ]]

    new particle
    {
        position = [[x]] [[y]]
    }

## Keeping track of values and extracting them later

It is often useful to add comments in the ouput file to help recover the
values generated by Preconfig. This is easily done as follows:

    [[ x = random.uniform(0,1) ]]%config.x = [[ x ]]
    
...
This will be replaced by preconfig producing:
	
	%config.x = 2.452
 
The '%' indicates a comment and the line will be ignored by Cytosim,
but it then easy to recover all lines containing 'config.' with `grep`:

    grep '^%config.' config0000.cym
One may also use 'awk':
    awk '/%config./{sub("%config.","");print}' config0000.cym
    
The same technique can be adapted to import the parameter into Python:
        
    def read_metadata(filename, pattern='config.'):
        res = dict()
        with open(filename, 'r') as f:
            for line in f:
                s = line.find(pattern)
                if s > 0:
                    s += len(pattern)
                    code = line[s:-1].rstrip(';')
                    [k, _, v] = code.partition('=')
                    try:
                        v = float(v)
                        if v == int(v):
                            v = int(v)
                    except:
                        pass
                    if k:
                        res[k] = v
        return res

# Tutorial

To use Preconfig, follow this steps:

- copy a configuration file and add '.tpl' to the name (`cp config.cym config.cym.tpl`)
- edit the template file you created, to add some double bracketed snippets,
  following the examples above.
- run Preconfig (`preconfig config.cym.tpl`)
- invoke your favorite simulation tool with each file (e.g. with the UNIX command [xargs](https://en.wikipedia.org/wiki/Xargs))

# Requirements

A template file, and the [Python](https://www.python.org) interpreter

# Testing

We provide three type of template files to test Preconfig:

- [Cytosim](www.cytosim.org) configuration files: `config?.cym.tpl`
- [Smoldyn](www.smoldyn.org) configuration file: `smoldyn.txt.tpl`
- [BioModel](www.biomodels.org) XML configuration file: `BioModel.xml.tpl`

To test them, please enter the following commands, one by one:

    preconfig configA.cym.tpl
    preconfig configB.cym.tpl 16
    preconfig configC.cym.tpl
    preconfig smoldyn.txt.tpl
    preconfig BioModel.xml.tpl

# Credits & Licence

We wish to thank the members of the Nedelec group, and all users of 
Cytosim for their feedback which has contributed greatly to this development.
We also thank Shaun Jackman and Steven Andrews for valuable feedback!

Copyright Francois J. Nedelec, 2010--2017.

This is Free Software with absolutely no WARRANTY.

Preconfig is distributed under GPL3.0 Licence (see LICENSE)

# Feedback

Your feedback is very much appreciated, please write to `feedback(xxx)cytosim.org`

