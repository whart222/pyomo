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
# Problem Writer for LP Format Files using POEK
#

import logging
from pyomo.opt.base import AbstractProblemWriter, WriterFactory
try:
    import poek
    poek_available=True
except ImportError:
    poek_available=False

logger = logging.getLogger('pyomo.core')


class ProblemWriter_poeklp(AbstractProblemWriter):

    def __init__(self):

        AbstractProblemWriter.__init__(self, ProblemFormat.cpxlp)

        # The LP writer tracks which variables are
        # referenced in constraints, so that a user does not end up with a
        # zillion "unreferenced variables" warning messages.
        # This dictionary maps id(_VarData) -> _VarData.
        self._referenced_variable_ids = {}

    def __call__(self,
                 model,
                 output_filename,
                 solver_capability,
                 io_options):

        # Make sure not to modify the user's dictionary,
        # they may be reusing it outside of this call
        io_options = dict(io_options)

        if len(io_options):
            raise ValueError(
                "ProblemWriter_cpxlp passed unrecognized io_options:\n\t" +
                "\n\t".join("%s = %s" % (k,v) for k,v in iteritems(io_options)))

        poek = pyomo_to_poek(model, self._referenced_variable_ids)
        poek.write(output_filename)


if poek_available:
    ProblemWriter_poeklp = WriterFactory.register('poeklp', 'Generate the corresponding LP file using POEK')(ProblemWriter_poeklp)