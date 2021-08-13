# Normandy

v0.2.3
by [Epsilon DataLabs](https://echang1802.github.io/epsilon.github.io)

----------------------------------------------------------------

Normandy is a python framework for data pipelines, which main objective is standardizing your team code and provide a data treatment methodology flexible to your team needs.

----------------------------------------------------------------

## Installing Normandy

Normandy is available via PIP using:

```
pip install normandy
```

----------------------------------------------------------------

## Features

With Normandy you can define your data pipeline system and within it several _data flows_ with each one use or produce different kind of data.

First let's explain the basic Normandy terminology:

* **Flow**: Is a complete data process (ETL), you may have any number of _flows_ on a Normandy project and each one may or may not share code or data.

* **Steps**: A Normandy _flow_ is composed by any number of _steps_, this _steps_ are one or more _processes_, the _steps_ works as a guideline of priorities, _processes_ from one _step_ cannot start before the _processes_ of the previous _step_ has ended.

* **Processes**: This are the lower level of granularity in Normandy, each _process_ belong to a _step_, and all _processes_ from one _step_ are processed in parallel, which mean that they can share the input data but you must be cautious that each _process_ have different outputs.

So, Normandy let you:

* Create multiple data flows, and share code between then avoiding repeat code.

* Parallel processing at _process_ level, allowing you, for example, to read from several sources or produce several outputs from the same data set simultaneously.

* A standardized form of coding.

* A clean and understandable data pipeline structure.

* Easily share parameters between processes.

----------------------------------------------------------------

## Creating a Normandy project

Normandy offer a easy files structure, nevertheless, you may create it using the `create project` command with the path where to create the project.

```
normandy --create-project -file-path write/project/path
```

If the given path do not exist Normandy will create it.

This command will also create a template of the `pipeline_conf.yml` file used to configure Normandy behavior.

## How to use Normandy

The Normandy behavior is configured in the `pipeline_conf.yml` file, it has two sections:

* flows: In this section is defined every aspect of each flow you want to use.

* confs: Here are settled general configurations like environments.

### Defining Flows

Each flow has two options that need to be settled, those are tags, and steps.

In the tags sections you must specify with which tags the flow will run, those work to carefully select which flows you want to run in each command.

If several flows have the same tag, all flows with that tag will run when the tag is selected, and they will run in the order they are defined on the `pipeline_conf.yml` file.

At least one flow should have the tag _default_, this flow will run when no tags are selected.

To set the steps is enough to list then with the process they should run.

Here may be defined global parameters as well, this parameters are available at all process.

A configured flow, should looks like:

```
my_flow:
  tags:
    - default
    - sr1
  params:
    version: Andromeda
  steps:
    read:
      - read_file
    process:
      - process_data
    finish:
      - prints
```

### Defining Steps:

A step is a individual process or group of processes from a pipeline, this are used to secure order, each process on a step must end before the processes of the next step start.

A step defined in the `pipeline_conf.yml` is a reference to a sub folder with the same name on the `pipeline` folder, by example, the previously defined flow has three steps: read, process and finish, then the pipeline folder should look like:

- pipeline
  - read
    - read_file.py
  - process
    - process_data.py
  - finish
    - prints.py

Steps have no further configurations excepts the process within it, note that you may have several process (python files) on each step, but if you don´t listed on the step definition it will not run, this allow you to create several flows using the same step, but the step itself in each flow may be different if different processes are called.  

### Defining Processes

The processes are the smaller unit of Normandy pipelines, and here is where your code must be in.

You may define a process on the `pipeline_conf.yml` file on two ways:

* As a list: Use this method if you do not want to add any configuration out of the defaults, you must use the list version even if the step has just one process.

* As a dictionary: With this method you can make more in depth configurations to the specific process, the allowed configurations are:

  * avoid_tags: With this setup you can told Normandy to do not run this process f a specific tags has been use, this is very useful if you have several flows very similar between then then you can define just one flow and use the tags to shape the flow.

  * error_tolerance: If your process may fail and that does not affect the rest of the data flow, you may activate this feature, so, in case the process fail, the flow would still run.

  * params: If your process need some extra parameters you may listed here as a dictionary, then inside the process you can invoke them as `params["params_name"]`. If the same parameter is defined globally and at a process the last one would be chosen.

  * iter_param: this help you if you need to run a process several time but with a different value of a parameters, you must past the name and values to take. Note: this would run as several different processes of the same steps, this mean they will run in parallel.

Note that if you want to use one of the special setups on one process of a step, you must specify all others process as a dictionary too, even if in one of the processes no special setup is used, on this case the setup `ignore` is used.

A complete example:

```
my_flow:
  tags:
    - default
    - salarians
  params:
    version: Andromeda
  steps:
    read:
      - read_file
      - read_database
    process:
      main_processing:
        avoid_tags:
          - hammerhead
        params:
          limit: 100
          flag: True
          version: Trilogy
      side_processing:
        avoid_tags:
          - Shepard
        error_tolerance: True
        iter_param:
          name: locations
          values:
            - Thessia
            - SurKesh
            - Rannoch
            - Tuchanka
            - Palaven
    finish:
      write_data:
        - ignore
      backup_writing:
        error_tolerance: True
```

### Pipeline Configuration

The main objective of this section is to configure your pipeline settings, like environment distinctions.

You are free to make all configurations you need over the environment section of the configuration file, just must use the keyword "envs", in the example below the read and write folder are distinguished based on the environment.

Other settings are:

* path: This is the project path, and must be defined.

* threads: Maximum number of threads allowed to run simultaneously, this is used in case a step have several processes, the default value is 8.  

* log_level: Level of detail in log files, may be info, warnings or erros, the default value is info.

```
confs:
  path: your/project/path
  threads: 4
  log_level: errors
  envs:
    dev:
      read:
        data/dev/raw/
      write:
        data/dev/processed/
    prod:
      read:
        data/prod/raw/
      write:
        data/prod/processed
```

### Writing a process

As mentioned before, each process listed on the `pipeline_conf.yml` file is making a reference to a python file inside the correspondent step folder, whatever, this file must have defined inside it a process function which need to parameter `pipe` and `log`.

Pipe is a Normandy pipeline object,  at the stage is only function is to use the environment configurations defined on `pipeline_conf.yml` , to get this use the `get_env_confs()` method, which returns a dictionary with the mentioned configurations.

log is a Normandy logger object, the main function is to easily log your code.

Process snippet:

```
from normandy.engine.variables_storage import variables_storage

def process(pipe, log, params):
    # Configurations
    env_confs = pipe.get_confs()
    var_str = variables_storage()
    log.info("Configuration ready")

    # Code here your process
    # Use params as any dict ej:
    # flag = params["flag"]
    # ...

    return
```

#### The Normandy logger

Normandy provide a fully settled logger.

Each flow execution will have a separated log folder inside the log folder of the project root directory, the folder would be called as `{flow_name}_{execution_datetime}`, inside it a bunch of file would be created, one file for each Normandy object, with the intention to let you easily get in depth logs or just a general one. The main flow log would have the logs of each of the children's objects, this means, in the main log would be the flow logs, the steps logs and even the processes logs.

The Normandy logger have three basic methods to use:

* info

* warning

* error

Each one just receive one parameter which is the message you want to log.

#### The Normandy Variable Storage

Normandy also provide a variable storage object to let you share the data between processes.

It's very easily to use, with just two methods:

* get: It let you use a previously stored variable

* update: It let you store a new variable or overwrite it if it already exists.

A usage example:

```
import pandas as pd
from normandy.engine.variables_storage import variables_storage

def process(pipe, log, params):
    # Get confs
    read_path = pipe.get_env_confs()
    var_str = variables_storage()
    log.info("Configuration ready")

    try:
      main_df = pd.read_csv(f"{read_path}{params["filename"]}.csv")
    except Exception as e:
      log.error(e)
      raise e
    log.info("Data read")

    var_str.update("main_df", main_df)
    log.info("Data stored")

    return
```

### How to run it

To run the Normandy pipeline use the command `run-pipeline` as below from the project directory:

```
normandy --run-pipeline
```

With this command the _default_ flow would run on the defined _dev_ environment.

The `run-pipeline` has several arguments as:

* tags: Specify any number of tags.

* env: Specify the environment to run on.

* params: Used to overwrite or define global parameters on all running flows.

* log level: Overwrite the log_level setting.

* threads: Overwrite the maximum number of threads setting.

A complete example:

 ```
normandy --run-pipeline -tags my_tag -tags sr2 -env prod -param version Trilogy -log-level warnings -threads 16
 ```
