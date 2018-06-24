#!/usr/bin/python3
'''
//===------------------------------------------------------------------------------------------===//
//
//                        The MANIAC Dynamic Binary Instrumentation Engine
//
//===------------------------------------------------------------------------------------------===//
//
// Copyright (C) 2018 Libre.io Developers
//
// This program is free software: you can redistribute it and/or modify it under the terms of the
// GNU General Public License as published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
// even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
// General Public License for more details.
//
//===------------------------------------------------------------------------------------------===//
//
// The build module.
//
//===------------------------------------------------------------------------------------------===//
'''

import glob
import hashlib
import io
import json
import os
import zipfile

import nacl.encoding
import nacl.signing


class BuildModule():
    def __init__(self, id, author, key, control, readme, payloads):
        self.id = id
        self.author = author
        self.key = key
        self.control = control
        self.readme = readme
        self.payloads = payloads

    def run(self):
        for target, _ in self.payloads.items():
            self.target = target
            self.map_directory_structure()
            self.generate_checksum()
            self.generate_metadata()
            self.generate_signature()
            self.consolidate()

    def map_directory_structure(self):
        self.files = dict()

        # control
        self.files['control.json'] = open(self.control, mode='rb').read()

        # readme
        self.files['README.md'] = open(self.readme, mode='rb').read()

        # payloads
        for target, entries in self.payloads.items():
            if target != self.target:
                continue

            for entry in entries:
                for file in glob.iglob(entry):
                    name = 'payloads/{}'.format(os.path.basename(file))
                    self.files[name] = open(file, mode='rb').read()

    def generate_checksum(self):
        self.checksums = dict()

        for k, v in self.files.items():
            self.checksums[k] = hashlib.blake2b(v).hexdigest()

    def generate_metadata(self):
        self.metadata = dict()
        self.metadata['id'] = self.id
        self.metadata['author'] = self.author
        self.metadata['target'] = self.target
        self.metadata['checksums'] = self.checksums

        self.files['metadata.json'] = str.encode(json.dumps(self.metadata, indent=4))

    def generate_signature(self):
        signing_key_seed = bytes.fromhex(open(self.key, 'r').read().strip())
        signing_key = nacl.signing.SigningKey(signing_key_seed)
        signed = signing_key.sign(self.files['metadata.json'], nacl.encoding.HexEncoder)

        self.files['metadata.sig'] = signed.signature

        verify_key = signing_key.verify_key
        verify_key_hex = verify_key.encode(encoder=nacl.encoding.HexEncoder)

        print('Public key: {}'.format(verify_key_hex))

    def consolidate(self):
        mf = io.BytesIO()

        with zipfile.ZipFile(mf, 'w', zipfile.ZIP_DEFLATED) as zf:
            for k, v in self.files.items():
                zf.writestr(k, v)

        with open('{}.{}.zip'.format(self.id, self.target), 'wb') as f:
            f.write(mf.getvalue())
