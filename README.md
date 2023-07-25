# Summary

This application implements and visualises several path finding algorithms on a
fixed set of nodes, with start and target nodes specified by the user.

# Quickstart

1. Clone this repository and change into it,
2. (create a new virtual environment for dependencies and activate it,)
3. install dependencies,
3. run the script.

```
git clone ... path-finding-app
cd path-finding-app

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python path-finding-app.py
```

Depending on the system the above might need to use `pip3` and `python3`
instead.

# Contributing

Code should be formatted according to PEP8, e.g. `black` is a good
choice for auto-formatting:

```
pip install black
black -l 120 .
```

Running a linter like `pyflakes` would also be a good idea:

```
pip install pyflakes
pyflakes path-finding-app.py
```
