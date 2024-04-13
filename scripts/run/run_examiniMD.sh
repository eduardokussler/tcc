#!/bin/bash
# EDIT input/in.lj to run at least 10000 times (is the last paramater (run))

# Expected to run from the orchestrator directory
cd ../../projetos/ExaMiniMD/src
./ExaMiniMD -il ../input/in.lj --kokkos-threads=1 --kokkos-ndevices=1