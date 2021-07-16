
import yaml
from yaml.loader import SafeLoader
from importlib import import_module

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

    def _make_step(self,step_name, step):
        for process_name, process in step.items():
            if "in_variables" in process.keys():
                variables = self.variables.get(process["in_variables"])
            else:
                variables = None
            func = import_module(f"pipeline.{step_name}.{process_name}")
            exit_vars = func.process(confs = self.confs, args = variables)
            if "out_variables" in process.keys():
                variables = {process["out_variables"][x] : exit_vars[x] for x in range(len(process["out_variables"]))}
                self.variables.store_vars(variables)

    def run_tag(self, tag):
        for _,flow in self.flows.items():
            if not tag in flow["tags"]:
                continue
            for step_name, step in flow["steps"].items():
                self._make_step(step_name, step)
