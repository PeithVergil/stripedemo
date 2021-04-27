Stripe Demo
===========


Installation
------------

Create a new virtual environment and activate it.

```bash
python -m venv /path/to/envs/stripedemo && source /path/to/envs/stripedemo/bin/activate
```

Go to the project root directory and install the dependencies.

```bash
cd /path/to/stripedemo && pip install -r requirements.txt
```

Run the server.

```bash
python -m stripedemo
```

Running tests.

```bash
python -m tornado.testing tests/*.py
```