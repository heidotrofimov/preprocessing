import os
import sys

S1=sys.argv[1]  #Path to the S1 raster, based on which we want to predict sNDVI

#Linearize raster

'''
outdir="tmp"
os.system("mkdir "+outdir)
filename=os.path.basename(S1).split(".")[0]
prefix=outdir+"/"+filename

band1=prefix+"_s0vv.tif"      # backscattering in VV-polarization
band2=prefix+"_s0vh.tif"      # backscattering in VH-polarization
band3=prefix+"_cohvv.tif"     # coherence in VV-polarization
band4=prefix+"_cohvh.tif"     # coherence in VH-polarization

os.system("gdal_calc.py -A "+S1+" --A_band=1 --outfile="+band1+" --type=Float32 --NoDataValue=-32768 --calc=\"10**(A.astype(numpy.float32)/1e4 - 2.0)\" &>/dev/null")
os.system("gdal_calc.py -A "+S1+" --A_band=2 --outfile="+band2+" --type=Float32 --NoDataValue=-32768 --calc=\"10**(A.astype(numpy.float32)/1e4 - 2.0)\" &>/dev/null")
os.system("gdal_calc.py -A "+S1+" --A_band=3 --outfile="+band3+" --type=Float32 --NoDataValue=-32768 --calc=\"A.astype(numpy.float32)/1e4\" &>/dev/null")
os.system("gdal_calc.py -A "+S1+" --A_band=4 --outfile="+band4+" --type=Float32 --NoDataValue=-32768 --calc=\"A.astype(numpy.float32)/1e4\" &>/dev/null")

os.system("gdalbuildvrt -q -separate "+prefix+".vrt "+band1+" "+band2+" "+band3+" "+band4)
os.system("gdal_translate "+prefix+".vrt tmp/"+filename+".tif")
'''

#Colocate the linearized raster with S2 products:

for S2_product in os.listdir("S2_products"):
  for folder3 in os.listdir('S2_products/'+S2_product+'/GRANULE/'):
    if("L2" in folder3):
      for filename2 in os.listdir('S2_products/'+S2_product+'/GRANULE/'+folder3+'/IMG_DATA/R10m/'):
        if('B02_10m.jp2' in filename):
          B02='S2_product/'+S2_product+'/GRANULE/'+folder3+'/IMG_DATA/R10m/'+filename2
          B02name=filename2
  targetpath=outdir+"/"+filename2+".dim"
  os.system("/snap/snap8/bin/gpt collocation.xml -PB02=\""+B02+"\" -PS1=\""+outdir+"/"+S1+"\" -PB02name=\""+B02name+"\" -Ptargetpath=\""+targetpath+"\"")






