rpExtractSink's Documentation
=============================

Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Introduction
############

.. _rpBase: https://github.com/Galaxy-SynBioCAD/rpBase
.. _rpCache: https://github.com/Galaxy-SynBioCAD/rpCache
.. _RetroPath2.0: https://github.com/Galaxy-SynBioCAD/RetroPath2


Welcome to the documentation for rpExtractSink. This project generates an sink file that is RetroPath2.0_ friendly.

Usage
#####

First build the rpBase_ and rpCache_ dockers before building the local docker:

.. code-block:: bash

   docker build -t brsynth/rpextractsink-standalone:v2 .

To call the docker locally you can use the following command:

.. code-block:: bash

   python run.py -input /path/to/file -output /path/to/file

API
###

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. currentmodule:: rpToolServe

.. autoclass:: main
    :show-inheritance:
    :members:
    :inherited-members:

.. currentmodule:: rpTool

.. autoclass:: rpExtractSink
    :show-inheritance:
    :members:
    :inherited-members:

.. currentmodule:: run

.. autoclass:: main
    :show-inheritance:
    :members:
    :inherited-members:
