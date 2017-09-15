# PRECONFIG, a versatile configuration file generator

# Overview

Preconfig generates files from a template by evaluating doubly-bracketed Python code.

# Description

Preconfig reads a template file from top to bottom, identifying snippets
of code which are surrounded by double square brackets. It then executes this
code using the Python interpreter, proceeding recursively whenever multiple
values are specified. Values are eventually converted to their string
representation, and substituted in place of the code snippet. In this way,
Preconfig will generate all the possible combinations following the order in
which these combinations were specified in the file. Importantly, any
accompanying text in the template file is copied verbatim to the output file,
such that any syntax present in the configuration file can be maintained
during the process.

At least one template file should be specified, and other arguments are optional.
If several template files are specified, they will be processed sequentially.
The names of the produced files are built from the name of the template
by removing any second extension, and inserting an integer of constant width.

Examples:

- config.cym.tpl --> config0000.cym, config0001.cym, config0002.cym, etc.
- config.txt.tpl --> config0000.txt, config0001.txt, config0002.txt, etc.
- model.xml.tpl --> model0000.xml, model0001.xml, model0002.xml, etc.

The width of the variable part (default=4) can be changed on the command line.
For instance, to specify a width of 2, simply invoke "preconfig -2 ...".

# Syntax

    preconfig [OPTIONS] TEMPLATE_FILE [ADDITIONAL_TEMPLATE_FILES]

## Options

   - if a positive integer REPEAT is specified, each template file will be
   processed REPEAT times, for example: `preconfig 3 config.cym.tpl` will parse
   the template three times and generate three times more files.
   
   - if the path to an existing directory is specified, files will be created
   in this directory, for example: `preconfig dir config.cym.tpl`
   
   - DEFINITIONS can be specified on the command line as 'name=value' or 
   'name=sequence', with no space around the '='. They are added to the 
   dictionary used to evaluate the code snippets found inside the template file,
   for example: `preconfig n_molecules=100 config.cym.tpl`
   
   - if a negative integer is specified, this will set the width of the integer
   that is used to build the file namess.
   For example: `preconfig -2 config.cym.tpl` will create 'config00.cym', etc.
   
   - if a '-' is specified, all accessory output is suppressed
   
   - if a '+' is specified, more detailed information on the parsing is provided.
   
   - if '++' or 'log' is specified, a file 'log.csv' will be created containing one
   line for each file created, containing the substitutions operated for this file.
   
   - if '--help' is specified, this documentation will be printed.

## Code Snippets

Any plain python code can be embedded in the file, and functions from the
[Random Module](https://docs.python.org/library/random.html) can be used.
It is possible to use multiple bracketed expressions in the same file, and
to define variables in the python environment. An integer 'n', starting at
zero and corresponding to the file being generated is automatically defined.

### Example 1

Generate all combinations with multiple values for 2 parameters

    rate = [[ [1, 10, 100] ]]
    speed = [[ [-1, 0, 1] ]]

To generate the files, issue this command in the terminal:

`> preconfig config.cym.tpl`

In this case, Preconfig will generate 9 files.

### Example 2

Scan multiple parameters values randomly

    diffusion_rate = [[ random.uniform(0,1) ]]
    reaction_rate = [[ random.choice([1, 10, 100]) ]]
    abundance = [[ random.randint(0, 1000) ]]

`> preconfig 100 config.cym.tpl`

In this case, Preconfig is instructed to generate 100 files.

### Example 3

Regularly scan 2 parameters with 10 values each,
one according to a linear scale, and the other with a geometric scale

    [[ x = range(10) ]]
    [[ y = range(10) ]]
    reaction_rate = [[ 1 + 0.5 * x ]]
    diffusion_rate = [[ 1.0 / 2**y ]]

`> preconfig config.cym.tpl`

In this case, Preconfig will generate 100 files.

### Example 4

Randomize two parameters while keeping their ratio constant.

    [[ x = random.uniform(0,1) ]] 
    binding_rate = [[ 10.0 * x ]]
    unbinding_rate = [[ x ]]

`> preconfig 100 config.cym.tpl`

In this case, Preconfig is instructed to generate 100 files.

### Example 5
   
   Randomize one parameter, using 256 values in ascending order:
   
    [[ x = sorted([random.uniform(0.10, 0.25) for i in range(256)]) ]]
    binding_rate = [[ x ]]
   
   Command: `preconfig TEMPLATE_FILE`
   In this case, the number of files (256) is specified in the template

### Example 6

Boolean variables can be used to introduce qualitative differences:

    [[ enable = random.choice([0, 1]) ]]
    feeback = [[ random.uniform(0, 1) if (enable) else 0  ]]

`> preconfig 100 config.cym.tpl`

### Example 7
   
Randomize a value, and print this value as a comment in the file:
   
    [[ x = random.uniform(0,1) ]]% [[x]]
   
This sets a value for x, and print this value after '%',
In this case the '%' is used to indicate a comment, such that the line is skipped by
the simulation program that reads the file. However, the value can be read by any
analysis script that will later process the results of the simulation.
The value `x` can be used later:

    binding_rate = [[ 10*x ]]
    unbinding_rate = [[ 2*x ]]

To generate 256 files:

`> preconfig 256 TEMPLATE_FILE`


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

Your feedback is very much appreciated, please send it to:
feedback(xxx)cytosim.org

