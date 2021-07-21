
import sys
import yaml
from datetime import datetime
from yaml.loader import SafeLoader
from importlib import import_module
import multiprocessing
import multiprocessing.pool
from tools.engine_errors import step_error

def _info(title, _t):
    print(title , 'start at:', _t, 'process time:', datetime.now() - _t)
import multiprocessing.pool

class NoDaemonProcess(multiprocessing.Process):
    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass


class NoDaemonContext(type(multiprocessing.get_context())):
    Process = NoDaemonProcess

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class NestablePool(multiprocessing.pool.Pool):
    def __init__(self, *args, **kwargs):
        kwargs['context'] = NoDaemonContext()
        super(NestablePool, self).__init__(*args, **kwargs)

class variables_storage:

    def __init__(self):
        #self.__variables__ = {}
        pass

    def __setattr__(self, name, var):
        self.__dict__[name] = var

class flow:

    def __init__(self, flow_data, name, tags):
        self.__tags__ = flow_data["tags"]
        self.__name__ = name
        self.__steps__ = [step(data, step_name, self.__name__, tags) for step_name, data in flow_data["steps"].items()]

    def steps(self):
        return self.__steps__

    def step_number(self):
        return len(self.__steps__)

    def __str__(self):
        return f"Flow: {self.__name__}"

class step:

    def __init__(self, step_data, name, belong, tags):
        self.__name__ = name
        self.__from_flow__ = belong
        self.__processes__ = [process(process_data, process_name, self.__name__, self.__from_flow__) for process_name, process_data in step_data.items() if (not "avoid_tags" in process_data.keys()) or (not tags.intersection(set(process_data["avoid_tags"])))]

    def processes(self):
        return self.__processes__

    def processes_number(self):
        return len(self.__processes__)

    def __str__(self):
        return f"Step from {self.__from_flow__} flow: {self.__name__}"

setups_defaults = {
    "in_variables": [],
    "out_vriables" : [],
    "error_tolerance" : False
}

class process:

    def __init__(self, process_data, name, step_name, flow_name):
        self.__data__ = process_data
        self.__name__ = name
        self.__from_step__ = step_name
        self.__from_flow__ = flow_name
        #self.__in_variables__ = self.__setup__(process_data, "in_variables")
        #self.__out_variables__ = self.__setup__(process_data, "out_variables")
        self.__error_tolerance__ = self.__setup__(process_data, "error_tolerance")
        self.__import_module__()

    def __setup__(self, data, setup):
        if setup in data.keys():
            return data[setup]
        return setups_defaults[setup]

    def __import_module__(self):
        self.module = import_module(f"pipeline.{self.__from_step__}.{self.__name__}")

    def execute(self, pipeline):
        try:
            self.module.process(confs = pipeline.confs(), args = pipeline.variables())
            # TODO: Use variables object!   <<<--------------------------------------------
        except Exception as e:
            if not self.__error_tolerance__:
                raise step_error("Step exception without errors tolerance")
            print(e)

class pipeline:

    def __init__(self, env, tags):
        tags = set(tags)
        with open("pipeline/pipelines_conf.yml") as file:
            confs = yaml.load(file, Loader=SafeLoader)
            self.__flows__ = [flow(data, flow_name, tags) for flow_name, data in confs["flows"].items() if tags.intersection(set(data["tags"]))]
            self.__confs__ = confs["confs"]
            self.__confs__["active_env"] = env
        self.__variables__ = variables_storage()

    def confs(self):
        return self.__confs__

    def variables(self):
        return self.__variables__

    def __step_runner__(self, step):
        _t = datetime.now()
        with NestablePool(step.processes_number()) as process_pool:
            process_pool.map(self.__process_runner__, step.processes())
        _info(step, _t)

    def __process_runner__(self, process):
        process.execute(self)

    def __flow_runner__(self, flow):
        _t = datetime.now()
        for step in flow.steps():
            self.__step_runner__(step)
        _info(flow, _t)

    def start_pipeline(self):
        with NestablePool(len(self.__flows__)) as flow_pool:
            flow_pool.map(self.__flow_runner__, self.__flows__)
