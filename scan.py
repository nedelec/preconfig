#!/usr/bin/env python3
#
# scan.py executes a given command sequentially or in parallel, in specified directories
#
# Copyright  F. Nedelec and S. Dmitrieff; 2007--2022

"""
    Execute specified command in given directories, sequentially or in parallel,
    using independent threads.
 
Syntax:

    scan.py command [-][+] directory1 [directory2] [directory3] [...] [jobs=INTEGER]
    
    if '-' is specified, output is limited to what the command does
    if '+' is specified, the directory path is printed without decoration
    if 'jobs' is set, run in parallel using specified number of threads

Examples:
    
    scan.py 'play image' run*
    scan.py 'play image' run* jobs=2
    
    
F. Nedelec 02.2011, 09.2012, 03.2013, 01.2014, 06.2017, 07.2021, 21.03.2022, 8.04.2022
S. Dmitreff 06.2017
"""

try:
    import sys, os, subprocess
except ImportError:
    sys.stderr.write("Error: could not load necessary python modules\n")
    sys.exit()

err = sys.stderr
out = sys.stdout
verbose = 2

#------------------------------------------------------------------------

def assemble(path, lines, verb):
    """
    Assembles lines for output according to 'verb' argument
    """
    res = ''
    if verb == 2:
        for s in lines:
            res += s
    elif verb == 1:
        res = os.path.basename(path) + " "
        for s in lines:
            res += s.replace('\n', ' ')
        res += '\n'
    else:
        for s in lines:
            res += s
    return res


def execute(tool, path, verb):
    """
    run executable in specified directory
    """
    lines = []
    try:
        os.chdir(path)
        if verb == 2:
            sys.stderr.write('-  '*24+path+"\n")
        sub = subprocess.Popen(tool, shell=True, stdout=subprocess.PIPE)
        for s in sub.stdout:
            lines.append(s.decode())
        sub.stdout.close()
    except Exception as e:
        err.write("Error: %s\n" % repr(e))
    res = assemble(path, lines, verb)
    out.write(res)
    out.flush()


def worker(queue):
    """
    run executable taking argument from queue
    """
    while True:
        try:
            t, p, v = queue.get(True, 1)
        except:
            break;
        execute(t, p, v)


def main(args):
    """
        read command line arguments and process command
    """
    global verbose
    
    if args[0] == '-':
        verbose = 0
        args.pop(0)
    elif args[0] == '+':
        verbose = 1
        args.pop(0)
    
    try:
        tool = args[0]
    except:
        err.write("Missing command: scan.py command [-][+] directory1 [directory2]...\n")
        return 1

    njobs = 1
    paths = []
    for arg in args[1:]:
        [key, equal, val] = arg.partition('=')
        if os.path.isdir(arg):
            paths.append(os.path.abspath(arg))
        elif key == 'nproc' or key == 'njobs' or key == 'jobs':
            njobs = int(val)
        elif arg == '-':
            verbose = 0
        elif arg == '+':
            verbose = 1
        else:
            err.write("  Warning: unexpected argument `%s'\n" % arg)
            sys.exit()

    if not paths:
        err.write("Missing directories: scan.py command [-][+] directory1 [directory2]...\n")
        err.write(" (scan.py would execute `%s`)\n"%tool)
        return 2
    
    njobs = min(njobs, len(paths))
    
    if njobs > 1:
        #process in parallel with child threads:
        try:
            from multiprocessing import Process, Queue
            queue = Queue()
            for p in paths:
                queue.put((tool, p, verbose))
            jobs = []
            for n in range(njobs):
                j = Process(target=worker, args=(queue,))
                jobs.append(j)
                j.start()
            # wait for completion of all jobs:
            for j in jobs:
                j.join()
            return 0
        except ImportError:
            err.write("Warning: multiprocessing module unavailable\n")
    #process sequentially:
    for p in paths:
        execute(tool, p, verbose)
    return 0

#------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1].endswith("help"):
        print(__doc__)
    else:
        main(sys.argv[1:])
