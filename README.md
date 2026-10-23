# xcp-ng-dist

The [XCP-ng](https://xcp-ng.org/) distribution: the specs of its packages, the lock of the upstream packages they
build with, and the files of its installation ISO, built by [xcraft](https://github.com/glehmann/xcraft).

```
base/<pkg>/             a package of the base repository: its spec, patches and small sources
iso/                    the files of the installation ISO
xcraft.toml             the settings: build environment, platforms, remote storage, publishing
xcraft.<arch>.lock      the versions of the upstream packages, for each architecture
pyproject.toml          the version of xcraft, pinned
```

```
uv sync                 # xcraft, in its pinned version
uv run xcraft --help
uv run xcraft build     # all the packages, or the ones given
```

See the README of xcraft for everything else.
