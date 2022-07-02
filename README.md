# Secure Python package template

Template for a Python package with a secure
project host and package repository configuration.

## Configuring your package repository

- Upload a dummy v0.0 package under the desired package name using your PyPI username and password.
- Create an API token that is scoped to only the package
- Copy the value into your clipboard, it will be used later.

## Configuring your project host

### Protected branches

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

## License

CC0-1.0
