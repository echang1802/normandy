
import sys
import yaml
from yaml.loader import SafeLoader
from importlib import import_module
from tools.engine_errors import step_error

class variables_storage:

    def __init__(self):
        self.variables = {}

    def store_vars(self, variables):
        for name, var in variables.items():
            self._store(name, var)

    def _store(self, name, var):
        self.variables[name] = var

    def get(self, variables):
        return [self.variables[var] for var in variables]

class pipeline:

    def __init__(self, env):
        with open("pipeline/pipelines_conf.yml") as file:
            confs = yaml.load(file, Loader=SafeLoader)
            self.flows = confs["flows"]
            self.confs = confs["confs"]
            self.confs["active_env"] = env
        self.variables = variables_storage()

    def _make_step(self, step_name, step, tags):
        for process_name, process in step.items():
            # The process must be execute?
            if "avoid_tags" in process.keys() and tags.intersection(set(process["avoid_tags"])):
                continue

            # Step Confs
            if "in_variables" in process.keys():
                variables = self.variables.get(process["in_variables"])
            else:
                variables = None
            error_tolerance = "error_tolerance" in process.keys() and process["error_tolerance"]

            # Process step
            func = import_module(f"pipeline.{step_name}.{process_name}")
            try:
                exit_vars = func.process(confs = self.confs, args = variables)
            except Exception as e:
                if not error_tolerance:
                    raise step_error("Step exception without errors tolerance")
                print(e)
            if "out_variables" in process.keys():
                variables = {process["out_variables"][x] : exit_vars[x] for x in range(len(process["out_variables"]))}
                self.variables.store_vars(variables)

    def run_tag(self, tags):
        tags = set(tags)
        for _,flow in self.flows.items():
            if not tags.intersection(set(flow["tags"])):
                continue
            for step_name, step in flow["steps"].items():
                self._make_step(step_name, step, tags)
