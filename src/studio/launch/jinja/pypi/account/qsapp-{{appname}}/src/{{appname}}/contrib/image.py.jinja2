# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import qiniu
import base64
import struct
import hashlib
from PIL import Image

from .. import app

qn = qiniu.Auth(app.config["QINIU_ACCESS_KEY"], app.config["QINIU_SECRET_KEY"])


def calc_hashkey(data):
    h = hashlib.sha256(data.read()).digest()
    data.seek(0)
    im = Image.open(data)
    width, height = im.size
    format_ = im.format
    h = struct.pack(b'<32sII2s', h, width, height, format_[:2])
    # h is 42 bytes, 4[n/3] = 56, this will avoid padding
    _hashkey = base64.urlsafe_b64encode(h)

    return _hashkey


def parse_hashkey(hashkey):
    h = base64.urlsafe_b64decode(str(hashkey))
    return struct.unpack(b'<32sII2s', h)


def thumbnail(hashkey, shcema='http', mode=2, width=None, height=None):
    domain = random.choice(app.config['QINIU_DOMAINS'])
    url = '%s://%s/%s?imageView2/%s' % (shcema, domain, hashkey, mode)
    if width:
        url += '/w/%s' % width
    if height:
        url += '/h/%s' % height
    return url
