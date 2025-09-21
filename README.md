SolidFire storage backend for Cinder
------------------------------------

**NOTE:** this is a fork from https://github.com/solidfire/charm-cinder-solidfire which NetApp no longer maintains (and/or supports). It's meant to serve as an ecouragement for users interested in using SolidFire with newer VMware alternatives.

Overview
========

This charm configures Cinder to use SolidFire as a backend. This charm works
with multiple backends from other vendors in the same environment. 

To use:

    juju deploy cinder
    juju deploy cinder-solidfire_amd64.charm
    juju config cinder-solidfire san_ip=192.168.1.34 san_login=admin san_password=b____n
    juju add-relation cinder-solidfire:storage-backend cinder:storage-backend

This will setup a configuration file with the stanza named for the unit
(ex: cinder-solidfire-1) and the volume_backend_name set to 'cinder-solidfire'.
The charm does NOT setup the volume-types for Cinder. You will need to do that
once the Stack is up. See the Cinder configuration guide for details. 

Prerequisites
=============

Everything assumes you have the SolidFire cluster up and running already and
that your controller nodes (containers) can reach the SolidFire MVIP and SVIP
as needed.

**Important:** The SolidFire API uses HTTPS (port 443 by default). Ensure a 
valid TLS certificate is deployed on the SolidFire cluster, as Cinder requires 
secure communication and will reject invalid certificates.

Configuration
=============

The configuration options for this charm are shown below (by the charm store).
The required configuration minimum options are san_ip, san_login, san_password,
all others are optional. 

As an option to the above command (in overview) to set the variables, you can
also pass a file into the deploy command with the configuration like this:

    juju deploy  /home/$(whoami)/charms/noble/cinder-solidfire_amd64.charm --config=SF-Config.yaml

Development
===========

Environment used to build the bundle for AMD64 systems contained in the root of this repository:

- LXD 5.21.4
- Charm Tools 3.5.3

```sh
sudo apt install charm-tools  # or sudo snap install charmcraft --classic for the newer tool
sudo snap install lxd --classic
sudo lxd init --auto
sudo charmcraft pack
```

Test the bundle:

- Install Zaza with `pip install zaza` (or `pip3 install zaza`). Create and activatte a venv if necessary.
- Have Juju Ready: Bootstrap a controller and create a model (e.g., `juju add-model test`).
- Run the Bundle: `zaza run tests/bundles/noble.yaml`
- This deploys the bundle (Cinder + SolidFire charm), sets up relations, and runs any defined tests. 
Since there's only the bundle so far (no test files), it will only deploy and check that units are active.

Where to get help
===================

Please use Github Issues.

