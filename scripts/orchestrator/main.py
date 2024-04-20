from classes.orchestrator import Orchestrator
from classes.utils import Platform

script = '../run/run_examiniMD.sh'

orchestrator = Orchestrator(platform=Platform.GEFORCE, run_script=script)

orchestrator.perform_experiment(0.1)