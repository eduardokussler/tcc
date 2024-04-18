from classes.orchestrator import Orchestrator
from classes.utils import Platform

script = '../run/run_examiniMD.sh'

orchestrator = Orchestrator(platform=Platform.GEFORCE)

orchestrator.perform_experiment(script, 0.1)