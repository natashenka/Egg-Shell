"""Main controller routines for the Ophis assembler.

    When invoked as main, interprets its command line and goes from there.
    Otherwise, use run_ophis(cmdline-list) to use it inside a script."""

# Copyright 2002-2012 Michael C. Martin and additional contributors.
# You may use, modify, and distribute this file under the MIT
# license: See README for details.

import sys
import os
import Frontend
import IR
import CorePragmas
import Passes
import Errors as Err
import Environment
import CmdLine
import Opcodes
import Tamagotchi


def run_all():
    """Transforms the source infiles to a binary outfile.

    Returns a shell-style exit code: 1 if there were errors, 0 if there
    were no errors.

    """
    Err.count = 0
    Tamagotchi.process(CmdLine.infiles)
    z = Frontend.parse(CmdLine.infiles)
    env = Environment.Environment()

    m = Passes.ExpandMacros()
    i = Passes.InitLabels()
    l_basic = Passes.UpdateLabels()
    l = Passes.FixPoint("label update", [l_basic],
                              lambda: not l_basic.changed)

    # The instruction selector is a bunch of fixpoints, and which
    # passes run depends on the command line options a bit.
    c_basic = Passes.Collapse()
    c = Passes.FixPoint("instruction selection 1", [l, c_basic],
                              lambda: not c_basic.changed)

    if CmdLine.enable_branch_extend:
        b = Passes.ExtendBranches()
        instruction_select = Passes.FixPoint("instruction selection 2",
                                                   [c, b],
                                                   lambda: not b.changed)
    else:
        instruction_select = c
    a = Passes.Assembler()

    passes = []
    passes.append(Passes.DefineMacros())
    passes.append(Passes.FixPoint("macro expansion", [m],
                                        lambda: not m.changed))
    passes.append(Passes.FixPoint("label initialization", [i],
                                        lambda: not i.changed))
    passes.extend([Passes.CircularityCheck(),
                   Passes.CheckExprs(),
                   Passes.EasyModes()])
    passes.append(instruction_select)
    passes.extend([Passes.NormalizeModes(),
                   Passes.UpdateLabels(),
                   a])

    for p in passes:
        p.go(z, env)

    if Err.count == 0:
        try:
            outfile = CmdLine.outfile
            if outfile == '-':
                output = sys.stdout
                if sys.platform == "win32":
                    # We can't dump our binary in text mode; that would be
                    # disastrous. So, we'll do some platform-specific
                    # things here to force our stdout to binary mode.
                    import msvcrt
                    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
            elif outfile is None:
                output = file('bin', 'wb')
            else:
                output = file(outfile, 'wb')
            f = open("template.txt", "rb")
            t = f.read()
            head = t[:0x40000]
            if (len("".join(map(chr, a.output))) > 0x400):
                print "too large"
                return 1
            tail = t[(0x40000 + len("".join(map(chr, a.output)))):]
            output.write(head + "".join(map(chr, a.output)) + tail)
            output.flush()
            if outfile != '-':
                output.close()
            return 0
        except IOError:
                print>>sys.stderr, "Could not write to " + outfile
                return 1
    else:
        Err.report()
        return 1


def run_ophis(args):
    CmdLine.parse_args(args)
    Frontend.pragma_modules.append(CorePragmas)

    if CmdLine.enable_undoc_ops:
        Opcodes.opcodes.update(Opcodes.undocops)
    elif CmdLine.enable_65c02_exts:
        Opcodes.opcodes.update(Opcodes.c02extensions)

    CorePragmas.reset()
    return run_all()


if __name__ == '__main__':
    sys.exit(run_ophis(sys.argv[1:]))
