# Changelog
<!-- scriv-insert-here -->

<a id='changelog-0.6.0'></a>
## 0.6.0 (2023-01-10)

### Added

- Added the `repo_token` parameter to the `ossf/scorecard-action` GitHub Action.

- Added documentation on how to upgrade dependencies in lock files manually with `pip-compile` and the `--upgrade-package` option.

### Changed

- Changed Dependabot configuration to reduce the total number of opened pull requests without sacrificing timely security fixes or upgrades signalling a new major version.

- Changed the build job to forward `PYPI_TOKEN` to the publish job
  via `GITHUB_OUTPUT` to avoid needing to approve multiple environment
  runs in one release.

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
