#!/bin/bash

if [ -z $(which svg2png) ]
then
   brew install svg2png
fi

if [ -z $(which magick) ]
then
   brew install imagemagick
fi


RESOLUTIONS=(
   16,16x16
   32,16x16@2x
   32,32x32
   64,32x32@2x
   120,120x120
   128,128x128
   152,152x152
   167,167x167
   256,128x128@2x
   256,256x256
   512,256x256@2x
   512,512x512
   1024,512x512@2x
   1024,1024x1024
)

RESOLUTIONS_KEEP=(
   120x120
   152x152
   167x167
   1024x1024
)

for SVG in $@
do
   BASE=$(basename "$SVG" | sed 's/\.[^\.]*$//')
   echo "Processing $SVG into iconset for $BASE"
   ICONSET="$BASE.iconset"
   ICONSET_DIR="./$ICONSET"
   mkdir -p "$ICONSET_DIR"
   for RES in ${RESOLUTIONS[@]}
   do
      SIZE=$(echo $RES | cut -d, -f1)
      LABEL=$(echo $RES | cut -d, -f2)
      svg2png -w $SIZE -h $SIZE "$SVG" "$ICONSET_DIR"/icon_${LABEL}.png
   done

   mkdir ios
   for LABEL in ${RESOLUTIONS_KEEP[@]}
   do
      cp "$ICONSET_DIR"/icon_${LABEL}.png  ios/AppIcon${LABEL}.png
   done

   iconutil -c icns "$ICONSET_DIR"
   rm -rf "$ICONSET_DIR"

   magick $SVG -define icon:auto-resize=256,64,48,32,16 $BASE.ico
   
done