
import os
import yaml
import click
from engine.pipeline import pipeline
from engine.errors import excecution_error

def rur_pipe(tags, env):
    pipe = pipeline(env = env, tags = tags)
    pipe.start_pipeline()

def create_framework(project_path):
    actual_path = os.getcwd()
    try:
        os.chdir(project_path)
    except:
        os.mkdir(project_path)
    finally:
        os.chdir(project_path)

    # Create pieline folder and basic confs
    os.mkdir("pipeline")
    os.mkdir("pipeline/extract")
    os.mkdir("pipeline/transform")
    os.mkdir("pipeline/load")
    basic_confs = {
        "flows" : {
            "my-flow" : {
                "tags" : ["deafult"],
                "steps" : {
                    "extract" : ["extract_data"],
                    "transform" : ["transform_data"],
                    "load" : ["load_data"]
                }
            }
        },
        "confs" : {
            "envs" : {
                "dev" : "dev confs",
                "prod" : "prod confs",
            }
        }
    }
    with open("pipeline/pipeline_conf.yml", "w") as file:
        yaml.dump(basic_confs, file, default_flow_style = False)

    # Create extra folders
    os.mkdir("logs")
    os.mkdir("temp")

    os.chdir(actual_path)
    print("Normandy folder structure created")


@click.command()
@click.option("--create-project", "create_project", is_flag = True, help = "Used to create a Normandy project structure in the specify directory.")
@click.option("-project-path", "project_path", default = None, help = "Path where to start Normandy project.")
@click.option("--run-pipeline", "run_pipeline", is_flag = True, help = "Execute the pipeline.")
@click.option("-tags", default = ["default"], help = "Flows with this tag will run.", show_default = True, multiple=True)
@click.option("-env", default = "dev", help = "Enviroment to run.", show_default=True)
def run(create_project, project_path, run_pipeline, tags, env):
    if create_project and run_pipeline:
        raise excecution_error("Cannot use create-project and run-pipeline at the same time")
    if run_pipeline:
        rur_pipe(tags, env)
    elif create_project:
        if project_path is None:
            raise excecution_error("Project path must be specify")
        create_framework(project_path)
    else:
        raise excecution_error("No option selected")
