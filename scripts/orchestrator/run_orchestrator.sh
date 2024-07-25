PREFIX="../run/"
SCRIPTS=(run_examiniMD.sh  run_quicksilver.sh run_goulash.sh run_hypar.sh run_iamr.sh run_miniMDock.sh run_kripke.sh)
INTERVALS=(0.1             1                  1              1            1           1                1)
PLATFORM_PARAM=$1
PLATFORM=$PLATFORM_PARAM
if [ $PLATFORM = "eekussler_laptop" ]; then
    PLATFORM="geforce"
fi

if [ -z $PLATFORM ]; then
    echo "The platform is required! Options are [geforce, gppd, enterprise, eekussler_laptop]";
    exit 1
fi

INDEX=0

for SCRIPT in ${SCRIPTS[@]}
do
    #echo ${INTERVALS[$INDEX]}
    # This test uses too much memory and doesn't run on my laptop
    if [ $PLATFORM_PARAM = "eekussler_laptop" ] && [ $SCRIPT = "run_hypar.sh" ]; then
        echo "$SCRIPT is not supported in this platform ($PLATFORM_PARAM)."
        INDEX=$((INDEX+1))
        continue
    fi
    sudo python3 main.py -r $PREFIX$SCRIPT -p $PLATFORM -i ${INTERVALS[$INDEX]}
    INDEX=$((INDEX+1))
done