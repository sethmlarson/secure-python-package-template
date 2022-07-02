# Secure Python package template

Template for a Python package with a secure
project host and package repository configuration.

The goals of this project are to:

- Show how to configure a package with automated deployments securely
- Obtain a perfect rating from OpenSSF Scorecard
- Integrate with sigstore for signed releases

## Configuring PyPI

### Obtain an API token

- Upload a dummy v0.0 package under the desired package name using your PyPI username and password.
- Create an API token that is scoped to only the package
- Copy the value into your clipboard, it will be used later.

## Configuring the GitHub repository

### Dependabot

- Settings > Code security and analysis
- Dependency graph should be enabled. This is the default for public repos.
- Enable Dependabot security updates

### CodeQL and vulnerable code scanning

- Settings > Code security and analysis
- Select "Set up"

### Protected branches

- Settings > Branches
- Select the "Add rule" button
- Branch name pattern should be your default branch, usually `main`
- Enable "Require a pull request before merging"
  - Enable "Require approvals". To get a perfect score from OpenSSF scorecard metric "[Branch Protection](https://github.com/ossf/scorecard/blob/main/docs/checks.md#branch-protection)" you must set the number of required reviewers to 2 or more.
  - Enable "Dismiss stale pull request approvals when new commits are pushed"
  - Enable "Require review from Code Owners"
- Enable "Require status checks to pass before merging"
  - Enable "Require branches to be up to date before merging". **Warning: This will increase the difficulty to receive contributions from new contributors.**
- Enable "Require signed commits". **Warning: This will increase the difficulty to receive contributions from new contributors.**
- Enable "Require linear history"
- Enable "Include administrators". This setting is more a reminder and doesn't prevent administrators from temporarily disabling this setting in order to merge a stuck PR in a pinch.
- Ensure that "Allow force pushes" is disabled.
- Ensure that "Allow deletions" is disabled.
- Select the "Create" button.

### Protected tags

- Settings > Tags > New rule
- Use a pattern of `*`, even if you have a pattern like `vX.Y.Z`.
- Select "Add rule"

### Publish GitHub Environment

- Settings > Environments > New Environment
- Name the environment: `publish`
- Add required reviewers, should be maintainers
- Select "Save protection rules" button
- Select "Protected Branches" in the deployment branches dropdown
- Select "Add secret" in the environment secrets section
- Add the PyPI API token value under `PYPI_TOKEN`

## Verifying configurations

### Verifying reproducible builds

- Find the latest release that was done via the publish GitHub Environment. ([v0.1.0](https://github.com/sethmlarson/python-package-template/runs/7163956796?check_suite_focus=true))
- Pull up the [release page on PyPI](https://pypi.org/project/secure-package-template/0.1.0).
- Select the "[Download files](https://pypi.org/project/secure-package-template/0.1.0/#files)" tab.
- For each `.whl` file select "view hashes" and copy the SHA256 and save the value somewhere (`de58d65d34fe9548b14b82976b033b50e55840324053b5501073cb98155fc8af`)
- Clone the GitHub repository locally. Don't use an existing clone of the repository to avoid tainting the workspace (`$ git clone ssh://git@github.com/sethmlarson/secure-python-package-template`)
- Check out the corresponding git tag (`$ git checkout v0.1.0`)
- Run `$ git log -1 --pretty=%ct` and store this value (`1656789393`)
- Export the stored value into `SOURCE_DATE_EPOCH` (`$ export SOURCE_DATE_EPOCH=1656789393`)
- Install the dependencies for publishing (`$ python -m pip install -r requirements/publish.txt`)
- Run `$ python -m build`
- Run `sha256sum dist/*.whl`
- Compare SHA256 hashes with the values on PyPI. They should match for each `.whl` file.

## License

CC0-1.0
