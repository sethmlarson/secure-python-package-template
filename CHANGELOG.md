# Changelog
<!-- scriv-insert-here -->

<a id='changelog-0.7.0'></a>
## 0.7.0 (2023-04-22)

### Added

- Added instructions on how to configure a Trusted Publisher.

<a id='changelog-0.6.0'></a>
## 0.6.0 (2023-01-10)

### Added

- Added the `repo_token` parameter to the `ossf/scorecard-action` GitHub Action.

- Added documentation on how to upgrade dependencies in lock files manually with `pip-compile` and the `--upgrade-package` option.

### Changed

- Changed Dependabot configuration to reduce the total number of opened pull requests without sacrificing timely security fixes or upgrades signalling a new major version.

- Changed the `publish` job to only use the `publish` GitHub Environment, rather than both `publish` and `build` jobs.
  This means that there will only be one approval required to publish to PyPI since all other steps before can either be
  rolled back without harming users (ie deleting GitHub releases, git tags) or are idempotent (provenance attestation).

<a id='changelog-0.5.0'></a>
## 0.5.0 (2022-12-10)

### Added

- Added instructions for configuring signed commits and tags automatically from git.
- Added security policy and instructions for configuring private vulnerability reporting.

<a id='changelog-0.4.0'></a>
## 0.4.0 (2022-12-09)

### Added

- Added scriv for tracking changelog fragments

### Changed

- Changed from flit to hatch for building the package

## 0.3.0

### Added

- Added deployment pipeline to PyPI
- Added provenance signing with SLSA GitHub Action
- Added instructions on how to configure branch protections
- Added instructions for opting-in to required 2FA on PyPI
- Added the OpenSSF Scorecard GitHub Action

### Changed

- Changed default permissions to `read-all` for GitHub Actions
