# FalkorDB Enterprise Helm Chart SDLC

This document describes the release flow for the FalkorDB Enterprise Helm chart.

## Workflows

Two workflows own the chart lifecycle:

- `Helm Chart` (`.github/workflows/helm-chart.yml`) validates changes on pushes, pull requests, and manual runs. It lints, renders, packages, and runs the k3d install/uninstall sanity test. It does not publish artifacts.
- `Publish FalkorDB Enterprise Helm Chart` (`.github/workflows/publish-enterprise-helm-chart.yml`) publishes the release artifact. It can be run manually with `workflow_dispatch` or called by another workflow with `workflow_call`.

The chart deploys images produced by separate workflows:

- `Build Enterprise Core Image` (`.github/workflows/build-enterprise.yml`) builds and publishes the underlying FalkorDB Enterprise core image with the FalkorDB, LDAP, and tier module matrix.
- `Build Admin Server & UI Images` (`.github/workflows/build.yml`) builds and publishes the admin server and admin UI images that are packaged by the Enterprise Helm chart.

The required order is:

1. Upstream FalkorDB, LDAP, or tier repository releases dispatch `Build Enterprise Core Image`, which updates the underlying `registry.falkordb.cloud/falkordb/falkordb-enterprise-db` image.
2. `Publish FalkorDB Enterprise Helm Chart` calls `Build Admin Server & UI Images` with `image_tag=<release_version>`, so `registry.falkordb.cloud/falkordb/falkordb-enterprise-server:<release_version>` and `registry.falkordb.cloud/falkordb/falkordb-enterprise-ui:<release_version>` exist before the chart is pushed.
3. The chart is packaged, pushed to `registry.falkordb.cloud/falkordb`, and attached to the GitHub Release only after the admin server and admin UI image build succeeds.

registry.falkordb.cloud is the only registry this repository publishes to, for every first-party image and for the chart. Do not publish a chart for image tags that do not exist in registry.falkordb.cloud. ghcr.io still hosts charts and images released from other FalkorDB repositories (the KubeBlocks addon, falkordb-browser, dm-sql-to-falkordb), which this chart depends on and the mirror job copies in.

## Versioning

Every published chart release must have an explicit `release_version` input. Use SemVer without a leading `v`, for example `0.2.0`.

The publish workflow uses `release_version` for:

- the packaged Helm chart version
- the OCI chart tag
- the GitHub Release tag, formatted as `v<release_version>`
- the packaged default admin server and admin UI image tags
- the packaged `appVersion`, unless `app_version` is supplied

Use `app_version` only when the chart should advertise a different application version than `release_version`. It used to be the *only* way `appVersion` was ever written, which left the checked-in placeholder `1.0.0` in every published chart; it is now stamped on every publish.

The checked-in chart values should keep `adminServer.image.tag` and `adminUi.image.tag` aligned with the checked-in chart `version`. During publishing, the workflow stamps both image tags to `release_version` before linting, rendering, and packaging. This keeps installed defaults traceable without relying on mutable `latest` tags.

## Release Notes And Compatibility

`CHANGELOG.md` at the repository root is the source of truth for release notes. Two things are generated from it plus the git tags:

- `docs/upgrades/changelog.mdx`, the published changelog
- `docs/reference/compatibility.mdx`, the version compatibility matrix

Regenerate both after editing `CHANGELOG.md`:

```bash
node scripts/generate-release-docs.mjs
```

The `Helm Chart` workflow runs the same command with `--check` and fails when the generated pages are stale. The generator needs the full tag history, so CI checks out with `fetch-depth: 0`.

### Cutting A Release

Cut the release on the branch **before** tagging, because the tag is what the compatibility matrix reads:

```bash
node scripts/generate-release-docs.mjs --release 0.5.0 --channel stable
```

That moves everything under `## [Unreleased]` into a `## [0.5.0] - <today> (stable)` section, opens a fresh empty `## [Unreleased]`, updates the compare links at the bottom of the file, and regenerates both pages. `--channel` defaults to `stable` and accepts `beta` or `lts`; `--date` overrides the date. It refuses to run when `## [Unreleased]` is empty or the version already has a section.

If the release has incompatible changes, add a `### Breaking changes` section linking to a guide in `docs/upgrades/migrations/`, then regenerate. Commit the result, then tag `v0.5.0`.

The publish workflow reads the section for `release_version` out of `CHANGELOG.md` and uses it as the GitHub Release notes. Its `Prepare Release Inputs` job fails if that section is missing, before anything is built or published.

## Release Channels

| Channel | Version form | Cut and tagged from | GitHub Release | Installed by |
| --- | --- | --- | --- | --- |
| `stable` | `0.5.0` | `release/0.5.x` | marked latest | the default install |
| `beta` | `0.5.0-beta.1` | `release/0.5.x` | marked prerelease | `--channel beta` |
| `lts` | `0.4.7` | `release/0.4.x` | marked latest | `--version 0.4.7` |

Beta releases are prerelease SemVer. This is what makes the channel work: Helm excludes prerelease versions when it resolves a chart reference that has no `--version`, so a published beta can never become the default install. `install.sh --channel beta` passes `--devel`, which opts back in.

The publish workflow reads the channel out of the `CHANGELOG.md` heading for the version being released and stamps it into `Chart.yaml` as the `falkordb.io/release-channel` annotation. Helm stores that in the release metadata, so the admin server reports the channel on the Diagnostics page and in the support package manifest. Packaging fails if the heading declares no channel.

`lts` is a maintenance line, not a different kind of build. An LTS release is a normal patch release cut from a long-lived `release/X.Y.x` branch that keeps receiving backported fixes after `main` has moved on.

### Cutting A Stable Minor Release

1. Branch from `main`, once per minor version:

   ```bash
   git switch main && git pull
   git switch -c release/0.5.x
   git push -u origin release/0.5.x
   ```

2. Cut the changelog on the release branch and commit it:

   ```bash
   node scripts/generate-release-docs.mjs --release 0.5.0 --channel stable
   git add CHANGELOG.md docs/upgrades/changelog.mdx docs/reference/compatibility.mdx
   git commit -m "Release 0.5.0"
   git push
   ```

3. Wait for the `Helm Chart` workflow to pass on the release branch. It validates release branches as well as `main` and `dev`.

4. Tag the commit that CI passed on, and push the tag. The tag is what triggers publishing:

   ```bash
   git tag v0.5.0
   git push origin v0.5.0
   ```

5. Merge the release branch back into `main` so the changelog and generated pages are on the trunk. Keep the branch: patch releases and any LTS backports are cut from it.

### Cutting A Beta

Same branch, prerelease version:

```bash
node scripts/generate-release-docs.mjs --release 0.5.0-beta.1 --channel beta
git commit -am "Release 0.5.0-beta.1" && git push
git tag v0.5.0-beta.1 && git push origin v0.5.0-beta.1
```

When the stable release is later cut from the same branch, the generator folds every `0.5.0-beta.*` section into the `0.5.0` section and removes them, so the stable release notes describe everything since `0.4.x` rather than only what changed after the last beta. The beta GitHub Releases and their published chart versions are left alone.

### Cutting A Patch Or LTS Release

Patch releases never come from `main`. Cherry-pick onto the release branch so the release line only contains what was intended:

```bash
git switch release/0.4.x
git cherry-pick <commit>
```

Add the entry under `## [Unreleased]` on that branch, then cut, tag, and push exactly as above with `--release 0.4.7`. Use `--channel lts` when the line is a supported LTS line, `stable` otherwise.

Do not merge an LTS branch back into `main` wholesale — it is behind. Land the fix on `main` separately, normally first.

A version can also be promoted to `lts` after the fact by editing its heading in `CHANGELOG.md` and regenerating.

## Pull Request Flow

1. Update chart templates, values, dependencies, install scripts, or docs.
2. Add an entry under `## [Unreleased]` in `CHANGELOG.md` for any user-visible change, then run:

   ```bash
   node scripts/generate-release-docs.mjs
   ```

3. If dependencies changed, run:

   ```bash
   helm dependency update helm/falkordb-enterprise
   ```

4. Run the focused local checks:

   ```bash
   helm lint helm/falkordb-enterprise --set adminServer.secret.jwtSecret=ci-chart-validation-secret-at-least-32-chars
   helm template falkordb-enterprise helm/falkordb-enterprise --set adminServer.secret.jwtSecret=ci-chart-validation-secret-at-least-32-chars >/tmp/falkordb-enterprise-render.yaml
   bash -n scripts/install.sh
   bash -n scripts/uninstall.sh
   node scripts/generate-release-docs.mjs --check
   git diff --check
   ```

5. Open a PR and wait for the `Helm Chart` workflow to pass.
6. Merge only after the k3d sanity install and uninstall pass.

## Publishing From GitHub Actions

Run `Publish FalkorDB Enterprise Helm Chart` manually from the Actions tab, or call it from another workflow.

Required input:

- `release_version`: chart and release version, without a leading `v`

Optional input:

- `app_version`: packaged chart `appVersion` override; defaults to `release_version`

Manual dispatch example:

```text
release_version: 0.2.0
app_version: 1.0.0
```

Reusable workflow example:

```yaml
jobs:
  publish-chart:
    uses: FalkorDB/FalkorDB-Enterprise/.github/workflows/publish-enterprise-helm-chart.yml@main
    permissions:
      contents: write
      packages: write
    with:
      release_version: 0.2.0
      app_version: 1.0.0
```

The workflow publishes:

- OCI chart: `oci://registry.falkordb.cloud/falkordb/falkordb-enterprise:<release_version>`
- GitHub Release: `falkordb-enterprise-chart-v<release_version>`
- Release asset: `falkordb-enterprise-<release_version>.tgz`

## Installing A Published Chart

```bash
helm install falkordb-enterprise \
  oci://registry.falkordb.cloud/falkordb/falkordb-enterprise \
  --version 0.2.0 \
  --namespace falkordb-system \
  --create-namespace \
  --set adminServer.secret.jwtSecret='<strong-random-32-plus-character-jwt-secret>'
```

For full installs, prefer `scripts/install.sh`, which installs KubeBlocks separately, configures image pull credentials, and installs the Enterprise chart.

## Upgrading A Published Chart

For normal release upgrades, do not use `helm upgrade --reuse-values`. Helm preserves all previously supplied values when `--reuse-values` is set, including old image tag overrides such as `adminServer.image.tag` and `adminUi.image.tag`. That can upgrade the chart version while leaving the running admin server or admin UI containers pinned to the previous release image.

Prefer a small environment-specific values file that contains only settings that must persist across releases, such as secrets, storage classes, image pull secrets, browser base path settings, and production-specific flags. Then upgrade without `--reuse-values` so the new chart defaults provide the release image tags:

```bash
helm upgrade falkordb-enterprise \
  oci://registry.falkordb.cloud/falkordb/falkordb-enterprise \
  --version 0.2.1 \
  --namespace falkordb-system \
  -f production-values.yaml \
  --wait --timeout 20m
```

If an emergency upgrade must use `--reuse-values`, set release-sensitive image tags explicitly in the same command:

```bash
helm upgrade falkordb-enterprise \
  oci://registry.falkordb.cloud/falkordb/falkordb-enterprise \
  --version 0.2.1 \
  --namespace falkordb-system \
  --reuse-values \
  --set adminServer.image.tag=0.2.1 \
  --set adminUi.image.tag=0.2.1 \
  --wait --timeout 20m
```

## Release Checklist

Before publishing:

- The release branch contains the intended chart changes.
- `CHANGELOG.md` has a section for the version being released, cut with `node scripts/generate-release-docs.mjs --release <release_version>` and committed. The publish workflow refuses to run without it.
- `helm/falkordb-enterprise/Chart.lock` is current when dependencies changed.
- The `Helm Chart` validation workflow passed on the commit being released.
- The Enterprise core image tag was built by `Build Enterprise Core Image` when the release depends on a new core image.
- The admin server and admin UI image tags are built automatically by `Publish FalkorDB Enterprise Helm Chart` before chart publishing.
- The chosen `release_version` has not already been published as a GHCR chart tag or GitHub Release tag.

After publishing:

- Confirm the workflow summary contains the expected OCI chart reference.
- Confirm the GitHub Release exists and includes the packaged `.tgz` asset.
- Run a smoke install against the published OCI chart or the install script before announcing the release.