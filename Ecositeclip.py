#CODE FOR ARCPY
#MERGE
#Follow steps 1-5 to set directories
# 1. Set the workspace environment (path to folder where shapefiles are that you want to merge)
workspace = "C:/Users/ryan.ray/Desktop/Test/Out_Footprints"
arcpy.env.workspace = workspace

# 2. Set the merged output shapefile path and name
output_merged = "C:/Users/ryan.ray/Desktop/Test/MERGE/out_footprint_merged.shp"

# 3. Perform the merge operation (change to appropriate geometry - POLYGON or POLYLINE)
shapefiles = arcpy.ListFeatureClasses("*.shp", "POLYGON")  

# Checks if there are shapefiles in the workspace to merge
if shapefiles:
    arcpy.Merge_management(shapefiles, output_merged)
    print("Shapefiles merged successfully.")
else:
    print("No shapefiles found in the workspace.")






# CLIP AND NAME FILES BASED ON ECOSITE
# 4. Set the input shapefile paths (for merged file and vegetation file)
input_footprint_lines = "C:/Users/ryan.ray/Desktop/Test/MERGE/out_footprint_merged.shp"
input_veg = "C:/Users/ryan.ray/Desktop/Test/Veg/veg.shp"

# Dictionary mapping gridcode values to output shapefile names (selects from vegetation ecosites for clipping and naming)
# If gridcode range = name, replace the gridcode number with the following: range(0,11): "upland_treed_mesic"
gridcode_mapping = {
    0: "excluded",
    10: "upland_treed_mesic_no_fire",
    11: "upland_treed_mesic_partial_burn",
    12: "upland_treed_mesic_burned",
    20: "upland_treed_dry_no_fire",
    21: "upland_treed_dry_partial_burn",
    22: "upland_treed_dry_burned",
    30: "transitional_treed_no_fire",
    31: "transitional_treed_partial_burn",
    32: "transitional_treed",
    40: "wetland_treed_no_fire",
    41: "wetland_treed_partial_burn",
    42: "wetland_treed_burned",
    50: "wetland_low_density_treed_partial_burn",
    51: "wetland_low_density_treed_partial_burn",
    52: "wetland_low_density_treed_burned"
}

# Loop over the gridcode values and clip the input layer
for gridcode, output_name in gridcode_mapping.items():
    # Set the expression for the selection (if gridcode = 0, expression will use value of 0)
    expression = f"gridcode = {gridcode}"

    # Create a feature layer from the input_veg shapefile (temporary layer)
    arcpy.MakeFeatureLayer_management(input_veg, "clip_features")

    # Select features based on the current gridcode
    # Uses temp layer based on the expression value and chooses the features in the vegetation grid code
    arcpy.SelectLayerByAttribute_management("clip_features", "NEW_SELECTION", expression)

    # 5. Set the output shapefile path for the labelled ecosites
    # (autofills name based on gridcode mapping)
    output_shapefile = f"C:/Users/ryan.ray/Desktop/Test/MERGE/{output_name}.shp"

    # Clip the input footprint layer using the selected features as clip features
    arcpy.Clip_analysis(input_footprint_lines, "clip_features", output_shapefile)

    # Delete the clip_features layer (clean up file, not needed)
    arcpy.Delete_management("clip_features")

# Delete the out_footprint_merged file (clean up file, not needed)
arcpy.Delete_management(output_merged)