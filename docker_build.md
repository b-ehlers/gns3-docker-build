# Docker Build System

The regular Docker build system has the disadvantage,
that only the cache system prevents a repetitive rebuild.
But when running the build in a VM this cache is initially
empty, resulting in a rebuild of all images on every run.
This not only increases the CPU load of the VM, but also
creates a lot of updated Docker images, that differ only
in the timestamps of the files.

This Docker build system wants to improve this situation.
It rebuilds only, when the base image or the build context
has changed. There are some other situations, where an
image needs to be recreated, that are not detected.
This mainly affects installation packages and external
files, that got an update. Then a manual trigger is needed.


## Build Tool

The `docker_build` tool reads a configuration file and
then starts building images with `docker buildx build`.

If `docker_build` is launched without arguments, it checks
all configured images for an update of the base image.
Additionally it checks, if `git` shows an update of
the directory containing the docker build context.
When at least one of these conditions is met, the tool
starts a rebuild of that image.

Alternatively, `docker_build` can also be run with some
image names as arguments. Then these images will be rebuilt.

As a special case, if the first argument is `all`, then
all images are rebuild, except those following `all`.


## Configuration File

The build tool reads the `docker_images` configuration
file, located in the current directory. For each target
image, it contains its name, its context directory and
optionally the base image and some build options.

The fields are separated by one or more \<tab\> characters.
Comments start with a `#` as its first field character.
An empty line or an all-comments line is ignored.

A line with only one field is used for build options,
which are effective from that point until they are redefined.
This global build option and an optional image specific option
are combined and sent to the `docker buildx` command.

Here an example:

```
# Name		Directory	[Base Image]	[Build Options]

--platform=linux/arm64,linux/amd64		# global options

alpine-1	alpine-1	alpine		--image-specific-option
alpine-1:test	alpine-1a	--another-image-specific-option
```

The target image may contain the full name, in which
case it will contain one or more '/' characters.

Another option is to specify only the last part of the
image name. Then `docker_build` uses the `DOCKER_ACCOUNT`
environment variable as its initial part. For example, an
DOCKER_ACCOUNT value of "ghcr.io/b-ehlers" plus the image
name of "alpine-1" results in "ghcr.io/b-ehlers/alpine-1".

This method is not applied to the base images, they always
have to contain the complete name.


## Workflow Definition

[GitHub Actions](https://docs.github.com/en/actions)
uses YAML files in the .github/workflows directory
to define, which tasks should be run.

Before `docker_build` can be run the following steps
need to be done:

* Install python dateutil
* Check out the repository code
* Set up QEMU (for multi-arch building)
* Set up Docker Buildx
* Login to the Container Registry

Then `docker_build` can be executed,
normally without any arguments.

But what, when an image build needs to be forced?

For that a tag needs to be created, that contains the list
of images, joined by a `_` and beginning with a `_`.
For example, if images abc and def should both be
rebuild, create the tag `_abc_def`. The underscore at the
beginning was choosen to allow the use of "normal" tags,
that won't interfere with the build system.

Furthermore a tag may not contain a `:`, but images can.
Therefore a `;` was choosen to replace the `:` of an image.

The following part of a shell script undoes this replacement.
It generates a list of images out of a tag and stores them as
positional parameters:

```
if [ "$GITHUB_REF_TYPE" = "tag" ]; then
	set -f
	set -- $(echo "${GITHUB_REF_NAME#_}" | tr ';_' ': ')
	set +f
fi
```

