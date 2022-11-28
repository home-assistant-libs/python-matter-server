# Python Matter Server

This project implements a Matter Controller Server using WebSockets and provides both a server and client implementation.
The goal of this project is primary to Matter support for Home Assistant but the unioversal approach makes it suitable to be used in other projects too.

This repository is for development only. For enabling Matter support within Home Assistant, please refer to the Home Assistant documentation.

:warning: This project is under development and considered BETA !

## Trying it out

These instructions are for development only.

To install the client and server: `pip install python-matter-server[server]`
To only install the client part: `pip install python-matter-server`

NOTE that the server depends on the CHIP SDK for which we've built Python wheels for Linux only, to use it on other platforms, you'll have to build the CHIP core wheel and install it. See: https://github.com/home-assistant-libs/chip-wheels/blob/main/.github/workflows/build.yaml

## Development

WIP
