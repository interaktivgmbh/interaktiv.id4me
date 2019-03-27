Interaktiv.id4me
================
interaktiv.id4me is a Plugin for Plone 5.x to allow users to login and connect their accounts to any ID4Me Provider.
When set in Plone global settings, users can also register through their Provider.

Installation
------------

Add to your buildout.cfg: ::

  eggs +=
      interaktiv.id4me

Then start your buildout and restart your instance

go to `/prefs_install_products_form` and install "ID4Me"

Configuration
-------------
go to Plone Site Setup and select under "Add-on Configuration" the "ID4Me Settings" entry.
Select an Client name and save.

Usage
-----
link your users to the view `/@@id4me` from any navigation root

Optional
--------
If you are using a Zeo-Cluster, you need to configure BeakerSessionManager_


.. _BeakerSessionManager: https://pypi.org/project/Products.BeakerSessionDataManager/