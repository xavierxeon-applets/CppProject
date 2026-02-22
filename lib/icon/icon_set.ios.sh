#!/bin/bash

if [ -z $(which svg2png) ]
then
   brew install svg2png
fi

RESOLUTIONS=(
   120,120x120
   152,152x152
   167,167x167
   1024,1024x1024
)
for SVG in $@
do
   BASE=$(basename "$SVG" | sed 's/\.[^\.]*$//')
   echo "Processing $SVG into IOS iconset for $BASE"
      
   if [ ! -d Assets.xcassets/AppIcon.appiconset ]
   then
      mkdir -p Assets.xcassets/AppIcon.appiconset
   fi
   
   for RES in ${RESOLUTIONS[@]}
   do
      SIZE=$(echo $RES | cut -d, -f1)
      LABEL=$(echo $RES | cut -d, -f2)
      svg2png -w $SIZE -h $SIZE "$SVG" Assets.xcassets/AppIcon.appiconset/AppIcon${LABEL}.png
   done

done