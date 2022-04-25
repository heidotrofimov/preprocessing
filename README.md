# Biomass data preparation
The purpose of this repository is to prepare data for sNDVI raster creation (prediction) pipeline. It assumes that the S1 rasters have been already created and stored in S3 in a location that is defined in the config file. It will download the S1 rasters from given location, collocate them with suitable S2 products and in case cloudfree S2 products are found from +/- 2 days from S1 date, will add B2,B3,B4,B8 and NDVI values along with kappamask prediction mask as separate bands to the collocated S1 raster. The final rasters that include S2 data will be saved in the folder "data", while the collocated S1 rasters for which no cloudfree S2 products exist will be saved in the folder "collocated_S1".

It will work in senpy environment with the command

        python main_engine.py -c config.json
 
The code uses kappamask, which is called out as a subprocess. It is assumed that the user has saved the cm_predict as separate repository, created the cm_predict environment and verified that it is working. The first 10 parameters in the config.json are kappamask parameters. The product name need not be specified, but the "level_product" should be "L2A".

The explanation of the rest of the parameters follows. The parameters that the user should probably change are:
        "s3cfg_path" : "/home/heido/.s3cfg_creo",
"s3_loc" : The location on S3 where the S1 rasters are stored, eg "s3://ard/ard-demo-de/s1/"
"esa_credentials_file" : Path to the file that includes your scihub login info (username on first line and password on second line). This info will not be logged by the code in any way.
"input_shp" : Path to the shapefile of the AOI. Make sure it corresponds exactly to the S1 rasters.
"cm_predict_dir" : absolute path to the repository of cm_predict
"cm_predict_python" : absolute path to the cm_predict environment python executable, like "/home/{user}/miniconda3/envs/cm_predict/bin/python"

The rest of the parameters need not be changed, but the explanation follows:

"S2_bands" : - the S2 bands which we want to use as input for prediction, currently it's ["B2","B3","B4","B8"]
"out_path" : - the filename where scihub search results will be saved, such as "tmp.xml",
"cloudiness_percentage" : the maximum cloudiness percentage which will be used in scihub search when we are looking for suitable S2 products. Currently it's set to 35 from experience.
"cloudiness_percentage_2" : 0.4,
Folders: the names of the folders the code will use, most of which are only temporary. 
