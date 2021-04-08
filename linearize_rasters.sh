# ===========================================================
# Convert SENPY 16bit signed integer raster math output
# to a linear 32bit floating point format.
# In addition, add band with backscattering VH-VV ratio.
# (c) 2021 KappaZeta Ltd
# ===========================================================

if [ $# -ne 1 ]; then
    echo "Usage: $0 path/to/raster/images"
    exit 1
fi

datadir=$1
outdir=tmp

cd $datadir
rm -rf $outdir
mkdir $outdir

for raster_file in *.tif; do
    echo "Processing "$raster_file

    filename=$(basename $raster_file .tif)
    prefix=$outdir/$filename

    band1=$prefix"_s0vv.tif"      # backscattering in VV-polarization
    band2=$prefix"_s0vh.tif"      # backscattering in VH-polarization
    band3=$prefix"_cohvv.tif"     # coherence in VV-polarization
    band4=$prefix"_cohvh.tif"     # coherence in VH-polarization
    band5=$prefix"_linc.tif"      # local incidence angle
    #band6=$prefix"_s0vhvv.tif"    # ratio of band2 & band1

    gdal_calc.py -A $raster_file --A_band=1 --outfile=$band1 --type=Float32 --NoDataValue=-32768 --calc="10**(A.astype(numpy.float32)/1e4 - 2.0)" &>/dev/null
    gdal_calc.py -A $raster_file --A_band=2 --outfile=$band2 --type=Float32 --NoDataValue=-32768 --calc="10**(A.astype(numpy.float32)/1e4 - 2.0)" &>/dev/null
    gdal_calc.py -A $raster_file --A_band=3 --outfile=$band3 --type=Float32 --NoDataValue=-32768 --calc="A.astype(numpy.float32)/1e4" &>/dev/null
    gdal_calc.py -A $raster_file --A_band=4 --outfile=$band4 --type=Float32 --NoDataValue=-32768 --calc="A.astype(numpy.float32)/1e4" &>/dev/null
    gdal_calc.py -A $raster_file --A_band=5 --outfile=$band5 --type=Float32 --NoDataValue=-32768 --calc="A.astype(numpy.float32)/1e2" &>/dev/null
    gdal_calc.py -A $band1 -B $band2 --outfile=$band6 --type=Float32 --NoDataValue=-32768 --quiet --calc="B/A"

    # virtual raster to bind all the separate bands into a single file
    gdalbuildvrt -q -separate $prefix.vrt $band1 $band2 $band3 $band4 $band5
    echo $prefix.tif
    rm $prefix.tif
    gdal_translate $prefix.vrt $prefix.tif
done

mv $outdir/* .
rm -r $outdir
