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

import argparse
import textwrap

class Tool():
    """
    Base class for tools working with UM files, handles arguments etc.

    Users should replace parser_args, which adds argparse arguments, and
    __call__ which runs the tool, then add the subclass to the list in
    umtool.py
    """

    def __init__(self):
        pass

    def subparser(self, subp):
        parser = subp.add_parser(self.name, description=textwrap.dedent(self.__doc__), help=self.help, formatter_class = argparse.RawDescriptionHelpFormatter)
        self.parser_args(parser)
        parser.set_defaults(func=self)

    def main(self):
        parser = argparse.ArgumentParser(description=textwrap.dedent(self.__doc__),
            formatter_class = argparse.RawDescriptionHelpFormatter)
        self.parser_args(parser)

        args = parser.parse_args()

        self(args)

    def parser_args(self, parser):
        pass

    def __call__(self, args):
        pass
