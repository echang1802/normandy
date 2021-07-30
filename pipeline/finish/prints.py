
from engine.variables_storage import variables_storage

def process(pipe, log):
    # Get confs
    var_str = variables_storage()
    log.info("Configuration ready")

    main_df = var_str.get("main_df")
    log.info("Data recupered")

    print("print process")
    print(main_df)
    log.info("Process ready")

    return
