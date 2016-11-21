# PRECONFIG, a versatile configuration file generator

# Overview

preconfig.py is a python program used to vary parameter values in files.

# Requirements

A template file, and the [python](https://www.python.org) interpreter

# Syntax

    preconfig.py [OPTIONS] TEMPLATE_FILE [ADDITIONAL_TEMPLATE_FILES]

# Description

  preconfig.py reads the template file from top to bottom, identifying snippets 
  of code which are surrounded by double square brackets. It then executes this  
  code using the python interpreter, and will fork recursively whenever multiple 
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

##OPTIONS

- if a positive integer REPEAT is specified, each template file will be 
  processed REPEAT times, for example: `preconfig 3 config.cym.tpl`

- if the name of an existing directory is specified, files will be created 
  in this directory, for example: `preconfig config_dir config.cym.tpl`

- DEFINITIONS can be specified on the command line as 'name=value' or 
  'name=sequence', with no space around the '='. They are added to the 
  dictionary used to evaluate the code snippets found inside the template file,
  for example: `preconfig n_molecules=100 config.cym.tpl`

- if a negative integer is specified, this will affect the naming of the files,
  for example: `preconfig -3 config.cym.tpl`

- if a '-' is specified, this will suppress all accessory output

- if a '+' is specified, more detailed information on the parsing is provided.

- if 'log' is specified, a file 'log.csv' will be created containing parameter
  values for each file made.

- if 'help' is specified, this documentation will be printed.

##CODE SNIPPETS

The variations to be applied are specified within double squared brackets
in the template file. Any plain python code can used, including functions from
the [Random Module](https://docs.python.org/library/random.html). 
It is possible to use multiple bracketed expressions in the same file, and 
to define variables in the python environment. An integer 'n', starting at 
zero and corresponding to the file being generated is automatically defined.


###Example 1

Generate all combinations with multiple values for 2 parameters

    rate = [[ [1, 10, 100] ]]
    speed = [[ [-1, 0, 1] ]]

Command: `preconfig.py config.cym.tpl`


###Example 2
Scan multiple parameters values randomly

    diffusion_rate = [[ random.uniform(0,1) ]]
    reaction_rate = [[ random.choice([1, 10, 100]) ]]
    abundance = [[ random.randint(0, 1000) ]]

Command: `preconfig.py 100 config.cym.tpl`


###Example 3

Regularly scan 2 parameters with 10 values each,
one according to a linear scale, and the other with a geometric scale

    [[ x = range(10) ]]
    [[ y = range(10) ]]
    reaction_rate = [[ 1 + 0.5 * x ]]
    diffusion_rate = [[ 1.0 / 2**y ]]

Command: `preconfig.py config.cym.tpl`

###Example 4

Randomize two parameters while keeping their ratio constant.

    [[ x = random.uniform(0,1) ]] 
    binding_rate = [[ 10.0 * x ]]
    unbinding_rate = [[ x ]]

Command: `preconfig.py 100 config.cym.tpl`


###Example 5

Generate unconventional distributions with conditional expressions

    [[ x = random.uniform(1,10) ]]
    diffusion_rate = [[ x ]]
    reaction_rate = [[ 5-x if x < 5 else x-5 ]]

Command: `preconfig.py 100 config.cym.tpl`


###Example 6

Randomize a value, and print this value as a comment in the file.

    [[ x = random.uniform(0,1) ]]
    [[ "%set x= " + str(x) ]]

Command: `preconfig.py 100 config.cym.tpl`


# Testing

We provide three type of template files to test `preconfig.py`:

- [Cytosim](www.cytosim.org) configuration files: `config?.cym.tpl`
- [Smoldyn](www.smoldyn.org) configuration file: `smoldyn.txt.tpl`
- [BioModel](www.biomodels.org) XML configuration file: `BioModel.xml.tpl`

To test them, please enter the following commands, one by one:

    preconfig.py configA.cym.tpl
    preconfig.py configB.cym.tpl 16
    preconfig.py configC.cym.tpl
    preconfig.py smoldyn.txt.tpl
    preconfig.py BioModel.xml.tpl

# Credits & Licence

Francois J. Nedelec, 2010--2016.  
preconfig.py is distributed under GPL3.0 Licence (see LICENCE.md)

# Feedback

Your feedback is very much appreciated, please send it to:
francois.nedelec@embl.de

