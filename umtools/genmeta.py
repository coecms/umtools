#!/usr/bin/env python
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

from iris.fileformats.um_cf_map import STASH_TO_CF
from yaml import dump, CDumper as Dumper
from stashvar import atm_stashvar

stashmeta = '/scratch/access/umdir/vn11.5/ctldata/STASHmaster/STASHmaster-meta.conf'

def standard_meta():
    meta = {}

    for line in open(stashmeta):
        line = line.strip()
        
        if line.startswith('['):
            section = line[len('[stashmaster:'):-1]
            meta[section] = {}
            continue

        parts = line.split('=')
        if len(parts) == 1:
            continue

        if parts[0] != '':
            key = 'stash_' + parts[0]
            meta[section][key] = parts[1]
        else:
            meta[section][key] += "\n" + parts[1]

    codes = {}

    for key, value in meta.items():
        if key.startswith('code('):
            lbuser4 = int(key[len('code('):-1])

            stash = f'm01s{lbuser4//1000:02d}i{lbuser4%1000:03d}'
            codes[stash] = value

            short_name = atm_stashvar.get(lbuser4, ["","","","",""])[1] 
            if short_name != "":
                codes[stash]['var_name'] = short_name
            short_name = atm_stashvar.get(lbuser4, ["","","","",""])[4]
            if short_name != "":
                codes[stash]['var_name'] = short_name

    return codes

if __name__ == '__main__':
    print(dump(codes, Dumper=Dumper))
