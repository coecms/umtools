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

from .utils import mule_field_to_xarray
import climtas
import mule
from . import base
import argparse
import numpy


class RegridOp(mule.DataOperator):
    """
    Regrids fields from one UM file to another

    Call like::

        for a, b in zip(A.fields, B.fields):
            op([a, b])

    to regrid field 'b' to the grid of 'a', using metadata from 'a'

    All 'b' fields should be on the same grid as 'source_mask'
    All 'a' fields should be on the same grid as 'target_mask'
    """

    def __init__(self, target, source, mask_value=0, method="bilinear"):
        """

        Args:
            target: Mule field with the target grid
            source: Mule field with the source grid
            mask_value: If not None, only grid points where source/target don't match
                the mask value will be considered for regridding

        """
        self.source_da = mule_field_to_xarray(source)
        self.target_da = mule_field_to_xarray(target)

        self.shape = [target.lbrow, target.lbnpt]

        if mask_value is not None:
            self.source_da = self.source_da.where(self.source_da != mask_value)
            self.target_da = self.target_da.where(self.target_da != mask_value)

        if self.source_da.count() == 0:
            self.regrid = None
            return

        weights = climtas.regrid.esmf_generate_weights(
            self.source_da, self.target_da, method=method, extrap_method="nearestidavg"
        )

        self.regrid = climtas.regrid.Regridder(weights=weights)

    def new_field(self, source_field):
        field = source_field.copy()

        field.lbrow = self.shape[0]
        field.lbnpt = self.shape[1]

        return field

    def transform(self, source_field, new_field):

        da = mule_field_to_xarray(source_field)

        if self.regrid is not None:
            return self.regrid.regrid(da).values
        else:
            return numpy.zeros(self.shape)


def regrid(target, source):
    """
    Regrid the fields in 'source' to match the grid of 'target'
    """

    out = target.copy()

    op = RegridOp(target.fields[0], source.fields[0], mask_value=None)

    for f in source.fields:
        out.fields.append(op(f))

    return out


class Tool(base.Tool):
    """
    Regrid fields in a UM file
    """

    name = "regrid"
    help = "Regrid all UM fields"

    def parser_args(self, parser):
        parser.add_argument(
            "target",
            help="UM file on target grid (e.g. land mask)",
            type=argparse.FileType("r"),
        )
        parser.add_argument(
            "source", help="UM file with fields to regrid", type=argparse.FileType("r")
        )
        parser.add_argument("--output", help="Output UM file", required=True)

    def __call__(self, args):
        mf_target = mule.load_umfile(args.target)
        mf_source = mule.load_umfile(args.source)
        out = regrid(mf_target, mf_source)
        out.validate = lambda *args, **kwargs: None
        # utils.mule_write_with_replace(out, args.output)
        out.to_file(args.output)


if __name__ == "__main__":
    import argparse
    import os

    os.environ["UMDIR"] = "/projects/access/umdir"

    Tool().main()
