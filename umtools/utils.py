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

import xarray
import numpy
from iris.fileformats.um_cf_map import STASH_TO_CF
import tempfile
import shutil

def mule_field_to_xarray(field):
    """
    Convert mule field 'field' to a Xarray DataArray
    """

    da = xarray.DataArray(field.get_data(), dims=['lat','lon'])
    da = da.where(da != field.bmdi)

    stash = f'm01s{field.lbuser4 // 1000:02d}i{field.lbuser4%1000:03d}'

    cf_info = STASH_TO_CF.get(stash)
    if cf_info is not None:
        if cf_info.standard_name is not None:
            da.attrs['standard_name'] = cf_info.standard_name
        if cf_info.long_name is not None:
            da.attrs['long_name'] = cf_info.long_name
        if cf_info.units is not None:
            da.attrs['units'] = cf_info.units

    da.attrs['STASH'] = stash
    da.attrs['lbuser4'] = field.lbuser4
    if field.stash is not None:
        da.attrs['stash_name'] = field.stash.name

    da.name = f'stash_{field.lbuser4}'

    da.coords['lon'] = ('lon', field.bzx + numpy.arange(1, da.shape[1]+1)*field.bdx)
    da.coords['lat'] = ('lat', field.bzy + numpy.arange(1, da.shape[0]+1)*field.bdy)

    da.coords['lat'].attrs = {
            'standard_name': 'latitude',
            'axis': 'Y',
            'units': 'degrees_north',
            }
    da.coords['lon'].attrs = {
            'standard_name': 'longitude',
            'axis': 'X',
            'units': 'degrees_east',
            }
    da.lat.encoding['_FillValue'] = None
    da.lon.encoding['_FillValue'] = None

    return da


def mule_write_with_replace(mf, path):
    """
    Safely write out a mule file when it potentially replaces itself
    """
    with tempfile.NamedTemporaryFile() as f:
        mf.to_file(f)

        shutil.copy2(f.name, path)

