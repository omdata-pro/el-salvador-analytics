# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "4655e07e-cb64-4682-9fba-394ce86b8a98",
# META       "default_lakehouse_name": "ElSalvador_01_Bronze",
# META       "default_lakehouse_workspace_id": "54e503e8-ffac-4107-9d85-2a67491b6def",
# META       "known_lakehouses": [
# META         {
# META           "id": "4655e07e-cb64-4682-9fba-394ce86b8a98"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

df_wb_homicide = spark.read.table("bronze_worldbank_homicide")
df_manual_homicide = spark.read.table("bronze_security_annual_totals")

df_wb_homicide.show()
df_manual_homicide.show()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import lit, col

# From World Bank: keep only years where we actually have real data (drop the null years)
wb_clean = df_wb_homicide.filter(col("Homicide_Rate_Per100k").isNotNull()) \
    .select(
        col("Country"),
        col("Year"),
        col("Homicide_Rate_Per100k"),
        lit(None).cast("double").alias("Homicide_Count"),
        lit("World Bank / UNODC").alias("Source")
    )

# From manual table: reshape to match the same column structure
manual_clean = df_manual_homicide.select(
    col("Country"),
    col("Year"),
    col("Homicide_Rate_Per100k"),
    col("Homicide_Count").cast("double"),
    col("Source")
)

# Combine into one continuous trend, sorted by year
silver_homicide_trend = wb_clean.unionByName(manual_clean).orderBy("Year")

silver_homicide_trend.show(30)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

silver_homicide_trend.write.format("delta").mode("overwrite").saveAsTable("silver_security_homicide_trend")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
