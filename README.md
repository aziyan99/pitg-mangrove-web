# pitg-mangrove-web

An website for pitg mangrove

## Run

Init DB first

```
$ flask --app admin init-db
```

Then run

```
$ flask --app admin run --debug
```

You can use the following command to output a random secret key:

```
$ python -c 'import secrets; print(secrets.token_hex())'

'192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
```

## Build

```
$ python -m build --wheel
```

Copy this file to another machine, set up a new virtualenv, then install the file with pip.

```
$ pip install admin-1.0.0-py2.py3-none-any.whl
```

## Test

```
$ pytest

$ coverage run -m pytest

$ coverage report

$ coverage html
```
