
import sys
import yaml
import pickle
from datetime import datetime
from yaml.loader import SafeLoader
from importlib import import_module
from multiprocessing import Pool
from tools.engine_errors import step_error

def _info(title, _t):
    print(title , 'start at:', _t, 'process time:', datetime.now() - _t)

class variables_storage:

    def update(self, name, var):
        with open(f"temp/{name}", "wb") as file:
            pickle.dump(var, file)

    def get(self, name):
        with open(f"temp/{name}", "rb") as file:
            return pickle.load(file)

class pipeline:
    def __init__(self, env, tags):
        self.tags = set(tags)
        with open("pipeline/pipelines_conf.yml") as file:
            confs = yaml.load(file, Loader=SafeLoader)
            self.__flows__ = [self.flow(data, flow_name, tags) for flow_name, data in confs["flows"].items() if tags.intersection(set(data["tags"]))]
            self.__confs__ = confs["confs"]
            self.__confs__["active_env"] = env

    def confs(self):
        return self.__confs__

    def get_variable(self, name):
        return __variables__.variables[name]

    def __step_runner__(self, step):
        _t = datetime.now()
        __variables__ = variables_storage()
        with Pool(step.processes_number()) as process_pool:
            process_pool.map(self.__process_runner__, step.processes())
        _info(step, _t)

    def __process_runner__(self, process):
        __variables__ = variables_storage()
        process.execute(self)

    def __flow_runner__(self, flow):
        _t = datetime.now()
        for step_name, step in flow.steps():
            self.__take_step__(step_name, step)
        _info(flow, _t)

    def start_pipeline(self):
        for fl in self.__flows__:
            self.__flow_runner__(fl)

    class flow:

        def __init__(self, flow_data, name, tags):
            self.__tags__ = flow_data["tags"]
            self.__name__ = name
            self.__steps__ = [self.step(data, step_name, self.__name__, tags) for step_name, data in flow_data["steps"].items()]

        def steps(self):
            return self.__steps__

        def step_number(self):
            return len(self.__steps__)

        def __str__(self):
            return f"Flow: {self.__name__}"

        class step:

            def __init__(self, step_data, name, belong, tags):
                import pickle
                self.__name__ = name
                self.__from_flow__ = belong
                self.__processes__ = [self.process(process_data, process_name, self.__name__, self.__from_flow__) for process_name, process_data in step_data.items() if (not "avoid_tags" in process_data.keys()) or (not tags.intersection(set(process_data["avoid_tags"])))]

            def processes(self):
                return self.__processes__

            def processes_number(self):
                return len(self.__processes__)

            def __str__(self):
                return f"Step from {self.__from_flow__} flow: {self.__name__}"

            class process:

                def __init__(self, process_data, name, step_name, flow_name):
                    self.__data__ = process_data
                    self.__name__ = name
                    self.__from_step__ = step_name
                    self.__from_flow__ = flow_name
                    self.__error_tolerance__ = self.__setup__(process_data, "error_tolerance")

                def __setup__(self, data, setup):
                    setups_defaults = {
                        "in_variables": [],
                        "out_vriables" : [],
                        "error_tolerance" : False
                    }
                    if setup in data.keys():
                        return data[setup]
                    return setups_defaults[setup]

                def execute(self, pipe):
                    module = import_module(f"pipeline.{self.__from_step__}.{self.__name__}")
                    try:
                        exit_vars = module.process(pipe)
                    except Exception as e:
                        if not self.__error_tolerance__:
                            raise step_error("Step exception without errors tolerance")
                        print(e)
                        exit_vars = ()
                    return exit_vars

