# down_ballot_climate
Repository for work with the Down Ballot Climate Project

# Usage
## Docker
The Down Ballot Climate Project uses [Docker](https://www.docker.com/) for development and deployment. To start working with DBCP, [install docker](https://docs.docker.com/get-docker/) and refer to the following make commands:

```
make build
```
to build the dbcp docker imagess.

```
make run_etl
```
to run the etl.

```
make sql_shell
```
starts a PostgreSQL interactive terminal.

```
make shell
```
starts a bash interactive terminal.

```
make run_etl_bq
```
runs the etl and loads the data to our BigQuery instance.

```
make jupyter_lab
```
starts a jupyter lab instance at http://127.0.0.1:8888/. If you have another jupyter service running at 8888 you can change the port by setting an environment variable in your shell:

```
export JUPYTER_PORT=8890
```

## Conda
There are some packages that are helpful for local development that aren't necessary in the docker image like pre-commit. To manage these packages, create a conda environment using this command:

```
conda env create -f environment.yml
```
