
import argparse
from tools.engine import pipeline

arg_parser = argparse.ArgumentParser(description = "Data Science pipeline")
arg_parser.add_argument("-tags", default = ["default"], help = "Flows with this tag will run", nargs="+")
arg_parser.add_argument("-env", default = "dev", help = "Enviroment to run")

if __name__ == "__main__":

    argv = arg_parser.parse_args()

    pipe = pipeline(env = argv.env)

    pipe.run_tag(argv.tags)
