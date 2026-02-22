#!/bin/bash

if [ -z $(which svg2png) ]
then
   brew install svg2png
fi

RESOLUTIONS=(
   48,mipmap-mdpi
   72,mipmap-hdpi
   96,mipmap-xhdpi
   144,mipmap-xxhdpi
   192,mipmap-xxxhdpi
)

for SVG in $@
do
   BASE=$(basename "$SVG" | sed 's/\.[^\.]*$//')
   echo "Processing $SVG into ANDROID iconset for $BASE"

   for RES in ${RESOLUTIONS[@]}
   do
      SIZE=$(echo $RES | cut -d, -f1)
      LABEL=$(echo $RES | cut -d, -f2)
      ICON_PATH="android_icons/${LABEL}"

      if [ ! -d $ICON_PATH ]
      then
         mkdir -p $ICON_PATH
      fi

      svg2png -w $SIZE -h $SIZE "$SVG" "$ICON_PATH/icon.png"
   done

done