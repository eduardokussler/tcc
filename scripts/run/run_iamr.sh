#!/bin/bash


TESTS=(Bubble                    DoubleShearLayer                    FlowPastCylinder                HIT                  HotSpot                    LidDrivenCavity              Particles              Poiseuille            RayleighTaylor            TaylorGreen            TracerAdvection)
INPUTS=(inputs.2d.bubble         inputs.2d.double_shear_layer-rotate inputs.3d.flow_past_cylinder-x  inputs.3d.forced     inputs.2d.average_hotspot  inputs.2d.lid_driven_cavity  inputs_ml              inputs.2d.poiseuille  inputs.2d.rayleightaylor  inputs.2d.taylorgreen  inputs.2d.traceradvect)
EXECUTABLE=(./amr2d.gnu.CUDA.ex ./amr2d.gnu.CUDA.ex                  ./amr3d.gnu.CUDA.ex             ./amr3d.gnu.CUDA.ex  ./amr2d.gnu.CUDA.ex        ./amr2d.gnu.CUDA.ex          ./amr2d.gnu.CUDA.ex   ./amr2d.gnu.CUDA.ex    ./amr2d.gnu.CUDA.ex       ./amr2d.gnu.CUDA.ex    ./amr2d.gnu.CUDA.ex)

cd ../../projetos/IAMR/Tutorials

INDEX=0
for test in ${TESTS[@]}
do
    cd $test
    echo "running test $test"
    ${EXECUTABLE[$INDEX]} ${INPUTS[$INDEX]}
    INDEX=$((INDEX+1))
    cd ..
done