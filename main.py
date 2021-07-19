
import click
from tools.engine import pipeline

@click.command()
@click.option("-tags", default = ["default"], help = "Flows with this tag will run", show_default = True, multiple=True)
@click.option("-env", default = "dev", help = "Enviroment to run", show_default=True)
def main(tags, env):
    pipe = pipeline(env = env, tags = tags)
    pipe.start_pipeline()

if __name__ == "__main__":
    main()
