
import argparse
from tools.engine import pipeline

arg_parser = argparse.ArgumentParser(description = "Data Science pipeline")
arg_parser.add_argument("-tag", default = "default", help = "Flows with this tag will run")

if __name__ == "__main__":

    argv = arg_parser.parse_args()

    pipe = pipeline()

    pipe.run_tag(argv.tag)
