# Execute the file
# java --module-path "c:/javafx/lib" --add-modules=javafx.controls [filename] >> $out

# Execute java file with arguments
# java --module-path "c:/javafx/lib" --add-modules=javafx.controls [filename] [arguments] >> $out

# Execute java file with input
# java --module-path "c:/javafx/lib" --add-modules=javafx.controls [filename] < cat "${start}/[inputFileName]" >> $out

# Execute java file with arguments and input
#java --module-path "c:/javafx/lib" --add-modules=javafx.controls [filename] [arguments] < cat "${start}/[inputFileName]" >> $out

# Diff
# diff -B -b --strip-trailing-cr $temp [goodFile] >> $out

start=`pwd`
out="${start}/output.txt"
temp="${start}/temp.txt"

sep() {
	echo ==================================================================================================================== >> $out
}

echo "Starting grading now..."
if [ -e "output.txt" ]; then
    rm output.txt
fi

cd src
#--------TESTS--------#



#--------TESTS--------#
cd "$start"
cat "$out"
