#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## What model are we working with?

import os

def determine_model():
    """Determine the System76 model number"""
    
    # Determine system unique value    
    b = os.popen('sudo dmidecode -s system-uuid')
    try:
        uuid = b.readline().strip()
    finally:
        b.close()
    system_uuid = uuid
    
    c = os.popen('sudo dmidecode -s baseboard-product-name')
    try:
        baseboard_product = c.readline().strip()
    finally:
        c.close()
    baseboard_product_name = baseboard_product
    
    d = os.popen('sudo dmidecode -s system-product-name')
    try:
        system_product = d.readline().strip()
    finally:
        d.close()
    system_product_name = system_product
    
    e = os.popen('sudo dmidecode -s system-version')
    try:
        system_version = e.readline().strip()
    finally:
        e.close()
    system_product_version = system_version
    
    # Determine ultimate System76 model
    # Return values to the program

    # Unique ID (UUID)
    if system_uuid == '00000000-0000-0000-0000-000000000001':
        modelname = "koap1"
        return modelname
    # Baseboard Product Name
    elif baseboard_product_name == 'Z35FM':
        modelname = "daru1"
        return modelname
    elif baseboard_product_name == 'Z35F':
        modelname = "daru1"
        return modelname
    elif baseboard_product_name == 'MS-1221':
        modelname = "daru2"
        return modelname
    elif baseboard_product_name == 'IFL91':
        modelname = "panv3"
        return modelname
    elif baseboard_product_name == 'IFT01':
        modelname = "gazv5"
        return modelname
    elif baseboard_product_name == 'IFT00':
        modelname = "gazp5"
        return modelname
    elif baseboard_product_name == 'A8N8L':
        modelname = "sabv1"
        return modelname
    elif baseboard_product_name == 'M2N8L':
        modelname = "sabv2"
        return modelname
    elif baseboard_product_name == 'P5K-VM':
        modelname = "sabv3"
        return modelname
    elif baseboard_product_name == 'IFL90':
        modelname = "serp3"
        return modelname
    elif baseboard_product_name == 'JFL92':
        modelname = "serp4"
        return modelname
    elif baseboard_product_name == 'MS-7250':
        modelname = "wilp1"
        return modelname
    elif baseboard_product_name == 'A8V-MQ':
        modelname = "ratv1"
        return modelname
    elif baseboard_product_name == 'P5VD2-MX':
        modelname = "ratv2"
        return modelname
    elif baseboard_product_name == 'P5VD2-VM':
        modelname = "ratv3"
        return modelname
    elif baseboard_product_name == 'D945GCPE':
        modelname = "ratv4"
        return modelname
    elif baseboard_product_name == 'P5GC-MX/1333':
        modelname = "ratv5"
        return modelname
    elif baseboard_product_name == 'MPAD-MSAE Customer Reference Boards':
        modelname = "gazv2"
        return modelname
    elif baseboard_product_name == 'K8N-DL':
        modelname = "wilp2"
        return modelname
    elif baseboard_product_name == 'KFN5-D SLI':
        modelname = "wilp3"
        return modelname
    elif baseboard_product_name == 'DP35DP':
        modelname = "wilp5"
        return modelname
    # System Product Name
    elif system_product_name == 'MS-1012':
        modelname = "gazv1"
        return modelname
    elif system_product_name == 'Z62FP':
        modelname = "gazv3"
        return modelname
    elif system_product_name == 'Z62FM':
        modelname = "gazv4"
        return modelname
    elif system_product_name == 'Z62F':
        modelname = "gazp1"
        return modelname
    elif system_product_name == 'Z62J':
        modelname = "gazp2"
        return modelname
    elif system_product_name == 'Z62JM':
        modelname = "gazp3"
        return modelname
    elif system_product_name == 'Z62JP':
        modelname = "gazp3"
        return modelname
    elif system_product_name == 'U-100':
        modelname = "meec1"
        return modelname
    elif system_product_name == 'Z96F':
        modelname = "panv2"
        return modelname
    elif system_product_name == 'Centoris V661':
        modelname = "panv2"
        return modelname
    elif system_product_name == 'Z96FM':
        modelname = "panv2"
        return modelname
    elif system_product_name == 'HEL80I':
        modelname = "serp1"
        return modelname
    elif system_product_name == 'HEL8X':
        modelname = "serp1"
        return modelname
    elif system_product_name == 'HEL80C':
        modelname = "serp2"
        return modelname
    elif system_product_name == 'A7V':
        modelname = "bonp1"
        return modelname
    # System Product Version
    elif system_product_name == 'M570TU':
        modelname = "bonp2"
        return modelname
    elif system_product_version == 'bonp2':
        modelname = "bonp2"
        return modelname
    elif system_product_version == 'bonp3':
        modelname = "bonp3"
        return modelname
    elif system_product_version == 'gazu1':
        modelname = "gazu1"
        return modelname
    elif system_product_name == 'M720T/M730T':
        modelname = "daru3"
        return modelname
    elif system_product_version == 'daru3':
        modelname = "daru3"
        return modelname
    elif system_product_name == 'M740T/M760T':
        modelname = "panp4i"
        return modelname
    elif system_product_name == 'M740TU/M760TU':
        modelname = "panp4n"
        return modelname
    elif system_product_version == 'panp4n':
        modelname = "panp4n"
        return modelname
    elif system_product_version == 'panp5':
        modelname = "panp5"
        return modelname
    elif system_product_version == 'ment1':
        modelname = "ment1"
        return modelname
    elif system_product_version == 'ratv6':
        modelname = "ratv6"
        return modelname
    elif system_product_version == 'wilp6':
        modelname = "wilp6"
        return modelname
    elif system_product_name == 'M860TU':
        modelname = "serp5"
        return modelname
    elif system_product_version == 'serp5':
        modelname = "serp5"
        return modelname
    else:
        modelname = "nonsystem76"
        return modelname
