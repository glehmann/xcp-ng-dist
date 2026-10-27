# xcp-ng-dist

The [XCP-ng](https://xcp-ng.org/) distribution: the specs of its packages, the lock of the upstream packages they
build with, and the files of its installation ISO, built by [xcraft](https://github.com/glehmann/xcraft).

```
base/<pkg>/             a package of the base repository: its spec, patches and small sources
iso/                    the files of the installation ISO
xcraft.toml             the settings: build environment, platforms, remote storage, publishing
xcraft.lock             the versions of the upstream packages, for all the architectures, and what builds found
pyproject.toml          the version of xcraft, pinned
```

```
uv sync                 # xcraft, in its pinned version
uv run xcraft --help
uv run xcraft build     # all the packages, or the ones given
```

## Installer development

Use the [installer-vm agent skill](.agents/skills/installer-vm/SKILL.md) for VM setup, console control, log retrieval,
and the current development-session handoff.

## Signing uploads

The build workflow signs builds and compiler caches with the test key whose public fingerprint is in
`remote.main.build_keys` in `xcraft.toml`. GitHub Actions stores its armored private key in `SIGNING_PRIVATE_KEY` and its
fingerprint in the repository variable `SIGNING_KEY_FINGERPRINT`. The workflow imports the key into a temporary GPG
keyring after building, signs uploads with `--key` to the `--to main` bucket, then removes the keyring. Sources are
fetched explicitly before uploads. Pull-request jobs do not import the key or push artifacts.

On pushes to `master`, the x86 job also runs `xcraft publish --locked --to main --stage incoming --arch x86_64_v2`
with the signing key. Repositories are published under `repos/9.0/incoming/latest/`, and ISOs under
`isos/9.0/incoming/latest/`. Arm64 publishing is excluded while its build is broken. Developer publishing defaults
to a stage named after the current OS user; `--stage` selects another name.

With the same test key imported into your GPG keyring and the S3 credentials configured:

```sh
uv run xcraft fetch sources
uv run xcraft push --to main --key F7685175612B78858C4211D861ECBE94C30BC7B5
uv run xcraft push ccache --to main --key F7685175612B78858C4211D861ECBE94C30BC7B5
```

No `[sign]` setting is needed. Without `--key`, xcraft uses your checkout's developer key when one exists; your
checkout trusts its own signatures, but other checkouts only trust the configured public keys and their own key.

## Developer bucket

The main bucket is served at `https://91.98.220.14`; the independent `xcraft-dev` bucket is served at
`https://91.98.220.14:8443`. Both endpoints provide public reads and authenticated S3 writes. Developer S3 keys have
read/write permissions only on `xcraft-dev`; the CI key keeps its permissions on main.

Export your developer key as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. Upload commands default to dev:

```sh
uv run xcraft push sources
uv run xcraft push builds
uv run xcraft push ccache
uv run xcraft publish --arch x86_64_v2
```

Build, ccache and publication uploads need your checkout's signing key, created once with `uv run xcraft key create`,
or an explicit `--key`. Sources are checked against their committed hashes and need no signing key.

See the README of xcraft for everything else.
