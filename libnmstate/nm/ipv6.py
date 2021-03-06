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

import socket

from libnmstate.nm import nmclient


def get_info(active_connection):
    info = {'enabled': False}
    if active_connection is None:
        return info

    ipconfig = active_connection.get_ip6_config()
    if ipconfig is None:
        return info

    addresses = [
        {
            'ip': address.get_address(),
            'prefix-length': int(address.get_prefix())
        }
        for address in ipconfig.get_addresses()
    ]
    if not addresses:
        return info

    info['enabled'] = True
    info['address'] = addresses
    return info


def create_setting(config):
    setting_ip = nmclient.NM.SettingIP6Config.new()
    if config and config.get('enabled') and config.get('address'):
        setting_ip.props.method = (
            nmclient.NM.SETTING_IP6_CONFIG_METHOD_MANUAL)
        for address in config['address']:
            naddr = nmclient.NM.IPAddress.new(socket.AF_INET6,
                                              address['ip'],
                                              address['prefix-length'])
            setting_ip.add_address(naddr)
    else:
        setting_ip.props.method = (
            nmclient.NM.SETTING_IP6_CONFIG_METHOD_IGNORE)
    return setting_ip
