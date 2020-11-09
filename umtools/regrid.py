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
    def __init__(self, target, source, mask_value=0, method='bilinear'):
        """

        Args:
            target: Mule field with the target grid
            source: Mule field with the source grid
            mask_value: If not None, only grid points where source/target don't match
                the mask value will be considered for regridding

        """
        self.source_da = mule_field_to_xarray(source)
        self.target_da = mule_field_to_xarray(target)

        print(self.source_da)
        print(self.target_da)

        if mask_value is not None:
            self.source_da = self.source_da.where(self.source_da != mask_value)
            self.target_da = self.target_da.where(self.target_da != mask_value)

        if self.source_da.count() == 0:
            self.regrid = None
            return

        self.source_da.to_netcdf('a.nc')

        weights = climtas.regrid.esmf_generate_weights(
                self.source_da,
                self.target_da,
                method=method,
                extrap_method='nearestidavg')

        self.regrid = climtas.regrid.Regridder(weights=weights)

    def new_field(self, source):
        source_field, data_field = source

        field = source_field.copy()
        return field

    def transform(self, source, new_field):
        source_field, data_field = source

        da = mule_field_to_xarray(data_field)

        if self.regrid is not None:
            return self.regrid.regrid(da).values
        else:
            return source_field.get_data() * 0


