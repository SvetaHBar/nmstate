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


import pytest

from libnmstate import netapplier


@pytest.fixture
def eth_state():
    return {
        'interfaces': [
            {
                'name': 'eth1',
                'state': 'up',
                'type': 'ethernet',
                'mtu': 9000,
                'ipv4': {
                    'enabled': False
                },
                'ipv6': {
                    'enabled': False
                }
            }
        ]
    }


def test_edit_nic_mtu(eth_state):
    eth_state['interfaces'][0]['eth1']['mtu'] = 1500
    netapplier.apply(eth_state)


@pytest.fixture
def eth_state1():
    return {
        'interfaces': [
            {
                'name': 'eth1',
                'state': 'up',
                'type': 'ethernet',
                'mtu': 9000,
                'ipv4': {
                    'enabled': False
                }
            },

                {
                    'name': 'eth2',
                    'state': 'up',
                    'type': 'ethernet',
                    'mtu': 1500,
                    'ipv4': {
                        'enabled': False
                    }
                },

                    {
                        'name': 'bond99',
                        'state': 'up',
                        'type': 'bond',
                        'ipv4': {
                            'enabled': True,
                            'address':{
                                'ip':'10.10.10.10',
                                'prefix-length':'24'
                            },
                        'link-aggregation':{
                            'mode':'balance-rr',
                            'options':{
                                'miimon':'140'
                            }
                        },
                        'slaves':{
                            ['eth1','eth2']
                        }
                        }
                    }

        ]
    }


def test_edit_nic_mtu(eth_state1):
    eth_state['interfaces'][2]['bond99']['state'] = 'absent'
    netapplier.apply(eth_state1)