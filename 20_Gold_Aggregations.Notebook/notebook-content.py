# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "447fcbb5-1f3d-4bcb-a966-6915930db478",
# META       "default_lakehouse_name": "ElSalvador_02_Silver",
# META       "default_lakehouse_workspace_id": "54e503e8-ffac-4107-9d85-2a67491b6def",
# META       "known_lakehouses": [
# META         {
# META           "id": "447fcbb5-1f3d-4bcb-a966-6915930db478"
# META         },
# META         {
# META           "id": "06bd0ffa-add5-40a5-9f6d-b81355c6e8ad"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

df_gold_security = spark.read.table("ElSalvador_02_Silver.dbo.silver_security_homicide_trend"); df_gold_security.write.format("delta").mode("overwrite").saveAsTable("ElSalvador_03_Gold.dbo.gold_security_trend")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_gold_macro = spark.read.table("ElSalvador_02_Silver.dbo.silver_macro_trend"); df_gold_macro.write.format("delta").mode("overwrite").saveAsTable("ElSalvador_03_Gold.dbo.gold_macro_trend")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F; df_gold_bitcoin = spark.read.table("ElSalvador_02_Silver.dbo.silver_bitcoin_treasury"); df_gold_bitcoin.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("ElSalvador_03_Gold.dbo.gold_bitcoin_treasury"); saved_gold_bitcoin = spark.read.table("ElSalvador_03_Gold.dbo.gold_bitcoin_treasury"); print("Saved Gold rows:", saved_gold_bitcoin.count()); print("Saved Date type:", dict(saved_gold_bitcoin.dtypes).get("Date")); print("Saved columns:", saved_gold_bitcoin.columns); saved_gold_bitcoin.filter((F.col("Country_Code") == "SV") & (F.col("Record_Type") == "Snapshot") & (F.col("Government_Level") == "National")).select("Entity_Name", "BTC_Holdings", "Value_USD").show(truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_gold_regional = spark.read.table("ElSalvador_02_Silver.dbo.silver_regional_comparison"); df_gold_regional.write.format("delta").mode("overwrite").saveAsTable("ElSalvador_03_Gold.dbo.gold_regional_comparison")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F; df_gold_security = spark.read.table("ElSalvador_03_Gold.dbo.gold_security_trend"); df_gold_macro = spark.read.table("ElSalvador_03_Gold.dbo.gold_macro_trend"); df_gold_bitcoin = spark.read.table("ElSalvador_03_Gold.dbo.gold_bitcoin_treasury"); homicide_row = df_gold_security.filter(F.col("Homicide_Rate_Per100k").isNotNull()).orderBy(F.col("Year").desc()).limit(1).collect()[0]; gdp_row = df_gold_macro.filter(F.col("GDP_Growth_Pct").isNotNull()).orderBy(F.col("Year").desc()).limit(1).collect()[0]; fdi_row = df_gold_macro.filter(F.col("FDI_USD").isNotNull()).orderBy(F.col("Year").desc()).limit(1).collect()[0]; bitcoin_row = df_gold_bitcoin.filter((F.col("Country_Code") == "SV") & (F.col("Country_Name") == "El Salvador") & (F.col("Government_Level") == "National") & (F.col("Record_Type") == "Snapshot")).orderBy(F.col("BTC_Holdings").desc()).limit(1).collect()[0]; print("Homicide:", homicide_row["Homicide_Rate_Per100k"], homicide_row["Year"]); print("GDP:", gdp_row["GDP_Growth_Pct"], gdp_row["Year"]); print("FDI:", fdi_row["FDI_USD"], fdi_row["Year"]); print("Bitcoin:", bitcoin_row["BTC_Holdings"], bitcoin_row["Entity_Name"])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

kpi_rows = [("Homicide Rate", float(homicide_row["Homicide_Rate_Per100k"]), "per 100k", str(homicide_row["Year"]), homicide_row["Source"]), ("GDP Growth", float(gdp_row["GDP_Growth_Pct"]), "%", str(gdp_row["Year"]), "World Bank"), ("FDI Net Inflows", float(fdi_row["FDI_USD"]), "USD", str(fdi_row["Year"]), "World Bank"), ("Bitcoin Treasury", float(bitcoin_row["BTC_Holdings"]), "BTC", "Current", "CoinGecko")]; gold_kpi_summary = spark.createDataFrame(kpi_rows, ["Metric", "Value", "Unit", "As_Of", "Source"]); gold_kpi_summary.show(truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

gold_kpi_summary.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("ElSalvador_03_Gold.dbo.gold_kpi_summary"); saved_kpi_summary = spark.read.table("ElSalvador_03_Gold.dbo.gold_kpi_summary"); print("Saved KPI rows:", saved_kpi_summary.count()); saved_kpi_summary.orderBy("Metric").show(truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

for t in ["gold_security_trend", "gold_macro_trend", "gold_bitcoin_treasury", "gold_regional_comparison", "gold_kpi_summary"]: spark.read.table(f"ElSalvador_03_Gold.dbo.{t}").toPandas().to_csv(f"/lakehouse/default/Files/{t}.csv", index=False)

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

# CELL ********************

notebookutils.session.stop()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F; gold_refresh_metadata = spark.range(1).select(F.lit("ElSalvador_Analytics").alias("Model_Name"), F.current_timestamp().alias("Last_Updated_UTC"), F.to_date(F.from_utc_timestamp(F.current_timestamp(), "America/Chicago")).alias("Last_Updated_Date")); gold_refresh_metadata.write.format("delta").mode("overwrite").saveAsTable("ElSalvador_03_Gold.dbo.gold_refresh_metadata"); spark.read.table("ElSalvador_03_Gold.dbo.gold_refresh_metadata").show(truncate=False)

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
