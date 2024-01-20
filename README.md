# DEALER IMITATOR

## Work Flow

Before making any changes to the project, run the following code to make sure that on making a commit the code will satisfy the acceptance criteria of .pre-commit-config.yaml hook file.

```bash
$ pip install pre-commit
```

and then

```bash
$ pre-commit install
```

If changes are made after triggering pre-commit hook while making a commit - stage the changed files and commit again and you will be able to push the changes to the repo afterwards.
