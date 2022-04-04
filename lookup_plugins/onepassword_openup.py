# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Scott Buchanan <sbuchanan@ri.pn>
# Copyright: (c) 2016, Andrew Zenk <azenk@umn.edu> (lastpass.py used as starting point)
# Copyright: (c) 2018, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: onepassword
    author:
      - Scott Buchanan (@scottsb)
      - Andrew Zenk (@azenk)
      - Sam Doran (@samdoran)
    requirements:
      - C(op) 1Password command line utility. See U(https://support.1password.com/command-line/)
    short_description: fetch field values from 1Password
    description:
      - C(onepassword) wraps the C(op) command line utility to fetch specific field values from 1Password.
    options:
      _terms:
        description: identifier(s) (UUID, name, or subdomain; case-insensitive) of item(s) to retrieve.
        required: True
      field:
        description: field to return from each matching item (case-insensitive).
        default: 'password'
      section:
        description: Item section containing the field to retrieve (case-insensitive). If absent will return first match from any section.
      domain:
        description: Domain of 1Password. Default is U(1password.com).
        version_added: 3.2.0
        default: '1password.com'
        type: str
      subdomain:
        description: The 1Password subdomain to authenticate against.
      vault:
        description: Vault containing the item to retrieve (case-insensitive). If absent will search all vaults.
    notes:
      - This lookup will only use an existing 1Password session. It assumes you have already
        performed an initial sign in (meaning C(~/.op/config exists))
      - Tested with C(op) version 2.0.0
'''

EXAMPLES = """
# These examples only work when already signed in to 1Password
- name: Retrieve password for KITT when already signed in to 1Password
  ansible.builtin.debug:
    var: lookup('onepassword-openup', 'productname-{{ env }}', 'KITT')
- name: Retrieve password for Wintermute when already signed in to 1Password
  ansible.builtin.debug:
    var: lookup('onepassword-openup', 'productname-{{ env }}', 'Tessier-Ashpool', section='Wintermute')
- name: Retrieve username for HAL when already signed in to 1Password
  ansible.builtin.debug:
    var: lookup('onepassword-openup', 'Discovery', 'HAL 9000', field='username')
"""

RETURN = """
  _raw:
    description: field data requested
    type: list
    elements: str
"""

import errno
import json
import os

from subprocess import Popen, PIPE

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleLookupError, AnsibleError
from ansible.module_utils.common.text.converters import to_bytes, to_text


class OnePass(object):

    def __init__(self, path='op'):
        self.cli_path = path
        self.get_version()
        if self.cli_version >= 2:
            config_path = '~/.config/op/config'
        else:
            config_path = '~/.op/config'
        self.config_file_path = os.path.expanduser(config_path)
        self.logged_in = False
        self.token = None
        self.subdomain = None
        self.domain = None

    def get_version(self):
        # Get the 1password cli version
        try:
            rc, out, err = self._run(['--version'], ignore_errors=True)
            self.cli_version = int(to_text(out).split('.')[0])
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise AnsibleLookupError("1Password CLI tool '%s' not installed in path on control machine" % self.cli_path)
            raise e

    def assert_logged_in(self):
        try:
            if self.cli_version >= 2:
                args = ['account', 'get']
            else:
                args = ['get', 'account']
            rc, out, err = self._run(args, ignore_errors=True)
            if rc == 0:
                self.logged_in = True
            else:
                raise AnsibleError("Error getting 1password account from op command.")
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise AnsibleLookupError("1Password CLI tool '%s' not installed in path on control machine" % self.cli_path)
            raise e

    def get_raw(self, item_id, vault=None, field=None):
        if self.cli_version >= 2:
            args = ["item", "get", "--format=json", "--no-color"]
            if field:
                args += ['--fields', 'label={0}'.format(field)]
        else:
            args = ["get", "item"]
        args += [item_id]
        if vault is not None:
            args += ['--vault={0}'.format(vault)]
        if not self.logged_in:
            args += [to_bytes('--session=') + self.token]
        rc, output, dummy = self._run(args)
        return output

    def get_field(self, item_id, field, section=None, vault=None):
        output = self.get_raw(item_id, vault, field)
        if self.cli_version >= 2:
            return json.loads(output).get('value')
        else:
            return self._parse_field(output, field, section) if output != '' else ''

    def _run(self, args, expected_rc=0, command_input=None, ignore_errors=False):
        command = [self.cli_path] + args
        p = Popen(command, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        out, err = p.communicate(input=command_input)
        rc = p.wait()
        if not ignore_errors and rc != expected_rc:
            raise AnsibleLookupError(to_text(err))
        return rc, out, err

    def _parse_field(self, data_json, field_name, section_title=None):
        """
        Retrieves the desired field from the `op` response payload
        When the item is a `password` type, the password is a key within the `details` key:
        $ op get item 'test item' | jq
        {
          [...]
          "templateUuid": "005",
          "details": {
            "notesPlain": "",
            "password": "foobar",
            "passwordHistory": [],
            "sections": [
              {
                "name": "linked items",
                "title": "Related Items"
              }
            ]
          },
          [...]
        }
        However, when the item is a `login` type, the password is within a fields array:
        $ op get item 'test item' | jq
        {
          [...]
          "details": {
            "fields": [
              {
                "designation": "username",
                "name": "username",
                "type": "T",
                "value": "foo"
              },
              {
                "designation": "password",
                "name": "password",
                "type": "P",
                "value": "bar"
              }
            ],
            [...]
          },
          [...]
        """
        data = json.loads(data_json)
        if section_title is None:
            # https://github.com/ansible-collections/community.general/pull/1610:
            # check the details dictionary for `field_name` and return it immediately if it exists
            # when the entry is a "password" instead of a "login" item, the password field is a key
            # in the `details` dictionary:
            if field_name in data['details']:
                return data['details'][field_name]

            # when the field is not found above, iterate through the fields list in the object details
            for field_data in data['details'].get('fields', []):
                if field_data.get('name', '').lower() == field_name.lower():
                    return field_data.get('value', '')
        for section_data in data['details'].get('sections', []):
            if section_title is not None and section_title.lower() != section_data['title'].lower():
                continue
            for field_data in section_data.get('fields', []):
                if field_data.get('t', '').lower() == field_name.lower():
                    return field_data.get('v', '')
        return ''


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        op = OnePass()

        field = kwargs.get('field', 'password')
        section = kwargs.get('section')
        op.subdomain = kwargs.get('subdomain')
        op.domain = kwargs.get('domain', '1password.com')

        op.assert_logged_in()

        vault = terms.pop(0)

        values = []
        for term in terms:
            values.append(op.get_field(term, field, section, vault))
        return values
