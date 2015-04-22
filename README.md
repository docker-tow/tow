Tow - configuration management tool for Docker
==============================================

[![Build Status](https://travis-ci.org/docker-tow/tow.svg)](https://travis-ci.org/docker-tow/tow)
[![Coverage Status](https://coveralls.io/repos/docker-tow/tow/badge.svg)](https://coveralls.io/r/docker-tow/tow)
[![Dependency Status](https://gemnasium.com/docker-tow/tow.svg)](https://gemnasium.com/docker-tow/tow)
[![Code Climate](https://codeclimate.com/github/docker-tow/tow/badges/gpa.svg)](https://codeclimate.com/github/docker-tow/tow)    

[![Stories in Ready](https://badge.waffle.io/docker-tow/tow.png?label=ready&title=Ready)](https://waffle.io/docker-tow/tow)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/docker-tow/tow?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)


## Overview

Tow provides a workflow for building docker images with dynamics configuration files using templates. The main concept is processing all configuration templates outside of container and then build image using pre-processed files.

Here how it works:

![Tow process diagram](docs/images/tow-process.png)

## Installation

Latest stable release is always available on PyPi.

[![PyPI version](https://badge.fury.io/py/tow.svg)](http://badge.fury.io/py/tow)
[![PyPi downloads](https://pypip.in/d/tow/badge.png)](https://crate.io/packages/tow/)

```
pip install tow
```

## Getting Started

Check out [Getting Started Guide](docs/introduction.md) to get more familiar with Tow.

If you are looking real world example of Tow project checkout: [tow-nginx](https://github.com/docker-tow/tow-nginx) - an example Tow project set up Nginx in most simple configuration.

## Usage

```
tow [command] <options>

Commands:
    create <projectname> - create new tow project in current directory
    build - process configs and build images
        [--run-tow] - executes tow.sh on start
    run [-e <parameter>][args] <image> - process configuration files overrides and start container
```

Tow also available in docker image. Checkout [Tow docker image documentation](https://github.com/yurinnick/tow-docker) for more information.

## License

Tow is licensed under the Apache License, Version 2.0. See LICENSE for full license text

```
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
```
