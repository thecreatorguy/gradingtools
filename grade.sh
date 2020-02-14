#!/usr/bin/env sh

# This file should go in the top level grading folder. In this folder
# should only initially contain this file, the 'gradefast' folder,
# and the generic 'lab.yaml' for use with gradefast.

dl="c:/Users/tcrea/Downloads"

echo -n "What are you grading?: "
read name

if [[ ! -d $name ]]; then
    for f in $dl/*.zip; do
        echo -n "Is $f the file? (y/nothing): "
        read -e isfile
        if [[ $isfile = "y" ]]; then
            labfile=$f
        fi
    done
    if [[ -z $labfile ]]; then
        echo "There is no zip file with that name in downloads"
        read -rsp $'Press any key to continue...\n' -n1 key
        exit 1
    fi

    if [ ! -d "./provided/$name" ]; then
        mkdir "./provided/$name"
    fi
    if [ ! -d "$name" ]; then
        mkdir "$name"
    fi

    mv "$labfile" "$name/$name".zip
    cd $name
    unzip ${name}.zip
    rm ${name}.zip
    rm "index.html"
    cd ..
fi

cd $name
if [[ -f index.html ]]; then
    rm index.html
fi
for f in *.zip; do
    n=${f#*-}
    n=${n#*-}
    n=${n%%.*}
    n=${n//[[:blank:]]/}
    n=${n%-*}

    if [ -f "$f"  ]; then
        if [ ! -d "$n"  ]; then
            mkdir $n
        fi

        mv "$f" $n/$n.zip
        cd $n
        unzip $n.zip
        rm $n.zip
        cd ..
    fi
done
cd ..

if [[ ! -f $name/$name.yaml ]]; then
    cp Provided/template.yaml $name/$name.yaml
fi

read -rsp $'Make changes to yaml file and add provided files now\n' -n1 key

cd gradefast
python36.exe -m gradefast -f "..\\$name\\" --shell "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" "..\\$name\\$name.yaml"
