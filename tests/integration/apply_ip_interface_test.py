#
# Copyright 2018 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import copy

from libnmstate import netapplier

from .testlib import assertlib
from .testlib import statelib


def test_add_static_ipv4():
    desired_state = statelib.show_only(('eth1',))
    eth1_desired_state = desired_state['interfaces'][0]

    eth1_desired_state['state'] = 'up'
    eth1_desired_state['ipv4']['enabled'] = True
    eth1_desired_state['ipv4']['address'] = [
        {'ip': '192.168.122.250', 'prefix-length': 24}
    ]
    netapplier.apply(copy.deepcopy(desired_state))

    assertlib.assert_state(desired_state)
