# Tools

## Prune GitHub Container Registry

The unused/untagged container in the GitHub container registry
are not automatically deleted, they stick around until they are
deleted by the user.

For details, see this discussion:
[Are tag-less container images deleted?](https://github.community/t/are-tag-less-container-images-deleted/132977)

That leads to an ever increasing space usage, which will result
in increasing costs for private repositories. The `ghcr_prune`
program is able to prune these unneeded containers. It is based on
<https://github.com/airtower-luna/hello-ghcr/blob/main/ghcr-prune.py>.

```
ghcr_prune.py - Prune old versions of GHCR container.

usage: ghcr_prune.py [-h] [--dry-run] --prune-age DAYS
                     container [container ...]

positional arguments:
  container         images to prune

optional arguments:
  -h, --help        show this help message and exit
  --dry-run, -n     do not actually prune images, just list them
  --prune-age DAYS  delete untagged images older than DAYS days
```
