import argparse
from classes.orchestrator import Orchestrator
from classes.utils import Platform
import logging


argparser = argparse.ArgumentParser(
                    prog='Orchestrator',
                    description='Runs a HPC Cuda program specified by `run_script` multiple times, variating GPU clocks and collecting the time spent and GPU telemtry')

argparser.add_argument('-r', '--run_script', action='store', dest='run_script', help='The bash script that runs the hpc program', required=True)
argparser.add_argument('-p', '--platform', action='store', dest='platform', help='The target platform', required=True)
argparser.add_argument('-i', '--interval', action='store', dest='interval', type=float, help='Measurements interval', required=True)

args = argparser.parse_args()
log = logging.Logger('main')
log.info(f'''Running orchestrator with: 
             run_script: {args.run_script},
             platform={args.platform},
             measurement interval = {args.interval}''')

orchestrator = Orchestrator(platform=Platform.from_str(args.platform), run_script=args.run_script)

orchestrator.perform_experiment(args.interval)