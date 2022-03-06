# Learning Space Creation for Single User

## Usage

This is an action to convert a yaml template for a learning space into a fully-fledged repo, complete with issues board for each of the learning materials in the space. This particular setup is intended for only a single user, and doesn't need any access to organizations, so the default `GITHUB_TOKEN` available within the action is sufficient to set up everything.

Run this action and supply a path to a local configuration file to create the project board from a given learning space template.

### Example workflow

```yaml
name: My Learning Space

# this lets you run it manually after the template is used to generate a new repo
on: workflow_dispatch

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master

    - name: Run action
      uses: lpmi-13/learning-space-single-setup@v1.0.0
      env:
        # this is the default token available during actions, so
        # you don't need to create one yourself
        TOKEN: ${{ secrets.GITHUB_TOKEN }}
        REPOSITORY: ${{ github.repository }}
      with:
        # reference the local configuration file
        path: ./learning/materials.yml
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `path`  | the path to the local file |

## Examples

### Referring to a local file

The local file can be anywhere in the project folder structure, but a good place to put it might be in a hidden directory to avoid namespace clashes...but you can put it anywhere you want.

```yaml
with:
  path: ./learning/materials.yml
```
