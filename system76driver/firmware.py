# system76-driver: Universal driver for System76 computers
# Copyright (C) 2005-2017 System76, Inc.
#
# This file is part of `system76-driver`.
#
# `system76-driver` is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# `system76-driver` is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with `system76-driver`; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
Firmware updater for System76 computers.
"""

from .ecflash import Ec
import nacl.encoding
import nacl.signing
import nacl.hash
from urllib import parse, request
import tarfile
import io
import tempfile
import time
from os import path
import os
import shutil
import subprocess
from .mockable import SubProcess
from gi.repository import GLib

import logging

log = logging.getLogger(__name__)

FIRMWARE_URI = 'http://iso.system76.com/firmware/current/'

FIRMWARE_SET_NEXT_BOOT = """#!/bin/bash -e

if [ "$EUID" != "0" ]
then
    echo "You are not running as root" >&2
    exit 1
fi

DISK="$(findmnt -n /boot/efi -o 'MAJ:MIN' | cut -d ':' -f 1)"
PART="$(findmnt -n /boot/efi -o 'MAJ:MIN' | cut -d ':' -f 2)"
DEV="/dev/$(lsblk -n -o 'KNAME,MAJ:MIN' | grep "${DISK}:0" | cut -d ' ' -f 1)"

echo -e "\e[1mCreating Boot1776\e[0m" >&2
efibootmgr -B -b 1776 || true
efibootmgr -C -b 1776 -d "${DEV}" -p "${PART}" -l '\\system76-fu\\boot.efi' -L "System76 Firmware Update"

echo -e "\e[1mSetting BootNext\e[0m" >&2
efibootmgr -n 1776

echo -e "\e[1mInstalled system76-fu\e[0m" >&2
"""

def get_url(filename):
    if not filename:
        f = open("/sys/class/dmi/id/product_version")
        model = f.read().strip()
        f.close()

        ec = Ec()
        project = ec.project()
        ec.close()

        project_hash = nacl.hash.sha256(bytes(project, 'utf8'), encoder=nacl.encoding.HexEncoder).decode('utf-8')

        filename = "{}_{}".format(model, project_hash)

    return 'http://iso.system76.com/firmware/current/{}'.format(filename)

def get_signed_tarball(filename=None):
    request.urlcleanup()
    signed_firmware = request.urlopen(get_url(filename)).read()
    key_file = open('verify', 'rb')
    verify_key = nacl.signing.VerifyKey(key_file.read(), encoder=nacl.encoding.HexEncoder)
    try:
        firmware = verify_key.verify(signed_firmware)
        log.info("Verified firmware signature, extracting...")
        tar = tarfile.open(fileobj=io.BytesIO(firmware))
        return tar
    except nacl.exceptions.BadSignatureError:
        log.exception("Bad firmware signature! Aborting...")
        raise nacl.exceptions.BadSignatureError
        return

def extract_tarball(tar, directory):
    os.chmod(directory, 0o700)
    tar.extractall(directory)
    os.chmod(directory, 0o500)

def set_next_boot():
    handle, name = tempfile.mkstemp()
    f = open(handle, 'w')
    f.write(FIRMWARE_SET_NEXT_BOOT)
    f.close()
    os.chmod(name, 0o500)
    try:
        output = SubProcess.check_output(['sudo', name])
    except:
        return

def _run_firmware_updater(model):
    #Download the latest updater and firmware for this machine and verify source.
    updater = get_signed_tarball('system76-fu')
    firmware = get_signed_tarball()

    if updater and firmware:
        #Extract to temporary directory and set safe permissions.
        with tempfile.TemporaryDirectory() as tempdirname:
            extract_tarball(updater, tempdirname)
            os.mkdir(path.join(tempdirname, 'firmware'))
            extract_tarball(firmware, path.join(tempdirname, 'firmware'))

            #Confirm installation with the user.

            user_name = subprocess.check_output(
                    "who | awk -v vt=tty$(fgconsole) '$0 ~ vt {print $1}'",
                    shell=True
            ).decode('utf-8').rstrip('\n')

            display_name = subprocess.check_output(
                    "who | awk -v vt=tty$(fgconsole) '$0 ~ vt {print $5}'",
                    shell=True
            ).decode('utf-8').rstrip('\n').lstrip('(').rstrip(')')

            if len(user_name) == 0 or len(display_name) == 0:
                return

            args = [
                "sudo",
                "-u", user_name,
                "DISPLAY=" + display_name,
                "--",
                "./system76-firmware-dialog"
            ]

            if subprocess.call(args) == 0:
                log.info("Setting up firmware installation.")

                #Remove old firmware updater
                try:
                    shutil.rmtree('/boot/efi/system76-fu')
                except:
                    pass

                #Install firmware to /efi/boot and set boot.efi on next boot.
                shutil.copytree(tempdirname, '/boot/efi/system76-fu')
                set_next_boot()
            else:
                return
    log.info("Installed firmware updater to boot partition. Firmware update will run on next boot.")

def run_firmware_updater(model):
    try:
        return _run_firmware_updater(model)
    except Exception:
        log.exception('Error calling _run_firmware_updater(%r):', model)