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
// Set of command line utilities for developing MANIAC packages.
//
//===------------------------------------------------------------------------------------------===//
'''

import argparse
import yaml
import sys

from modules import build


def main():
    main_parser = argparse.ArgumentParser()
    main_parser.add_argument('module', choices=['build'], type=str)
    args = main_parser.parse_args(sys.argv[1:2])

    if args.module == 'build':
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', type=str, required=True)
        args = parser.parse_args(sys.argv[2:])

        with open(args.config) as f:
            c = yaml.load(f)

        build_module = build.BuildModule(  #
            c['id'], c['author'], c['key'], c['control'], c['readme'], c['payloads'])
        build_module.run()

    else:
        raise NotImplementedError


if __name__ == '__main__':
    main()
