# FalkorDB Enterprise Helm Chart SDLC

This document describes the release flow for the FalkorDB Enterprise Helm chart.

## Workflows

Two workflows own the chart lifecycle:

- `Helm Chart` (`.github/workflows/helm-chart.yml`) validates changes on pushes, pull requests, and manual runs. It lints, renders, packages, and runs the k3d install/uninstall sanity test. It does not publish artifacts.
- `Publish FalkorDB Enterprise Helm Chart` (`.github/workflows/publish-enterprise-helm-chart.yml`) publishes the release artifact. It can be run manually with `workflow_dispatch` or called by another workflow with `workflow_call`.
- `Cut Release` (`.github/workflows/cut-release.yml`) and `Tag Release` (`.github/workflows/tag-release.yml`) automate a release around the publish workflow. See [Cutting A Release](#cutting-a-release).

The chart deploys images produced by separate workflows:

- `Build Enterprise Image` (`.github/workflows/build-enterprise.yml`) builds and publishes the `falkordb-enterprise-db` image: the FalkorDB core image with the enterprise module added. Every build is tagged `v<core>-<module>` (e.g. `v4.22.0-1.2.3`), which is immutable; the bare `v<core>` tag is moved by each module release.
- `Bump FalkorDB Version` (`.github/workflows/bump-falkordb-version.yml`) opens an issue and a pull request that move the chart to a newly published `falkordb-enterprise-db` image. See [New FalkorDB releases](#new-falkordb-releases).
- `Build Admin Server & UI Images` (`.github/workflows/build.yml`) builds and publishes the admin server and admin UI images that are packaged by the Enterprise Helm chart.

The required order is:

1. Releases of `FalkorDB/falkordb` and `FalkorDB/falkordb-enterprise-module` dispatch `Build Enterprise Image`, which publishes `registry.falkordb.cloud/falkordb/falkordb-enterprise-db` and then opens the chart bump PR. The PR is reviewed and merged into `main` like any other change.
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

A release is one **Run workflow** click and one pull request review:

1. Run **Cut Release** from the Actions tab with `version` (for example `1.1.0` or `1.1.0-beta.1`, no leading `v`). `channel` defaults to `auto`, which picks `beta` for a prerelease version and `stable` otherwise; choose `lts` explicitly. Leave `base` empty.
2. Review and merge the `chore(release): cut <version>` pull request it opens into `release/<major>.<minor>.x`. Edit the changelog section on that branch first if the notes need it.
3. **Tag Release** does the rest when the PR merges: it tags the merge commit `v<version>`, calls the publish workflow, and, for `stable` and `beta`, opens a `chore(release): merge release/<major>.<minor>.x back into main` PR.
4. Merge the merge-back PR with a merge commit, not squash or rebase. Until it merges, the `Release Docs` check fails on PRs against `main`: the matrix lists the new tag, but `main` has no changelog section for it yet. So merge it soon.

Nothing has to land on the release branch after the release PR. The release PR already renders the compatibility matrix as it reads once the tag exists, and the tag goes on that PR's merge commit, so tagging changes no generated page.

#### How the merge-back PR is built

Tag Release cuts `chore/merge-back-<version>` from the release branch and merges `main` into it there. The release branch itself is never changed. Resolving a merge-back conflict by merging `main` into the release branch would put `main`'s unreleased work on the release line.

Two files go wrong in every merge-back if git merges them as text, so the job fixes them before opening the PR:

- `CHANGELOG.md`: the release side moved `## [Unreleased]` into a version section, while `main` kept adding entries under `## [Unreleased]`. The text merge either conflicts or, worse, merges cleanly and files `main`'s new entries under the released version, next to the lines they were written beside. `.github/scripts/merge_back_changelog.mjs` keeps the merge and moves every entry `main` added since the merge base back under `## [Unreleased]`. It compares against the merge base, so an entry reworded in the release PR still counts as released, and a fix cherry-picked onto the release line, already in a version section there, stays out of `## [Unreleased]`. The PR description lists the entries it kept. If `main` edited or removed an entry after the release shipped it, the script refuses (exit 3): a clean merge may have carried `main`'s wording into the released section, and an edit cannot be told from a new entry. The job then treats `CHANGELOG.md` as an unresolved conflict and lists those entries in the PR.
- The generated pages (`docs/upgrades/changelog.mdx`, `docs/reference/compatibility.mdx`): rebuilt with `node scripts/generate-release-docs.mjs`, using the generator `main` brings, never merged as text.

A conflict in any other file, or a refused `CHANGELOG.md`, is left to a person. The job then opens the PR from the release branch's tip and lists the files. Merge `main` into `chore/merge-back-<version>` (not into the release branch), resolve, run the two commands above, and push.

What Cut Release enforces:

- The release branch already has `tag-release.yml` and the current publish workflow. A push runs the workflows on the pushed branch, not on `main`. A release branch cut before this automation (such as `release/1.0.x`) would merge the release PR and never be tagged. Cherry-pick the automation onto such a branch with a PR first.

- Releases are cut from `release/<major>.<minor>.x` only, never from `main`. A `base` other than that is refused.
- The release branch is created from `main` only for the first release of a minor (`X.Y.0` or an `X.Y.0` prerelease). Any other version fails if its branch does not exist.
- The channel matches the version form: `beta` needs a prerelease version, and `stable` or `lts` refuses one.
- It fails if tag `v<version>` or branch `chore/release-<version>` already exists.

It runs the same generator as the manual flow:

```bash
node scripts/generate-release-docs.mjs --release 0.5.0 --channel stable
```

That moves everything under `## [Unreleased]` into a `## [0.5.0] - <today> (stable)` section, opens a fresh empty `## [Unreleased]`, updates the compare links at the bottom of the file, and regenerates both pages. `--channel` defaults to `stable` and accepts `beta` or `lts`; `--date` overrides the date. It refuses to run when `## [Unreleased]` is empty or the version already has a section. The release is cut on the branch **before** tagging, because the tag is what the compatibility matrix reads.

If the release has incompatible changes, add a `### Breaking changes` section linking to a guide in `docs/upgrades/migrations/` on the release PR's branch, then regenerate.

The publish workflow reads the section for `release_version` out of `CHANGELOG.md` and uses it as the GitHub Release notes. Its `Prepare Release Inputs` job fails if that section is missing, before anything is built or published.

#### How Tag Release works

It runs on the push that merging the PR makes to the release branch, not on the `pull_request` event. A reusable workflow inherits its caller's event, and `build.yml` never pushes images on a `pull_request` event. It also builds `refs/pull/N/merge` there, not the merge commit. On every other push to a `release/**` branch it finds no `chore/release-*` PR for the commit and does nothing.

Release jobs are grouped per version, never per branch. GitHub keeps only one pending run per concurrency group, so a branch-wide group would let a later push to the branch replace a queued release merge.

The tag is annotated and pushed with `GITHUB_TOKEN`. That token does not start workflows, so the `push: tags: v*` trigger of the publish workflow does not fire, and Tag Release calls it directly with `workflow_call`. The tag message ends with `Release-Automation: tag-release`. The publish workflow skips a tag push carrying that line, so a release is still published once if the tag is ever pushed with a token that does start workflows. A tag pushed by hand has no such line and publishes as before.

Re-running a failed Tag Release run is safe: a tag already on the merge commit and an open PR are reused. If publishing failed, **Re-run failed jobs** on the Tag Release run, or run the publish workflow by hand with `release_version`.

#### Tokens and repository settings

- `RELEASE_TOKEN` (recommended): a fine-grained PAT with **Contents** and **Pull requests** read and write on this repository. Cut Release and Tag Release use it to push branches and open PRs, falling back to `CHART_BUMP_TOKEN` and then `GITHUB_TOKEN`. GitHub does not start workflows for a branch pushed or a PR opened with `GITHUB_TOKEN`. Without a PAT, the required `Helm Chart` checks do not start on the release PR or the merge-back PR until someone closes and reopens the PR or pushes to it. Cut Release warns about this in the PR. A GitHub App installation token expires after an hour, so it cannot be stored as this secret.
- "Allow GitHub Actions to create and approve pull requests" must be enabled in the repository settings when no PAT is set.
- Tags are always pushed with `GITHUB_TOKEN`. If a ruleset protects `v*` tags, let GitHub Actions bypass it. If a ruleset restricts creating `release/**` branches, let the `RELEASE_TOKEN` owner (or GitHub Actions) bypass it.
- The publish workflow's own secrets (`GITEA_REGISTRY_USERNAME`, `GITEA_REGISTRY_TOKEN`, `COSIGN_PRIVATE_KEY`, `COSIGN_PASSWORD`) reach it through `secrets: inherit` and need no change.

#### Manual fallback

When the workflows are unavailable, use the commands in the sections below. They are the same steps by hand.

## Release Channels

| Channel | Version form | Cut and tagged from | GitHub Release | Installed by |
| --- | --- | --- | --- | --- |
| `stable` | `0.5.0` | `release/0.5.x` | marked latest | the default install |
| `beta` | `0.5.0-beta.1` | `release/0.5.x` | marked prerelease | `--channel beta` |
| `lts` | `0.4.7` | `release/0.4.x` | marked latest | `--version 0.4.7` |

Beta releases are prerelease SemVer. This is what makes the channel work: Helm excludes prerelease versions when it resolves a chart reference that has no `--version`, so a published beta can never become the default install. `install.sh --channel beta` passes `--devel`, which opts back in.

The publish workflow reads the channel out of the `CHANGELOG.md` heading for the version being released and stamps it into `Chart.yaml` as the `falkordb.cloud/release-channel` annotation. Helm stores that in the release metadata, so the admin server reports the channel on the Diagnostics page and in the support package manifest. Packaging fails if the heading declares no channel.

`lts` is a maintenance line, not a different kind of build. An LTS release is a normal patch release cut from a long-lived `release/X.Y.x` branch that keeps receiving backported fixes after `main` has moved on.

### Cutting A Stable Minor Release

Automated: run **Cut Release** with `version: 0.5.0`. It creates `release/0.5.x` from `main` if the branch does not exist yet. Keep the branch after the release: patch releases and any LTS backports are cut from it.

By hand:

1. Branch from `main`, once per minor version:

   ```bash
   git switch main && git pull
   git switch -c release/0.5.x
   git push -u origin release/0.5.x
   ```

2. Cut the changelog on a branch off the release branch, and open a PR into it:

   ```bash
   git switch -c chore/release-0.5.0
   node scripts/generate-release-docs.mjs --release 0.5.0 --channel stable
   git add CHANGELOG.md docs/upgrades/changelog.mdx docs/reference/compatibility.mdx
   git commit -m "chore(release): cut 0.5.0"
   git push -u origin chore/release-0.5.0
   gh pr create --base release/0.5.x --title "chore(release): cut 0.5.0"
   ```

   Merging it runs Tag Release. If that succeeds, it replaces steps 3 to 5: merge the merge-back PR it opens.

3. Wait for the `Helm Chart` workflow to pass on the release branch. It validates release branches as well as `main` and `dev`.

4. Switch back to the release branch, bring it up to date with the merged PR, and tag the commit that CI passed on. A tag pushed by hand triggers publishing:

   ```bash
   git switch release/0.5.x
   git pull --ff-only
   git tag v0.5.0
   git push origin v0.5.0
   ```

5. Merge the release branch back into `main` through a branch of its own, so the changelog and generated pages are on the trunk. See [How the merge-back PR is built](#how-the-merge-back-pr-is-built) for why:

   ```bash
   git fetch origin --tags
   git switch -c chore/merge-back-0.5.0 origin/release/0.5.x
   git merge --no-ff --no-commit origin/main
   # Resolve any conflict outside CHANGELOG.md and the generated pages, then:
   # If the script exits 3, main edited a shipped entry: fix CHANGELOG.md by hand.
   if git rev-parse -q --verify MERGE_HEAD >/dev/null; then
     node .github/scripts/merge_back_changelog.mjs
   fi
   node scripts/generate-release-docs.mjs
   git add CHANGELOG.md docs/upgrades/changelog.mdx docs/reference/compatibility.mdx
   if git rev-parse -q --verify MERGE_HEAD >/dev/null; then
     git commit --no-edit
   elif ! git diff --cached --quiet; then
     git commit -m "docs: regenerate release docs for 0.5.0"
   fi
   git push -u origin chore/merge-back-0.5.0
   gh pr create --base main --title "chore(release): merge release/0.5.x back into main after 0.5.0"
   ```

   Merge it with a merge commit.

### Cutting A Beta

Same branch, prerelease version. Automated: run **Cut Release** with `version: 0.5.0-beta.1`; the channel defaults to `beta`. The first beta of a minor creates `release/0.5.x`.

By hand, as for a stable release with:

```bash
node scripts/generate-release-docs.mjs --release 0.5.0-beta.1 --channel beta
```

and tag `v0.5.0-beta.1`. Betas are tagged on the release branch too, never on `main`.

When the stable release is later cut from the same branch, the generator folds every `0.5.0-beta.*` section into the `0.5.0` section and removes them, so the stable release notes describe everything since `0.4.x` rather than only what changed after the last beta. The beta GitHub Releases and their published chart versions are left alone.

### Cutting A Patch Or LTS Release

Patch releases never come from `main`. Cherry-pick onto the release branch, through a PR, so the release line only contains what was intended:

```bash
git switch release/0.4.x
git cherry-pick <commit>
```

Add the entry under `## [Unreleased]` on that branch. Then run **Cut Release** with `version: 0.4.7`, or follow the manual steps above with `--release 0.4.7`. Choose `channel: lts` when the line is a supported LTS line; `auto` gives `stable`. Cut Release refuses a patch whose release branch does not exist.

Do not merge an LTS branch back into `main` wholesale: it is behind. Tag Release opens no merge-back PR for an `lts` release. Instead it opens a `docs(compatibility): list <version> on main` PR. The generator lists every tag whatever branch it is on, so `main`'s `Release Docs` check fails until that PR merges. The PR also copies the release's `CHANGELOG.md` section onto `main` (`.github/scripts/import_changelog_section.mjs`), where the generator reads the channel and notes from. Land the fix on `main` separately, normally first.

A version can also be promoted to `lts` after the fact by editing its heading in `CHANGELOG.md` and regenerating.

## New FalkorDB releases

The chart pins the immutable `v<core>-<module>` tag in `falkordb-addon.falkordbVersions`, so a new core or enterprise module only reaches users through a chart release. That step is automated up to the pull request:

1. A release of either upstream repository dispatches `Build Enterprise Image`.
2. When the image was built against the latest module, for the default (glibc) variant, its `bump-chart` job calls `Bump FalkorDB Version`. The workflow can also be run by hand with `falkordb_version` and `module_version`, for an image that is already published.
3. `.github/scripts/bump_falkordb_version.py` edits `values.yaml`, the image tags in `docs/deployment/private-images.mdx` and `docs/reference/supply-chain.mdx`, and adds a `CHANGELOG.md` `[Unreleased]` entry:
   - A newer core becomes the default and is added to `mirrorVersions` ahead of the older releases, which stay listed so existing deployments can upgrade in place.
   - A new module for the current core replaces that core's tag. The addon names a release after its version, so a version can only be listed once.
     Every running deployment on that core moves to the new module on the next chart upgrade (a rolling restart); users cannot stay on the previous module.
   - An older core, an older module than the pinned one, a prerelease, or a tag that is already pinned changes nothing. A new major version only opens an issue, because it needs new component definitions in the addon.
   - The script refuses to edit a `mirrorVersions` block containing anything but version/imageTag pairs, rather than dropping it.
4. The workflow checks the image exists in registry.falkordb.cloud, regenerates the docs, and lints and renders the chart.
5. `.github/scripts/open_bump_pr.sh` opens an issue labelled `falkordb-version-bump` with the upstream release notes, and a pull request against `main` that closes it. Open bump PRs for older tags, and their issues, are closed as superseded; their branches are kept.

The reviewer rewrites the generated changelog entry from the release notes, in particular calling out a one-way upgrade (a new RDB encoding) with a "take a backup first" warning, merges the PR, and then cuts a chart release as described above.

The workflow uses the `CHART_BUMP_TOKEN` secret (a fine-grained PAT) when it is set, and `GITHUB_TOKEN` otherwise. GitHub does not start workflows for a pull request opened with `GITHUB_TOKEN`, so without `CHART_BUMP_TOKEN` the `Helm Chart` checks only run after another push to the branch. `GITHUB_TOKEN` also needs "Allow GitHub Actions to create and approve pull requests" enabled in the repository settings.

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
- `CHANGELOG.md` has a section for the version being released, cut by `Cut Release` (or with `node scripts/generate-release-docs.mjs --release <release_version>`) and merged into the release branch. The publish workflow refuses to run without it.
- `helm/falkordb-enterprise/Chart.lock` is current when dependencies changed.
- The `Helm Chart` validation workflow passed on the commit being released.
- The `falkordb-enterprise-db` tag the chart pins was built by `Build Enterprise Image`.
- The admin server and admin UI image tags are built automatically by `Publish FalkorDB Enterprise Helm Chart` before chart publishing.
- The chosen `release_version` has not already been published as a GHCR chart tag or GitHub Release tag.

After publishing:

- Confirm the workflow summary contains the expected OCI chart reference.
- Confirm the GitHub Release exists and includes the packaged `.tgz` asset.
- Run a smoke install against the published OCI chart or the install script before announcing the release.
- For stable and beta, merge the merge-back PR into `main`.