#!/bin/bash

for raster_file in $1/*.vrt; do
    echo $raster_file
    filename=$(basename $raster_file .vrt)
    gdal_translate $raster_file s1_tif_final_2/$filename.tif
   done
