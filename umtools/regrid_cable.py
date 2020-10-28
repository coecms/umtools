#!/g/data/hh5/public/apps/nci_scripts/python-analysis3
# Copyright 2020 Scott Wales
# author: Scott Wales <scott.wales@unimelb.edu.au>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mule
from regrid import RegridOp
import base
import argparse


def regrid_cable(mf_target, mf_source):
    """
    Create a copy of mf_target, but with CABLE fields (STASH 800-900) regridded
    from mf_source
    """
    out = mf_target.copy()

    for f in mf_target.fields:
        if f.lbuser4 == 30:
            target_mask = f
            break

    for f in mf_source.fields:
        if f.lbuser4 == 30:
            source_mask = f
            break

    regrid_ops = []

    source_fields = []
    for f in mf_source.fields:
        if f.lbuser4 > 800 and f.lbuser4 < 900:
            source_fields.append(f)

        if f.lbuser4 == 801:
            regrid_ops.append(RegridOp(target_mask, f, mask_value=0))


    for f in mf_target.fields:
        if f.lbuser4 > 800 and f.lbuser4 < 900:
            source = source_fields.pop(0)

            op = regrid_ops[f.lbuser5-1]
            regridded = op([f, source])
            out.fields.append(regridded)
        else:
            out.fields.append(f)

    return out


class Tool(base.Tool):
    """
    Regrid the CABLE fields in an ACCESS-CM2 restart

    For most fields the UM reconfiguration accurately regrids, but specifics of
    CABLE implementation prevent this for STASH fields 800-899. This tool regrids
    these fields from a SOURCE UM file, with the remaining fields coming from TARGET
    (which is presumably the output of running the reconfiguration on SOURCE).
    """

    name = 'regrid_cm2_cable'
    help = 'Regrid ACCESS-CM2 CABLE fields'

    def parser_args(self, parser):
        parser.add_argument("target", help="Input UM file", type=argparse.FileType("r"))
        parser.add_argument("source", help="UM file with fields to regrid", type=argparse.FileType("r"))
        parser.add_argument("--output", help="Output UM file", required=True)

    def __call__(self, args):
        mf_target = mule.load_umfile(args.target)
        mf_source = mule.load_umfile(args.source)
        out = regrid_cable(mf_target, mf_source)
        out.to_file(args.output)



if __name__ == "__main__":
    import argparse
    import os
    os.environ['UMDIR'] = '/projects/access/umdir'

    Tool().main()
