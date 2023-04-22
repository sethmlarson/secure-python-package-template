# Secure Python package template

[![SLSA level 3](https://slsa.dev/images/gh-badge-level3.svg)](https://slsa.dev)
[![OpenSSF Scorecards](https://api.securityscorecards.dev/projects/github.com/sethmlarson/secure-python-package-template/badge)](https://deps.dev/pypi/secure-package-template)

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

## Configuring git for commit and tag signing

> **Info**
> Commit and tag signing is a practice that's recommended to avoid commit author spoofing
> but isn't strictly required for a secure project configuration.
> If you'd like to skip this step, you can jump ahead to [creating a GitHub repository](https://github.com/sethmlarson/secure-python-package-template/#creating-the-github-repository).

Git needs to be configured to be able to sign commits and tags. Git uses GPG for signing, so you need to
[create a GPG key](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key)
if you don't have one already. Make sure you use a [email address associated with your GitHub account](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address)
as the email address for the key. If you wish to keep your email address private you should use GitHub's provided `noreply` email address.

```sh
gpg --full-generate-key
```

After you've generated a GPG key you need to [add the GPG key to your GitHub account](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account).
Then locally you can [configure git to use your signing key](https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key):

```sh
git config --global --unset gpg.format
```

List GPG secret keys, in this example the key ID is '3AA5C34371567BD2'

```sh
$ gpg --list-secret-keys --keyid-format=long
/Users/hubot/.gnupg/secring.gpg
------------------------------------
sec   4096R/3AA5C34371567BD2 2016-03-10 [expires: 2017-03-10]
uid                          Hubot <hubot@example.com>
ssb   4096R/4BB6D45482678BE3 2016-03-10
```

Tell git about your signing key:

```sh
git config --global user.signingkey 3AA5C34371567BD2
````

Then tell git to auto-sign commits and tags:

```sh
git config --global commit.gpgsign true
git config --global tag.gpgSign true
```

Now all commits and tags you create from this git instances will be signed and show up as "verified" on GitHub.

## Creating the GitHub repository

Clone this repository locally:

```sh
git clone ssh://git@github.com/sethmlarson/secure-python-package-template
```

Rename the folder to the name of the package and remove existing git repository:

```sh
mv secure-python-package-template package-name
cd package-name
rm -rf .git
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
git branch -m master main
```

Create an **empty** repository on GitHub. To ensure the repository is empty you shouldn't add a README file, .gitignore file, or a license yet. For the examples below the GitHub repository will be named `sethmlarson/package-name` but you should substitute that with the GitHub repository name you chose.

We need to tell our git repository about our new GitHub repository:

```sh
git remote add origin ssh://git@github.com/sethmlarson/package-name
```

Change all the names and URLs be for your own package. Places to update include:

- `README.md`
- `pyproject.toml` (`project.name` and `project.urls.Home`)
- `src/{{secure_package_template}}`
- `tests/test_{{secure_package_template}}.py`

You should also change the license to the one you want to use for the package. Update the value in here:

- `LICENSE`
- `README.md`

Now we can create our initial commit:

```sh
git add .

git commit -m "Initial commit"
```

Verify that this commit is signed. If not you should configure git to auto-sign commits:

```sh
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

## Configuring the GitHub repository

### Dependabot

[Dependabot](https://docs.github.com/en/code-security/dependabot) is a service provided by GitHub that keeps your dependencies up-to-date automatically by creating
pull requests updating individually dependencies on your behalf. Unfortunately, when using Dependabot with any non-trivial number
of dependencies the number of pull requests quickly becomes too much to handle, especially
when you think about a single maintainer needing to manage multiple
projects worth of dependency updates.

The approach taken with Dependabot in this repository is to keep the number of pull requests from
Dependabot to a minimum while still maintaining a secure and maintained set of
dependencies for developing and publishing packages. The policy is described below:

- Always create pull requests upgrading dependencies if the pinned version has a public vulnerability.
  **This is the default behavior of Dependabot and can't be disabled.**
- Create pull requests when new major versions of development dependencies are made available.
  This is important because usually major versions contain backwards-incompatible changes so
  may actually require changes on our part.
- Create pull requests when there's a new version of a dependency that carries security sensitive data like
  `certifi`. It's always important to have this package be up-to-date to avoid monster-in-the-middle (MITM) attacks.
- All other upgrades to dependencies need to be done manually. These are cases like bug fixes that
  are impacting the project or new features. The developer experience here is the same
  as if Dependabot wasn't automatically upgrading dependencies.

You can [read the `dependabot.yml` configuration file](https://github.com/sethmlarson/secure-python-package-template/blob/main/.github/dependabot.yml) to learn how to
encode the above policy or [read the Dependabot documentation](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file) on the configuration format.

#### Enabling Dependabot

- Settings > Code security and analysis
- Dependency graph should be enabled. This is the default for public repos.
- Enable Dependabot security updates

#### Upgrading dependencies manually

Any upgrades to development dependencies to fix bugs or use new features
will require a manual upgrade instead of relying on Dependabot to keep things up to date
automatically. This can be done by running the following to upgrade only one package:

```shell
# We want to only upgrade the 'keyring' package
# so we use the --upgrade-package option.
pip-compile \
  requirements/publish.in \
  -o requirements/publish.txt \
  --no-header \
  --no-annotate \
  --generate-hashes \
  --upgrade-package=keyring
```

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

### Private vulnerability reporting

- Settings > Code security and analysis
- Select "Enable" for "Private vulnerability reporting". This will allow
  users to privately submit vulnerability reports directly to the repository.
- Update the URL in the `SECURITY.md` file to the URL of your own repository.

## Configuring PyPI

PyPI is increasing the minimum requirements for account security and credential management to make consuming packages on PyPI more secure. This includes [eventually requiring 2FA for all users and requiring API tokens to publish packages](https://pyfound.blogspot.com/2020/01/start-using-2fa-and-api-tokens-on-pypi.html). Instead of waiting for these best practices to become required we can opt-in to them now.

### Opt-in to required 2FA

If you don't have 2FA enabled on PyPI already there's a section in the [PyPI Help page](https://pypi.org/help) about how to enable 2FA for your account. To make 2FA required for the new project:

- Open "Your projects" on PyPI
- Select "Manage" for the project
- Settings > Enable 2FA requirement for project

### Configuring a Trusted Publisher

If your project is hosted on GitHub you can take advantage of a new PyPI feature called "[Trusted Publishers](https://docs.pypi.org/trusted-publishers/)".
It's recommended to use a Trusted Publisher over an API key or password because it provides an additional layer of security
by requiring the package to originate from a pre-configured GitHub repository, workflow, and environment.

There's a [short guide on how to add a Trusted Publisher to the project](https://docs.pypi.org/trusted-publishers/adding-a-publisher/).
Below is an example of how to map the publishing GitHub Workflow definition to the PyPI Trusted Publisher.

> **Warning**
> Care should be taken that the publishing workflow can only be triggered
> by the GitHub accounts that you intend. Remember that git tags (without Protected Tags enabled)
> only require write access to the repository. This is why GitHub Environments with
> a set of required reviewers is highly recommended to have an explicit list of
> people who are allowed to completely execute the publish job.

Configuring the Trusted Publisher requires 4 values:

- GitHub repository owner
- GitHub repository name
- GitHub workflow filename
- GitHub environment name (optional, but highly recommended!)

Using this repository ([https://github.com/sethmlarson/secure-python-package-template](https://github.com/sethmlarson/secure-python-package-template)) as an example, the values to set up a Trusted Publisher would be:

- GitHub repository owner: `sethmlarson`
- GitHub repository name: `secure-python-package-template`
- GitHub workflow filename: `publish.yml`
- GitHub environment name: `publish`

Below is the minimum configurations required from the GitHub Workflow:

```yaml
# Filename: '.github/workflows/publish.yml'
# Note that the 'publish.yml' filename doesn't need the '.github/workflows' prefix.
jobs:
  publish:
    # ...
    permissions:
      # This permission allows for the gh-action-pypi-publish
      # step to access GitHub OpenID Connect tokens.
      id-token: write

    # This job requires the 'publish' GitHub Environment to run.
    # This value is also set in the Trusted Publisher.
    environment:
      name: "publish"

    steps:
    # - ...
    # The 'pypa/gh-action-pypi-publish' action reads OpenID Connect
    # Note that there's zero config below, it's all magically handled!
    - uses: "pypa/gh-action-pypi-publish@0bf742be3ebe032c25dd15117957dc15d0cfc38d"
```

## Verifying configurations

### Verifying reproducible builds

Find the latest release that was done via the publish GitHub Environment, I used [v0.1.0](https://github.com/sethmlarson/python-package-template/runs/7163956796?check_suite_focus=true)
for this example.

Open the [corresponding release page on PyPI](https://pypi.org/project/secure-package-template/0.1.0).
Select the "[Download files](https://pypi.org/project/secure-package-template/0.1.0/#files)" tab.
For each `.whl` file select "view hashes" and copy the SHA256 and save the value somewhere (`de58d65d34fe9548b14b82976b033b50e55840324053b5501073cb98155fc8af`)

Clone the GitHub repository locally. Don't use an existing clone of the repository to avoid tainting the workspace:

```sh
git clone ssh://git@github.com/sethmlarson/secure-python-package-template
```

Check out the corresponding git tag.

```sh
git checkout v0.1.0
```

Run below command and export the stored value into `SOURCE_DATE_EPOCH`:

```sh
$ git log -1 --pretty=%ct
1656789393

$ export SOURCE_DATE_EPOCH=1656789393
```

Install the dependencies for publishing and build the package:

```sh
python -m pip install -r requirements/publish.txt
python -m build
```

Compare SHA256 hashes with the values on PyPI, they should match the SHA256 values that we saw on PyPI earlier.

```sh
$ sha256sum dist/*.whl
de58d65d34fe9548b14b82976b033b50e55840324053b5501073cb98155fc8af
```

## License

CC0-1.0
