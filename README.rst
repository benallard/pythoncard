============
 PythonCard
============

---------------------------------
 (a.k.a ``JavaCard`` under PyPi)
---------------------------------

This is a pure python version of the javacard operating system as
found on javacard smartcards.

It does not provides much on his own beside the functionnalities of the
Operating System, as such, it is often used in combination with others
projects like CAPRunner_ (linked via .CAP files) or WebSCard_ (through
CAPRunner or python versions of Applets).

Documentation on this project is better found as original JavaCard
documentation (ask Google). The goal is to replication the exact same
functionnalities. If your experience is other, please fill in a `bug
report`_. Please do the same for missing functionnalities. As for now,
I only implemented the functionnalities I was needing during my
various tests.

To **use it**, when writing your Applet, just replace the following
Java construction::

    import javacard.framework.Applet;

with::

    from pythoncard.framework import Applet

As, so far I know, the javacard version are backward compatible, the
goal is to provide a classic 3.0.1 version, while maintaining
compatiblity with earlier version like 2.1.2.

PythonCard is dependant on pyDes_ and pyCrypto_ for cryptographic
operations. The rest of the functionnalities will however work without
those packages installed.

To **install it**, either put the necessary directories in your
``PYTHONPATH``, or install it via PyPi_::

    $ pip install JavaCard 

To **run the test** try that:

    $ python -m unittest discover test

.. _CAPRunner: https://github.com/benallard/caprunner
.. _WebSCard: https://github.com/benallard/webscard
.. _`bug report`: https://github.com/benallard/caprunner/issues/new
.. _pyDes: http://twhiteman.netfirms.com/des.html
.. _pyCrypto: https://www.dlitz.net/software/pycrypto/
.. _PyPi: http://pypi.python.org/pypi/JavaCard
