Internet Download Manager
---------------------------

Python Internet Download Manager Library


Installing
----------

Install and update using `pip3`_:

.. code-block:: text

    $ pip3 install internetdownloadmanager

Python 3 and newer.

.. _pip3: https://pip.pypa.io/en/stable/quickstart/


Example
----------------



.. code-block:: python

    from internetdownloadmanager import Downloader

    downloader = Downloader(worker=25,
                            part_size=1000000,
                            resumable=True)

    downloader.download(url="http://example.com/file",
                        path= 'not_required.extension')

Output:
-------

.. code-block:: python

    INFO:internetdownloadmanager.utils:
    File Path:filename.extension
    File Size: 377277402
    Worker: 25
    Calculated Part: 378

    WARNING:internetdownloadmanager.utils:Download Starting
    Status: %3.17 | Transfer Rate =  27274 Kb/s | Time Left: 108 sn | Time: 8 sn | AVG Speed=15169 Kb/s



* worker: Set how many threads work (default=25)
* part_size: Set piece size downloaded byte (default=1000000)
* resumable: Setting the download to be resumable (default=False)

If something goes wrong and the process is interrupted

.. code-block:: python

    downloader.resume('example.file_extention.resumable')

Support
-------

*   Python 3.x
*   Supports all operating systems

Links
-----

*   License: `Apache License <https://github.com/dinceraslancom/internetdownloadmanager/LICENSE.rst>`_
*   Code: https://github.com/dinceraslancom/internetdownloadmanager
