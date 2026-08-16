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

df_btc_snapshot = spark.table("ElSalvador_01_Bronze.dbo.bronze_bitcoin_treasury_snapshot"); df_btc_history = spark.table("ElSalvador_01_Bronze.dbo.bronze_bitcoin_treasury_history"); print("Bitcoin Bronze tables loaded:", df_btc_snapshot.count(), "snapshot rows and", df_btc_history.count(), "history rows")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F; country_name_map = F.create_map(F.lit("US"), F.lit("United States"), F.lit("CN"), F.lit("China"), F.lit("GB"), F.lit("United Kingdom"), F.lit("KP"), F.lit("North Korea"), F.lit("BT"), F.lit("Bhutan"), F.lit("SV"), F.lit("El Salvador"), F.lit("AE"), F.lit("United Arab Emirates"), F.lit("VE"), F.lit("Venezuela"), F.lit("FI"), F.lit("Finland"), F.lit("DE"), F.lit("Germany"), F.lit("BG"), F.lit("Bulgaria")); df_snapshot_aligned = df_btc_snapshot.select(F.col("Name").alias("Entity_Name"), F.col("Country").alias("Country_Code"), F.element_at(country_name_map, F.col("Country")).alias("Country_Name"), F.when(F.col("Name") == "Texas", F.lit("State")).when(F.col("Name") == "Roswell, New Mexico", F.lit("Municipal")).otherwise(F.lit("National")).alias("Government_Level"), F.lit("Snapshot").alias("Record_Type"), F.lit(None).cast("date").alias("Date"), F.col("BTC_Holdings"), F.col("Current_Value_USD").alias("Value_USD"), F.col("Pct_Of_Total_Supply"), F.lit("CoinGecko").alias("Source"), F.lit(None).cast("string").alias("Notes"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_history_aligned = df_btc_history.select(F.lit("El Salvador").alias("Entity_Name"), F.lit("SV").alias("Country_Code"), F.lit("El Salvador").alias("Country_Name"), F.lit("National").alias("Government_Level"), F.col("Type").alias("Record_Type"), F.to_date(F.col("Date"), "yyyy-MM-dd").alias("Date"), F.col("Cumulative_BTC").alias("BTC_Holdings"), F.lit(None).cast("double").alias("Value_USD"), F.lit(None).cast("double").alias("Pct_Of_Total_Supply"), F.col("Source"), F.col("Notes"))

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

silver_bitcoin = df_snapshot_aligned.unionByName(df_history_aligned); silver_bitcoin.printSchema(); silver_bitcoin.show(25, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

silver_bitcoin.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("ElSalvador_02_Silver.dbo.silver_bitcoin_treasury"); saved_silver_bitcoin = spark.table("ElSalvador_02_Silver.dbo.silver_bitcoin_treasury"); print("Saved Silver rows:", saved_silver_bitcoin.count()); print("Saved Date type:", dict(saved_silver_bitcoin.dtypes).get("Date")); print("Saved columns:", saved_silver_bitcoin.columns)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

notebookutils.session.stop()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
