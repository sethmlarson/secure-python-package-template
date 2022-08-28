# Secure Python package template

[![SLSA level 3](https://slsa.dev/images/gh-badge-level3.svg)](https://slsa.dev)

Template for a Python package with a secure
project host and package repository configuration.

The goals of this project are to:

- Show how to configure a Python package hosted on GitHub with:
  - Operational security best-practices
  - Automated publishing to PyPI
  - Code quality and vulnerability scanning
  - Build reproducibility
  - Releases with provenance attestation
- Obtain a perfect rating from [OpenSSF Scorecard](https://github.com/ossf/scorecard)
- [SLSA Level 3](https://slsa.dev) using GitHub OIDC

## Creating the GitHub repository

Clone this repository locally:

```sh
$ git clone ssh://git@github.com/sethmlarson/secure-python-package-template

Cloning into 'secure-python-package-template'...
...
Receiving objects: 100% (79/79), 29.37 KiB | 1002.00 KiB/s, done.
Resolving deltas: 100% (20/20), done.
```

Rename the folder to the name of the package and remove existing git repository:

```sh
$ mv secure-python-package-template package-name
$ cd package-name
$ rm -rf .git
```

Create a new git repository and ensure the branch name is `main`:

```sh
$ git init
Initialized empty Git repository in .../package-name/.git/

$ git status
On branch main

No commits yet
...
```

If the branch isn't named `main` you can rename the branch:

```sh
$ git branch -m master main
```

Create an **empty** repository on GitHub. To ensure the repository is empty you shouldn't add a README file, .gitignore file, or a license yet. For the examples below the GitHub repository will be named `sethmlarson/package-name` but you should substitute that with the GitHub repository name you chose.

We need to tell our git repository about our new GitHub repository:

```sh
$ git remote add origin ssh://git@github.com/sethmlarson/package-name
```

Change all the names and URLs be for your own package. Places to update include:

- `README.md`
- `pyproject.toml` (`project.name` and `project.urls.Home`)
- `src/{{secure_package_template}}`
- `tests/test_{{secure_package_template}}.py`

You should also change the license to the one you want to use for the package. Update the value in here:

- `LICENSE`
- `README.md`

Now we can create our initial commit and ensure it is signed by default:

```sh
$ git add .

$ git commit -m "Initial commit"

# Verify that this commit is signed. If not you
# should configure git to auto-sign commits.
$ git verify-commit HEAD
gpg: Signature made Fri 15 Jul 2022 10:55:10 AM CDT
gpg:                using RSA key 9B2E1343B0B201B8883C79E3A99A0A21AD478212
gpg: Good signature from "Seth Michael Larson <sethmichaellarson@gmail.com>" [ultimate]
```

Now we push our commit and branch:

```sh
$ git push origin main

Enumerating objects: 25, done.
Counting objects: 100% (25/25), done.
Delta compression using up to 12 threads
Compressing objects: 100% (21/21), done.
Writing objects: 100% (25/25), 17.92 KiB | 1.28 MiB/s, done.
Total 25 (delta 0), reused 0 (delta 0), pack-reused 0
To ssh://github.com/sethmlarson/package-name
 * [new branch]      main -> main
```

Success! You should now see the commit and all files on your GitHub repository.

## Configuring PyPI

PyPI is increasing the minimum requirements for account security and credential management to make consuming packages on PyPI more secure. This includes [eventually requiring 2FA for all users and requiring API tokens to publish packages](https://pyfound.blogspot.com/2020/01/start-using-2fa-and-api-tokens-on-pypi.html). Instead of waiting for these best practices to become required we can opt-in to them now.

### Obtain an API token

API tokens will eventually be required for all packages to publish to PyPI.

- Upload a dummy v0.0 package under the desired package name using your PyPI username and password.
- Create an API token that is scoped to only the package
- Copy the value into your clipboard, it will be used later (see `PYPI_TOKEN` in the GitHub Environments section below)

### Opt-in to required 2FA

If you don't have 2FA enabled on PyPI already there's a section in the [PyPI Help page](https://pypi.org/help) about how to enable 2FA for your account. To make 2FA required for the new project:

- Open "Your projects" on PyPI
- Select "Manage" for the project
- Settings > Enable 2FA requirement for project

## Configuring the GitHub repository

### Dependabot

- Settings > Code security and analysis
- Dependency graph should be enabled. This is the default for public repos.
- Enable Dependabot security updates

### CodeQL and vulnerable code scanning

- CodeQL is already configured in `.github/workflows/codeql-analysis.yml`
- Configure as desired after reading the [documentation for CodeQL](https://codeql.github.com/docs).

### Protected branches

- Settings > Branches
- Select the "Add rule" button
- Branch name pattern should be your default branch, usually `main`
- Enable "Require a pull request before merging"
  - Enable "Require approvals". To get a perfect score from OpenSSF scorecard metric "[Branch Protection](https://github.com/ossf/scorecard/blob/main/docs/checks.md#branch-protection)" you must set the number of required reviewers to 2 or more.
  - Enable "Dismiss stale pull request approvals when new commits are pushed"
  - Enable "Require review from Code Owners"
- Enable "Require status checks to pass before merging"
  - Add all status checks that should be required. For this template they will be:
    - `Analyze (python)`
    - `Test (3.8)`
    - `Test (3.9)`
    - `Test (3.10)`
  - Ensure the "source" of all status checks makes sense and isn't set to "Any source".
    By default this should be configured properly to "GitHub Actions" for all the above status checks.
  - Enable "Require branches to be up to date before merging". **Warning: This will increase the difficulty to receive contributions from new contributors.**
- Enable "Require signed commits". **Warning: This will increase the difficulty to receive contributions from new contributors.**
- Enable "Require linear history"
- Enable "Include administrators". This setting is more a reminder and doesn't prevent administrators from temporarily disabling this setting in order to merge a stuck PR in a pinch.
- Ensure that "Allow force pushes" is disabled.
- Ensure that "Allow deletions" is disabled.
- Select the "Create" button.

### Protected tags

- Settings > Tags > New rule
- Use a pattern of `*` to protect all tags
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
