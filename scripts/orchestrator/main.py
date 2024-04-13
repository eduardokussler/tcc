from classes.orchestrator import *

script = '../run/run_examiniMD.sh'

orchestrator = Orchestrator()

orchestrator.perform_experiment(script)