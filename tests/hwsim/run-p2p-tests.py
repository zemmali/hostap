#!/usr/bin/python
#
# P2P tests
# Copyright (c) 2013, Jouni Malinen <j@w1.fi>
#
# This software may be distributed under the terms of the BSD license.
# See README for more details.

import os
import sys
import time

import logging

from wpasupplicant import WpaSupplicant

import test_p2p_grpform

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-d':
        logging.basicConfig(level=logging.DEBUG)
    elif len(sys.argv) > 1 and sys.argv[1] == '-q':
        logging.basicConfig(level=logging.WARNING)
    else:
        logging.basicConfig(level=logging.INFO)

    dev0 = WpaSupplicant('wlan0')
    dev1 = WpaSupplicant('wlan1')
    dev2 = WpaSupplicant('wlan2')
    dev = [ dev0, dev1, dev2 ]

    for d in dev:
        if not d.ping():
            print d.ifname + ": No response from wpa_supplicant"
            return
        d.reset()
        print "DEV: " + d.ifname + ": " + d.p2p_dev_addr()

    tests = []
    test_p2p_grpform.add_tests(tests)

    passed = []
    failed = []

    for t in tests:
        print "START " + t.__name__
        for d in dev:
            d.request("NOTE TEST-START " + t.__name__)
        try:
            t(dev)
            passed.append(t.__name__)
            print "PASS " + t.__name__
        except Exception, e:
            print e
            failed.append(t.__name__)
            print "FAIL " + t.__name__
        for d in dev:
            d.request("NOTE TEST-STOP " + t.__name__)

    print "passed tests: " + str(passed)
    print "failed tests: " + str(failed)
    if len(failed):
        sys.exit(1)

if __name__ == "__main__":
    main()