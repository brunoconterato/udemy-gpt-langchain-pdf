# Instructions --> Do this before the original README.md instructions

## Create a .env file in the root of the project with the following content:

```
SECRET_KEY=123
SQLALCHEMY_DATABASE_URI=sqlite:///sqlite.db
UPLOAD_URL=https://prod-upload-langchain.fly.dev
 
OPENAI_API_KEY=
 
REDIS_URI=
 
PINECONE_API_KEY=
PINECONE_ENV_NAME=
PINECONE_INDEX_NAME=
 
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
```


## (If needed) Install pipenv:

```
$ pip install pipenv
```

# Now follows the original README.md from course instructors:

## Using Pipenv [Recommended]

```
# Install dependencies
pipenv install

# Create a virtual environment
pipenv shell

# Initialize the database
flask --app app.web init-db

```

## Install faiss-gpu (if have nvidia gpu) or faiss-cpu (if not)

[Faiss install](https://github.com/facebookresearch/faiss/blob/main/INSTALL.md)

```
# Choose version

# CPU-only version
$ conda install -c pytorch faiss-cpu=1.8.0

# GPU(+CPU) version
$ conda install -c pytorch -c nvidia faiss-gpu=1.8.0
```

<br>

```

## Using Venv [Optional]

These instructions are included if you wish to use venv to manage your evironment and dependencies instead of Pipenv.

```
# Create the venv virtual environment
python -m venv .venv

# On MacOS, WSL, Linux
source .venv/bin/activate

# On Windows
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database
flask --app app.web init-db
```

# Running the app [Pipenv]

There are three separate processes that need to be running for the app to work: the server, the worker, and Redis.

If you stop any of these processes, you will need to start them back up!

Commands to start each are listed below. If you need to stop them, select the terminal window the process is running in and press Control-C

### To run the Python server

Open a new terminal window and create a new virtual environment:

```
pipenv shell
```

Then:

```
inv dev
```

### To run the worker

Open a new terminal window and create a new virtual environment:

```
pipenv shell
```

Then:

```
inv devworker
```

### To run Redis

```
redis-server
```

### To reset the database

Open a new terminal window and create a new virtual environment:

```
pipenv shell
```

Then:

```
flask --app app.web init-db
```

# Running the app [Venv]

_These instructions are included if you wish to use venv to manage your evironment and dependencies instead of Pipenv._

There are three separate processes that need to be running for the app to work: the server, the worker, and Redis.

If you stop any of these processes, you will need to start them back up!

Commands to start each are listed below. If you need to stop them, select the terminal window the process is running in and press Control-C

### To run the Python server

Open a new terminal window and create a new virtual environment:

```
# On MacOS, WSL, Linux
source .venv/bin/activate

# On Windows
.\.venv\Scripts\activate
```

Then:

```
inv dev
```

### To run the worker

Open a new terminal window and create a new virtual environment:

```
# On MacOS, WSL, Linux
source .venv/bin/activate

# On Windows
.\.venv\Scripts\activate
```

Then:

```
inv devworker
```

### To run Redis

```
redis-server
```

### To reset the database

Open a new terminal window and create a new virtual environment:

```
# On MacOS, WSL, Linux
source .venv/bin/activate

# On Windows
.\.venv\Scripts\activate
```

Then:

```
flask --app app.web init-db
```
