#!/bin/bash
license_server='192.168.0.170'
interactive_shell_set=''
dir_set=''
dir=''
file_set=''
files=''
gui_set=''
output_set=''
output='./'
base_set=''
extension_set=''
build_set=''

f=''
g=''
build=''

get_abs_filename() {
  # $1 : relative filename
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}

#Read Flags
while getopts 'bigl:o:d:f:' flag; do
  case "${flag}" in
    b) build_set=1 ;;
    l) license_server="$OPTARG" ;;
    i) interactive_shell_set=1 ;;
    g) gui_set=1 ;;
    o) output="${OPTARG}" && output_set=1 ;;
    d) dir=$(get_abs_filename "${OPTARG}") && dir_set=1 ;;
    f) files=("$OPTARG") && file_set=1
        until [[ $(eval "echo \${$OPTIND}") =~ ^-.* ]] || [ -z $(eval "echo \${$OPTIND}") ]; do
                files+=($(eval "echo \${$OPTIND}"))
                OPTIND=$((OPTIND + 1))
            done
        ;;
  esac
done

mkdir -p openTap/.resources/testPlans

#Flag Check
if [ "$file_set" ];
then
    for file in "${files[@]}"
    do
        if [ ! -f "$file" ];
        then
            echo "File or File Path does not exist."
            echo "File Selected: $file"
            echo "Usage: ./runall.sh -f <file1> <file2> ... <fileN> [-d:o:g]"
            exit 1
        fi
        if [ "${file: -8}" != ".TapPlan" ];
        then
            echo "Files must have the .TapPlan extension."
            echo "File Selected: $file"
            echo "Usage: ./runall.sh -f <file1> <file2> ... <fileN> [-d:o:g]"
            exit 1
        fi
    done
    cp "${files[@]}" openTap/.resources/testPlans/
    f='--build-arg FILES=true'
fi

if [ "$dir_set" ];
then
    if [ ! -d "$dir" ] || [ -z "$dir" ];
    then
        echo "Directory path is incorrect or directory does not exist."
        echo "Usage: ./runall.sh -d <directory1> <directory2> ... <directoryN> [-f:o:g]"
        exit 1
    fi
    if [ -z "$(ls -A $dir)" ];
    then
        echo "Directory is empty."
        echo "Usage: ./runall.sh -d <directory1> <directory2> ... <directoryN> [-f:o:g]"
        exit 1
    fi
    cp $dir/*.TapPlan openTap/.resources/testPlans
    f='--build-arg FILES=true'

fi

if [ "$gui_set" ];
then
    echo "GUI is set to: " $gui_set
    g='--build-arg GUI='$gui_set
fi

# # if [ -d "$output_set" ]
# # then
# #     echo "Output is set to: " $output
# #     echo "Output is not currently implemented."
# # fi
# #End of Flag Check

echo 'Beginning build...'
echo 'Checking Docker Hub for Images..'
if [ ! $build_set ] && [ "$(docker manifest inspect ucsckeysight/opentap:latest > /dev/null ; $? 2>&1)" ];
then
    echo 'Found OpenTAP Base Image...'
    docker pull ucsckeysight/opentap:latest
else
    cd openTap
    echo 'Building openTap...'
    build="docker build -t ucsckeysight/opentap:latest $f $g . > /dev/null"
    eval "$build"
    cd ..
fi

if [ ! $build_set ] && [ $gui_set ] && [ "$(docker manifest inspect ucsckeysight/opentapflux:latest > /dev/null ; $? 2>&1)" ];
then
    echo 'Found OpenTAP Flux Extension...'
    docker pull ucsckeysight/opentapflux:latest
elif [ "$gui_set" ];
then
    cd openTap
    echo 'Building OpenTAP Flux Extension...'
    docker build -t ucsckeysight/opentapflux:latest -f DockerfileVNC .
    cd ..
fi

if [ ! $build_set ] && [ "$(docker manifest inspect ucsckeysight/urhandler:latest > /dev/null ; $? 2>&1)" ];
then 
    echo 'Found UR Sim Image...'
    docker pull ucsckeysight/urhandler:latest
else
    cd urHandler
    echo 'Building urHandler...'
    build='docker build -t ucsckeysight/urhandler:latest . > /dev/null'
    eval "$build"
    cd ..
fi

echo 'Running Containers...'
tap_dir=$(get_abs_filename './openTap')
docker volume create --name resources --opt type=none --opt device=$tap_dir --opt o=bind

if [ "$gui_set" ];
then
    docker-compose up -d urHandler

    id=$(docker run -d \
    -p 5902:5902 \
    -p 30002:30002 \
    --shm-size=256m \
    -e VNC_PASSWD=keysight \
    -e LM_LICENSE_FILE=@$license_server \
    -v ./openTap/.resources/testPlans,target=/environment/testPlans/ \
    ucsckeysight/opentapflux:latest /opt/container_startup.sh)

    docker network connect opentap-cobot-plugin_ursim_net "$id"

    printf "\n\n"
    echo "------- NoVNC Services have started -----------"
    echo ""
    echo "  --> OpenTAP GUI Services: http://localhost:5902/?password=keysight"
    echo ""
    echo "  --> UR3e GUI Services: http://localhost:6080/vnc_auto.html"
    echo ""
    echo "  Containers now running in the background..."
    echo "-----------------------------------------------"
    ( trap exit SIGINT ; read -r -d '' _ </dev/tty ) ## wait for Ctrl-C
    printf "\n"
    echo "Removing OpenTAP Container @ $id..."
    docker stop $id
fi

if [ "$interactive_shell_set" ];
then
    docker-compose run --rm -e LM_LICENSE_FILE=@$license_server openTapController /bin/bash
fi

if [ ! $interactive_shell_set ] && [ ! $gui_set ] && [ "$file_set" ] || [ "$dir_set" ];
then
    docker-compose run --rm openTapController ./scripts/runTestPlans.sh
fi

printf 'Removing Docker Network\n'
rm -rf openTap/.resources/testPlans/

docker-compose down
exit 0