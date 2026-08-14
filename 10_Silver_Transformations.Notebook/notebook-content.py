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
# META         },
# META         {
# META           "id": "447fcbb5-1f3d-4bcb-a966-6915930db478"
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

silver_homicide_trend.write.format("delta").mode("overwrite").saveAsTable("ElSalvador_02_Silver.dbo.silver_security_homicide_trend")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.read.table("ElSalvador_02_Silver.dbo.silver_security_homicide_trend").show(35) 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print(spark.read.table("ElSalvador_02_Silver.dbo.silver_security_homicide_trend").count()) 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_gdp_regional = spark.read.table("ElSalvador_01_Bronze.dbo.bronze_worldbank_gdp_regional"); df_fdi_regional = spark.read.table("ElSalvador_01_Bronze.dbo.bronze_worldbank_fdi_regional"); df_homicide_regional = spark.read.table("ElSalvador_01_Bronze.dbo.bronze_worldbank_homicide_regional") 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

silver_regional = df_gdp_regional.join(df_fdi_regional, on=["Country", "Year"], 
how="outer").join(df_homicide_regional, on=["Country", "Year"], how="outer").orderBy("Country", "Year"); silver_regional.show(20)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print(silver_regional.count())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

silver_regional.write.format("delta").mode("overwrite").saveAsTable("ElSalvador_02_Silver.dbo.silver_regional_comparison")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_gdp = spark.read.table("ElSalvador_01_Bronze.dbo.bronze_worldbank_gdp"); df_fdi = spark.read.table("ElSalvador_01_Bronze.dbo.bronze_worldbank_fdi")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_gdp.show(5); df_fdi.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

silver_macro = df_gdp.join(df_fdi, on=["Country", "Year"], how="outer").orderBy("Year"); silver_macro.show(20)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print(silver_macro.count())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

silver_macro.write.format("delta").mode("overwrite").saveAsTable("ElSalvador_02_Silver.dbo.silver_macro_trend")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_btc_snapshot = spark.read.table("ElSalvador_01_Bronze.dbo.bronze_bitcoin_treasury_snapshot"); 
df_btc_history = spark.read.table("ElSalvador_01_Bronze.dbo.bronze_bitcoin_treasury_history")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_btc_snapshot.show(15); df_btc_history.show(10)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F; df_snapshot_aligned = df_btc_snapshot.select(F.col("Country"), F.lit("Snapshot").alias("Record_Type"), F.lit(None).cast("string").alias("Date"), F.col("BTC_Holdings"), F.col("Current_Value_USD").alias("Value_USD"), F.col("Pct_Of_Total_Supply"), F.lit("CoinGecko").alias("Source"), F.lit(None).cast("string").alias("Notes"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_history_aligned = df_btc_history.select(F.lit("El Salvador").alias("Country"), F.col("Type").alias("Record_Type"), F.col("Date").cast("string").alias("Date"), F.col("Cumulative_BTC").alias("BTC_Holdings"), F.lit(None).cast("double").alias("Value_USD"), F.lit(None).cast("double").alias("Pct_Of_Total_Supply"), F.col("Source"), F.col("Notes"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

 silver_bitcoin = df_snapshot_aligned.unionByName(df_history_aligned); silver_bitcoin.show(25, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

silver_bitcoin.write.format("delta").mode("overwrite").saveAsTable("ElSalvador_02_Silver.dbo.silver_bitcoin_treasury")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
