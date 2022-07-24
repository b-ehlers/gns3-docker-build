# Docker Build System

This is my playground for testing my Docker build system.
Docker images are rebuilt only, when the base image or
the build context has changed. For a detailed description
see [docker_build.md](docker_build.md).

It contains the following Docker images, that are designed
to work within [GNS3](https://github.com/GNS3).

| Image       | Registry | Description |
| ----------- | -------- | ------------|
| alpine-be   | [ghcr.io/b-ehlers/alpine-be](https://github.com/users/b-ehlers/packages/container/package/alpine-be)     | Nicer alpine appliance |
| ipterm-base | [ghcr.io/b-ehlers/ipterm-base](https://github.com/users/b-ehlers/packages/container/package/ipterm-base) | Networking Toolbox, base image |
| ipterm      | [ghcr.io/b-ehlers/ipterm](https://github.com/users/b-ehlers/packages/container/package/ipterm)           | Networking Toolbox, CLI version |
| webterm     | [ghcr.io/b-ehlers/webterm](https://github.com/users/b-ehlers/packages/container/package/webterm)         | Networking Toolbox, Web/GUI version |
