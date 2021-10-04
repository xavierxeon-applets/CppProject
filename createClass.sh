#!/bin/bash


if [ -z "$1" ]
then
   echo "must provide at least one class name"
   exit
fi

for CLASS_NAME in  $@
do
   if [ -f "${CLASS_NAME}.h" ]
   then
      echo "header ${CLASS_NAME}.h already exists"
   else
      echo "#ifndef ${CLASS_NAME}H" > ${CLASS_NAME}.h
      echo "#define ${CLASS_NAME}H" >> ${CLASS_NAME}.h
      echo "" >> ${CLASS_NAME}.h
      echo "class ${CLASS_NAME}" >> ${CLASS_NAME}.h
      echo "{" >> ${CLASS_NAME}.h
      echo "public:" >> ${CLASS_NAME}.h
      echo "   ${CLASS_NAME}();" >> ${CLASS_NAME}.h
      echo "};" >> ${CLASS_NAME}.h
      echo "" >> ${CLASS_NAME}.h
      echo "#endif //  ${CLASS_NAME}H" >> ${CLASS_NAME}.h
   fi

   if [ -f "${CLASS_NAME}.cpp" ]
   then
      echo "source ${CLASS_NAME}.cpp already exists"
   else
      echo "#include \"${CLASS_NAME}.h\"" > ${CLASS_NAME}.cpp
      echo "" >> ${CLASS_NAME}.cpp
      echo "${CLASS_NAME}::${CLASS_NAME}()" >> ${CLASS_NAME}.cpp
      echo "{" >> ${CLASS_NAME}.cpp
      echo "}" >> ${CLASS_NAME}.cpp
      echo "" >> ${CLASS_NAME}.cpp
   fi

done
