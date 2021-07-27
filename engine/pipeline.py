
class pipeline:

    from datetime import datetime
    from multiprocessing import Pool
    from engine.logger import logger

    def __init__(self, env, tags):
        from yaml import load
        from yaml.loader import SafeLoader

        self.tags = set(tags)
        with open("pipeline/pipelines_conf.yml") as file:
            confs = load(file, Loader=SafeLoader)
            self.__flows__ = [self.flow(data, flow_name, tags) for flow_name, data in confs["flows"].items() if self.tags.intersection(set(data["tags"]))]
            self.__confs__ = confs["confs"]
            self.__confs__["active_env"] = env
            self.__log_level__ = 0

    def __step_runner__(self, step):
        _t = self.datetime.now()
        log = self.logger(step, self.__log_level__)
        with self.Pool(step.processes_number()) as process_pool:
            process_pool.map(self.__process_runner__, step.processes())
        log.info(f"Step succefully ended at {self.datetime.now()} - Step time: {self.datetime.now() - _t}")

    def __process_runner__(self, process):
        process.execute(self)

    def __flow_runner__(self, flow):
        _t = self.datetime.now()
        log = self.logger(flow, self.__log_level__)

        for step in flow.steps():
            try:
                self.__step_runner__(step)
            except Exception as e:
                log.error(e)
                raise e
        log.info(f"flow succefully ended at {self.datetime.now()} - Flow time: {self.datetime.now() - _t}")

    def start_pipeline(self):
        for fl in self.__flows__:
            self.__flow_runner__(fl)

    class flow:

        def __init__(self, flow_data, name, tags):
            self.__type__ = "flow"
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
                self.__type__ = "step"
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
                    self.__type__ = "process"
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
                    from datetime import datetime
                    from importlib import import_module
                    from engine.errors import step_error
                    from engine.logger import logger

                    _t = datetime.now()
                    log = self.logger(step, self.__log_level__)

                    module = import_module(f"pipeline.{self.__from_step__}.{self.__name__}")
                    try:
                        exit_vars = module.process(pipe, log)
                    except Exception as e:
                        if not self.__error_tolerance__:
                            raise step_error("Step exception without errors tolerance")
                        log.error(e)

                    log.info(f"Process succefully ended at {self.datetime.now()} - Process time: {self.datetime.now() - _t}")
                    return
