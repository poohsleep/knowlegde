#!/usr/bin/env python
# coding=utf-8

import argparse
import urllib2
# from xml.etree.ElementTree import *
import xml.etree.ElementTree as ET
import json

BASE_URL = "http://api.donkey.db.rakuten.co.jp/api/"


def get_args():
    parser = argparse.ArgumentParser(
        description='get mount info')
    parser.add_argument('-nfs', metavar='nfs', type=str, default="nbackup20",
                        help='NFS-Name')
    parser.add_argument('-accesskey', metavar='accesskey', type=str, default="1b167f9057bae0a1a5577d8fbeb4f78b",
                        help='Donkey-Access-Key')
    args = parser.parse_args()
    return args


def create_json_mesg(key, value):
    lst = []
    key_list = key
    value_list = value
    lst = zip(key_list, value_list)
    orddic = OrderedDict(lst)
    return json.dumps(orddic)

# get the list of host


def get_host_list(host, accesskey):
    return urllib2.urlopen("{0}getHostList/hostName/{1}/accessKey/{2}".format(BASE_URL, nfs, accesskey)).read()

# get detailed information of the host.


def get_host_info(host, accesskey):
    return urllib2.urlopen("{0}getHost/v2/accessKey/{2}/en/hostName/{1}".format(BASE_URL, host, accesskey)).read()

# get list of the NFS host


def get_nfs_list(nfs, accesskey):
    return urllib2.urlopen("{0}getNfsList/nfshostName/{1}/accessKey/{2}".format(BASE_URL, nfs, accesskey)).read()

# get the hosts are mounting in the NFS host


def get_host_list(nfsName, accesskey):
    return urllib2.urlopen("{0}getNfs/v2/accessKey/{2}/nfsName/{1}".format(BASE_URL, nfsName, accesskey)).read()


def main():
    args = get_args()
    context = []
    # get nfs host
    nfs_host_lst = []
    nfs_host = get_nfs_list(args.nfs, args.accesskey)
    root = ET.fromstring(nfs_host)
    for i in root.findall('nfshost_list/nfshost/name'):
        nfs_host_lst.append(i.text)
    ['nbackup201', 'nbackup201.bk.jp.local', 'nbackup202', 'nbackup202.bk.jp.local',
        'nbackup203', 'nbackup203.bk.jp.local', 'nbackup204', 'nbackup204.bk.jp.local']

    nfs_host_lst = ['nbackup201']

    # get hosts list which are mounting in the NFS host
    for nfs_host in nfs_host_lst:
        host_lst = []

        host = get_host_list(nfs_host, args.accesskey)
        root = ET.fromstring(host)
        for i in root.findall('nfs_host_list/nfs_host/host_list/host'):
            host_lst.append(i.text)
            for host in host_lst:

        nfsHost_hosts_dict = {'nfs': nfs_host, 'hosts': host_lst}
        print nfsHost_hosts_dict


if __name__ == "__main__":
    main()
