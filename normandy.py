
import os
import yaml
import click
from engine.pipeline import pipeline

@click.command()
@click.option("-tags", default = ["default"], help = "Flows with this tag will run", show_default = True, multiple=True)
@click.option("-env", default = "dev", help = "Enviroment to run", show_default=True)
def run(tags, env):
    pipe = pipeline(env = env, tags = tags)
    pipe.start_pipeline()

@click.command()
@click.option("-project_path", required = True, help = "Path where to start Normandy project")
def start_project(project_path):

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
