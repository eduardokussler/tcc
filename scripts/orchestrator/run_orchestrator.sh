PREFIX="../run/"
SCRIPTS=(run_examiniMD.sh run_quicksilver.sh)
INTERVALS=(0.1              1)

PLATFORM=$1

if [ -z $PLATFORM ]; then
    echo "The platform is required! Options are [geforce, gppd, enterprise]";
    exit 1
fi

INDEX=0

for SCRIPT in ${SCRIPTS[@]}
do
    #echo ${INTERVALS[$INDEX]}
    sudo python3 main.py -r $PREFIX$SCRIPT -p $PLATFORM -i ${INTERVALS[$INDEX]}
    INDEX=$((INDEX+1))
done