# Python API for interacting with FLOCX

Overview
--------

This is a client for the OpenStack `Market API
It provides:

* a command-line interface: ``openstack market``

``python-flocxclient`` is licensed under the Apache License, Version 2.0,
like the rest of OpenStack.


``openstack market`` CLI
---------------------------

The ``openstack market`` command line interface is available when the marketplace
 plugin (included in this package) is used with the `OpenStackClient
https://docs.openstack.org/python-openstackclient/latest/

The client uses keystone to look for the `market` service and currently does not
allow for endpoint overriding.

To install this package, run `python3 setup.py install` on the command line

# Examples:

    openstack market offer list
will print to screen a list of all the offers in the flocx database

# This repository is currently a work in progress
