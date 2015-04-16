[![Stories in Ready](https://badge.waffle.io/alekseiko/tow.png?label=ready&title=Ready)](https://waffle.io/alekseiko/tow)
[![Build Status](https://travis-ci.org/alekseiko/tow.svg)](https://travis-ci.org/alekseiko/tow)
[![Coverage Status](https://coveralls.io/repos/alekseiko/tow/badge.svg)](https://coveralls.io/r/alekseiko/tow)
[![Code Climate](https://codeclimate.com/github/alekseiko/tow/badges/gpa.svg)](https://codeclimate.com/github/alekseiko/tow)                
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/alekseiko/tow?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

Tow - configuration management tool for Docker
==============================================

## Overview

Tow provides a workflow for building docker images with dynamics configuration files using templates. The main concept is processing all configuration templates outside of container and then build image using pre-processed files.

Here how it works:

![Tow process diagram](docs/images/tow-process.png)

## Installation

Latest stable release is always available on PyPi.

```
pip install tow
```

## Getting Started

Check out [Getting Started Guide](docs/introduction.md) to get more familiar with Tow.

If you are looking real world example of Tow project checkout: [tow-nginx](https://github.com/yurinnick/tow-nginx) - an example Tow project set up Nginx in most simple configuration.

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






