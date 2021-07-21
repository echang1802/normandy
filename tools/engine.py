
import sys
import yaml
from datetime import datetime
from yaml.loader import SafeLoader
from importlib import import_module
from multiprocessing import Pool
from tools.engine_errors import step_error

def _info(title, _t):
    print(title , 'start at:', _t, 'process time:', datetime.now() - _t)

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

class flow:

    def __init__(self, flow_data, name):
        self.__steps__ = flow_data["steps"]
        self.__tags__ = flow_data["tags"]
        self.__name__ = name

    def steps(self):
        return self.__steps__.items()

    def __str__(self):
        return f"Flow: {self.__name__}"

class pipeline:

    def __init__(self, env, tags):
        tags = set(tags)
        with open("pipeline/pipelines_conf.yml") as file:
            confs = yaml.load(file, Loader=SafeLoader)
            self.flows = [flow(data, flow_name) for flow_name, data in confs["flows"].items() if tags.intersection(set(data["tags"]))]
            self.confs = confs["confs"]
            self.confs["active_env"] = env
        self.variables = variables_storage()

    def __take_step__(self, step_name, step):
        for process_name, process in step.items():
            # The process must be execute?
            if "avoid_tags" in process.keys() and self.tags.intersection(set(process["avoid_tags"])):
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

    def __flow_runner__(self, flow):
        _t = datetime.now()
        for step_name, step in flow.steps():
            self.__take_step__(step_name, step)
        _info(flow, _t)

    def start_pipeline(self):
        with Pool(len(self.flows)) as pool:
            pool.map(self.__flow_runner__, self.flows)
