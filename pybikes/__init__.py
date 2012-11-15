# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012, eskerda <eskerda@gmail.com>
# Distributed under the AGPL license, see LICENSE.txt

"""PyBikes
PyBikes is a parsing library to extract bike sharing information from multiple
sources. It contains multiple classes to handle this sort of information,
and is not a class itself. The idea is to be able to call it like:

from pybikes import BicingShareSystem, BicingStation

bicing = new BicingShareSystem() <- Returns BicingShareSystem
print "%s: %s" % ("Bicing City is", bicing.meta.city)
stations = bicing.get_stations() <- Returns Array[BicingStation]

"""

import json

from pkg_resources import resource_string

from .base import *
from .bixi import *
from .bcycle import *
from .smartbike import *

__all__ = base.__all__ +\
          bixi.__all__ +\
          bcycle.__all__ +\
          smartbike.__all__

class BikeShareSystemNotFound(Exception):
    pass

def getDataFile(system):
    try:
        return json.loads(
            resource_string(__name__, "data/%s.json" % system).decode('utf-8')
        )
    except FileNotFoundError:
        raise FileNotFoundError('File data/%s.json not found' % system)

def getBikeShareSystem(system, tag):
    data = getDataFile(system)
    meta_data = [sys for sys in data['instances'] if sys['tag'] == tag]
    
    if len(meta_data) == 0:
        raise BikeShareSystemNotFound(
            'System %s not found in data/%s.json' % (tag, system))
    
    return eval(data.get('class'))(** list(meta_data)[0])
