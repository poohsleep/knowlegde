#! /usr/bin/env python
#  -*- coding: utf-8 -*-

import sys
import urllib2
import json
import pprint
from xml.etree.ElementTree import *

pp = pprint.PrettyPrinter(indent=4)


class Donkey(object):

    def __init__(self, access_key):
        self.config = {
            'BASE': 'http://api.donkey.db.rakuten.co.jp/api',
            'KEY': access_key,
        }
        self.cache_servers = {}

    def get_mount_info(self, server, nfs):
        return [{'mount_point': j.find('mount_point').text,
                 'nfs_path':    j.find('name').text,
                 'option':      j.find('mount_option').text}
                for i in self.get_server_detail(server).findall('host_list/host/nfs_host_list/nfs_host')
                if i.find('name').text == nfs
                for j in i.findall('mount_device_list/mount_device')]

    def get_server_info(self, server):
        host = self.get_server_detail(server).find('host_list/host')
        return {'app_team':     host.findtext('app_team'),
                'sys_team':     host.findtext('sys_team')}
        # return { 'os_name':    host.findtext('os/name'),
        #          'os_version': host.findtext('os/version'),
        #          'place':      host.findtext('dc') }

    # TODO; bulk request
    def get_server_detail(self, server):
        if server not in self.cache_servers:
            self.cache_servers[server] = fromstring(urllib2.urlopen(
                ('%(BASE)s/getHost/v2/accessKey/%(KEY)s/lang/en/hostName/' %
                 self.config) + server
            ).read())
        else:
            pass
        return self.cache_servers[server]

    def get_server_list(self, nfs):
        return [i.text for i in fromstring(urllib2.urlopen(
            ('%(BASE)s/getNfs/v2/accessKey/%(KEY)s/fqdn/on/nfsName/' %
             self.config) + nfs
        ).read()).findall('nfs_host_list/nfs_host/host_list/host')]

    def get_nfs_list(self, search):
        return [i.text for i in fromstring(urllib2.urlopen(
            ('%(BASE)s/getNfsList/accessKey/%(KEY)s/nfshostName/' %
             self.config) + search
        ).read()).findall('nfshost_list/nfshost/name')]


def main(donkey, nfs):
    result = {}
    for nfs in donkey.get_nfs_list(nfs):
        result[nfs] = {}
        for server in donkey.get_server_list(nfs):
            result[nfs][server] = {
                "mount":  donkey.get_mount_info(server, nfs),
                "detail": donkey.get_server_info(server)
            }
    print result[nfs], result[nfs][server]
    # return json.dumps(result)
    # return json.dumps({ nfs: { server: { "mount":donkey.get_mount_info(server, nfs), "detail": donkey.get_server_info(server) }
    #                 for server in donkey.get_server_list(nfs) }
    #          for nfs in donkey.get_nfs_list(nfs) })

if __name__ == '__main__':
    if len(sys.argv) == 3:
        print main(Donkey(sys.argv[2]), sys.argv[1])
    else:
        print 'Usage: %s "NFS-Name" "Donkey-Access-Key"' % sys.argv[0]
