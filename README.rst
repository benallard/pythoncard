============
 PythonCard
============

---------------------------------
 (a.k.a ``JavaCard`` under PyPi)
---------------------------------

This is a pure python version of the javacard operating system as found on
javacard smartcards.

It does not provides much on his own beside the functionnalities of the
Operating System, as such, it is often used in combinason with others projects
like CAPRunner_ (linked with CAP files) or WebSCard_ (through CAPRunner or
python versions of Applets)

Documentation on this project is better found as original JavaCard
documentation (ask Google). The goal is to replication the exact same
functionnalities. If your experience is other, please fill in a `bug report`_.
Same for missing functionnalities.

To **use it**, when writing your Applet, just replace the following Java
construction::

    import javacard.framework.Applet;

with::

    from pythoncard.framework import Applet

As, so far I know, the javacard version are backward compatible, the goal is to
provide a classic 3.0.1 version, while maintaining compatiblity with earlier
version like 2.1.2.

PythonCard is dependant on pyDes_ and pyCrypto_ for crptographic operations. The
rest of the functionnalities will however work without those packages installed.

.. _CAPRunner: https://bitbucket.org/benallard/caprunner
.. _WebSCard: https://bitbucket.org/benallard/webscard
.. _`bug report`: https://bitbucket.org/benallard/pythoncard/issues
.. _pyDes: http://twhiteman.netfirms.com/des.html
.. _pyCrypto: https://www.dlitz.net/software/pycrypto/
