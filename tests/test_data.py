# Copyright 2011 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from pprint import pprint # UNDONE

from os import path
import sys
import unittest

import splunk.data as data

class TestCase(unittest.TestCase):
    def test_elems(self):
        result = data.load("")
        self.assertTrue(result is None)

        result = data.load("<a></a>")
        self.assertTrue(result is None) # UNDONE: BUG: Should be {}

        result = data.load("<a>1</a>")
        self.assertEqual(result, '1') # UNDONE: BUG: Should be {'$text': '1'}

        result = data.load("<a><b></b></a>")
        self.assertEqual(result, {'b': None})

        result = data.load("<a><b>1</b></a>")
        self.assertEqual(result, {'b': '1'})

        result = data.load("<a><b></b><b></b></a>")
        self.assertEqual(result, {'b': [None, None]})

        result = data.load("<a><b>1</b><b>2</b></a>")
        self.assertEqual(result, {'b': ['1', '2']})

        result = data.load("<a><b></b><c></c></a>")
        self.assertEqual(result, {'b': None, 'c': None})

        result = data.load("<a><b>1</b><c>2</c></a>")
        self.assertEqual(result, {'b': '1', 'c': '2'})

        result = data.load("<a><b><c>1</c></b></a>")
        self.assertEqual(result, {'b': {'c': '1'}})

        result = data.load("<a><b><c>1</c></b><b>2</b></a>")
        self.assertEqual(result, {'b': [{'c': '1'}, '2']})

    def test_attrs(self):
        result = data.load("<e a1='v1'/>")
        self.assertEqual(result, {'a1': 'v1'})

        result = data.load("<e a1='v1' a2='v2'/>")
        self.assertEqual(result, {'a1': 'v1', 'a2': 'v2'})

        result = data.load("<e a1='v1'>v2</e>")
        self.assertEqual(result, {'$text': 'v2', 'a1': 'v1'})

        result = data.load("<e a1='v1'><b>2</b></e>")
        self.assertEqual(result, {'a1': 'v1', 'b': '2'})

        result = data.load("<e a1='v1'>v2<b>bv2</b></e>")
        self.assertEqual(result, {'a1': 'v1', 'b': 'bv2'})
        # UNDONE: BUG: Dropping v2, incorrect mixed content

        result = data.load("<e a1='v1'><a1>v2</a1></e>")
        self.assertEqual(result, {'a1': 'v1'})
        # UNDONE: BUG: Should be an array

    def test_real(self):
        testdir = path.dirname(path.abspath(__file__))

        fh = open(path.join(testdir, "services.xml"), 'r')
        result = data.load(fh.read())
        self.assertTrue(result.has_key('author'))
        self.assertTrue(result.has_key('entry'))
        titles = [item.title for item in result.entry]
        self.assertEqual(
            titles,
            ['alerts', 'apps', 'authentication', 'authorization', 'data',
             'deployment', 'licenser', 'messages', 'configs', 'saved',
             'scheduled', 'search', 'server', 'streams', 'broker', 'clustering',
             'masterlm'])

        fh = open(path.join(testdir, "services.server.info.xml"), 'r')
        result = data.load(fh.read())
        self.assertTrue(result.has_key('author'))
        self.assertTrue(result.has_key('entry'))
        self.assertEqual(result.title, 'server-info')
        self.assertEqual(result.author.name, 'Splunk')
        self.assertEqual(result.entry.content.cpu_arch, 'i386')
        self.assertEqual(result.entry.content.os_name, 'Darwin')
        self.assertEqual(result.entry.content.os_version, '10.8.0')

if __name__ == "__main__":
    unittest.main()

