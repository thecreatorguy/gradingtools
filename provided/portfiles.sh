if [ ! -f compile.sh ]; then
    echo Moving Files
    home=`pwd`
    mkdir temp
    mv */ -t temp
    cd "$1"
    cp * -r "$home/"
    cd "$home"
    directories=`find ./temp -maxdepth 1 -mindepth 1 -type d`
    if (( $# != 2 )); then
        loc=.
    else
        loc=./$2
    fi
    for dir in $directories; do
        mv -v $dir $loc
    done 
    rmdir temp
    echo Done!
else
    echo Files already moved!
fi