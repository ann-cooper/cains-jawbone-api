# Cain's Jawbone API
An API to track research about the Cain's Jawbone puzzle book.
## Dependency management pip-tools

### First steps
Make sure that you have created a virtual environment locally and it is activated. Then manually install pip-tools with `pip install pip-tools`

### How to specify which packages to use
Put these in the `.in` files. You can also pin the versions in the `.in` file if you need to, but the compiled output `.txt` will serve as the primary way to track and pin the dependencies.

### How to generate the .txt requirements file
`pip-compile requirements.in --output-file=- > requirements.txt`

### How to use the requirements file
- Install the `.txt` file:
`pip install -r requirements.txt`
- Note that the pip-tools docs recommend using `pip-sync` to install the dependencies in your virtualenv, that functionality can be flaky, so it's easier to just use pip as shown above.

## Virtual Environments

### Pyenv
- [How to get started](https://github.com/pyenv/pyenv)
- [A guide on setting it up and using it (if you need more help!)](https://realpython.com/intro-to-pyenv/)
- Make sure that you use pyenv to install Python 3.10.4 if you don't already have it.
- Set up and activate your pyenv:
```
pyenv virtualenv 3.10.4 my-env
pyenv activate my-env
```

### Install the requirements
- [Install the dependencies](#How-to-use-the-requirements-file)
- Install this package: `pip install -e .`

## DB set-up
- Locally export the DB_PATH for the sqlite file: `export DB_PATH=my_file.db`