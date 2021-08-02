# Normandy

v0.2
by [Epsilon DataLabs](https://echang1802.github.io/epsilon.github.io)

----------------------------------------------------------------

Normandy is a data treatment framework, which main objective is standardizing your team code and provide a data treatment methodology flexible to your team needs.

----------------------------------------------------------------

## Implementing Normandy

We are currently working in make Normandy a fully installable package, meanwhile, you may implement Normandy _forking_ this repository and changing the _steps_ and _pipeline_ configuration files.

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

----------------------------------------------------------------

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

A configured flow, should looks like:

```
my_flow:
  tags:
    - default
    - main_flow
    - my_flow
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

Note that if you want to use one of the special setups on one process of a step, you must specify all others process as a dictionary too, even if in one of the processes no special setup is used, on this case the setup `ignore` is used.

A complete example:

```
my_flow:
  tags:
    - default
  steps:
    read:
      - read_file
      - read_database
    process:
      main_processing:
        avoid_tags:
          - weekend
      side_processing:
        avoid_tags:
          - Shepard
        error_tolerance: True
    finish:
      write_data:
        - ignore
      backup_writing:
        error_tolerance: True
```

### Environment Configuration

You are free to make all configurations you need over the environment section of the configuration file, just must use the keyword "envs", by example  if you want to specify a reading and writing path of each environments do as follow:

```
confs:
  envs:
    dev:
      read:
        raw_dev
      write:
        processed_dev
    prod:
      read:
        raw
      write:
        processed
```

### Writing a process

AS mentioned before, each process listed on the `pipeline_conf.yml` file is making a reference to a python file inside the correspondent step folder, whatever, this file must have defined inside it a process function which need to parameter `pipe` and `log`.

Pipe is a Normandy pipeline object,  at the stage is only function is to use the environment configurations defined on `pipeline_conf.yml` , to get this use the `get_env_confs()` method, which returns a dictionary with the mentioned configurations.

log is a Normandy logger object, the main function is to easily log your code.

Process snippet:

```
from engine.variables_storage import variables_storage

def process(pipe, log):
    # Configurations
    env_confs = pipe.get_confs()["read"]
    var_str = variables_storage()
    log.info("Configuration ready")

    # Code here your process
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
from engine.variables_storage import variables_storage

def process(pipe, log):
    # Get confs
    read_path = pipe.get_env_confs()["read"]
    var_str = variables_storage()
    log.info("Configuration ready")

    main_df = pd.read_csv(f"{read_path}/sample_data.csv")
    log.info("Data read")

    var_str.update("main_df", main_df)
    log.info("Data stored")

    return
```

### How to run it

The Normandy CLI interface is still under construction, but you may run your pipeline with the command:

 ```
python main.py
 ```

With this command the default flow would run on the defined dev environment.

To specify tags you may use the tag parameter as follow:

 ```
python main.py -tags default -tags weekend
 ```

 Finally to specify the environment use the parameter env:

 ```
python main.py -env prod
 ```
