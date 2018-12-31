# maniacli

## Installation
> NOTE: python 3.7+ is required!
```
$ sudo -H pip3 install setuptools pynacl pyinstaller pyyaml
$ make && sudo make install
```

## Usage

### Build

```
$ maniacli build --config ./build.yaml
```

#### build.yaml
```
--- 
# Unique ID of the mod package
id: io.libre.jdoe.samplemod

# Name of the author
author: "Jane Doe"

# Path to the hex-encoded signing key
key: private.key

# Path to the main control file
control: control.json

# Path to the README file
readme: README.md

# Path to payloads
payloads:
  arm64-v8a:
    - libs/arm64-v8a/*.so

  armeabi-v7a:
    - libs/armeabi-v7a/*.so

```

#### control.json
```
[
	{"action": "elf-inject", "parameters": ["libxhook.so"]},
	{"action": "elf-inject", "parameters": ["libclient.so"]}
]
```

#### private.key
```
$ openssl rand -hex 32 > private.key
```
