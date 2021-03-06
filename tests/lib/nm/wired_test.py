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

import pytest

from lib.compat import mock

from libnmstate import nm


@pytest.fixture
def NM_mock():
    with mock.patch.object(nm.wired.nmclient, 'NM') as m:
        yield m


def test_create_setting_None(NM_mock):
    setting = nm.wired.create_setting({}, None)
    assert setting is None


def test_create_setting_duplicate(NM_mock):
    base_profile = mock.MagicMock()

    setting = nm.wired.create_setting({'ethernet': {'speed': 1000}},
                                      base_profile)
    assert setting == \
        base_profile.get_setting_wired.return_value.duplicate.return_value


def test_create_setting_mtu(NM_mock):
    setting = nm.wired.create_setting({'mtu': 1500}, None)
    assert setting == NM_mock.SettingWired.new.return_value
    assert setting.props.mtu == 1500


@mock.patch.object(nm.wired, 'minimal_ethtool',
                   return_value={'speed': 1337, 'duplex': 'mocked',
                                 'auto-negotiation': 'mocked'})
def test_create_setting_auto_negotiation_False(ethtool_mock, NM_mock):
    setting = nm.wired.create_setting(
        {'name': 'nmstate_test', 'ethernet': {'auto-negotiation': False}},
        None)
    assert setting == NM_mock.SettingWired.new.return_value
    assert setting.props.auto_negotiate is False
    assert setting.props.speed == 1337
    assert setting.props.duplex == 'mocked'
    assert ethtool_mock.called_with('nmstate_test')


def test_create_setting_only_auto_negotiation_True(NM_mock):
    setting = nm.wired.create_setting({'ethernet':
                                      {'auto-negotiation': True}}, None)
    assert setting == NM_mock.SettingWired.new.return_value
    assert setting.props.auto_negotiate is True
    assert setting.props.speed == 0
    assert setting.props.duplex is None


def test_create_setting_auto_negotiation_speed_duplex(NM_mock):
    setting = nm.wired.create_setting({'ethernet': {'auto-negotiation': True,
                                                    'speed': 1000, 'duplex':
                                                    'full'}}, None)
    assert setting == NM_mock.SettingWired.new.return_value
    assert setting.props.auto_negotiate is True
    assert setting.props.speed == 1000
    assert setting.props.duplex == 'full'


def test_create_setting_speed_duplex(NM_mock):
    setting = nm.wired.create_setting({'ethernet': {'speed': 1000,
                                                    'duplex': 'full'}},
                                      None)
    assert setting == NM_mock.SettingWired.new.return_value
    assert setting.props.speed == 1000
    assert setting.props.duplex == 'full'
