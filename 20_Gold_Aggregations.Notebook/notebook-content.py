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

df_gold_bitcoin = spark.read.table("ElSalvador_02_Silver.dbo.silver_bitcoin_treasury"); df_gold_bitcoin.write.format("delta").mode("overwrite").saveAsTable("ElSalvador_03_Gold.dbo.gold_bitcoin_treasury")

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

from pyspark.sql import functions as F; homicide_row = df_gold_security.filter(F.col("Homicide_Rate_Per100k").isNotNull()).orderBy(F.col("Year").desc()).limit(1).collect()[0]; gdp_row = df_gold_macro.filter(F.col("GDP_Growth_Pct").isNotNull()).orderBy(F.col("Year").desc()).limit(1).collect()[0]; fdi_row = df_gold_macro.filter(F.col("FDI_USD").isNotNull()).orderBy(F.col("Year").desc()).limit(1).collect()[0]; btc_row = df_gold_bitcoin.filter((F.col("Record_Type")=="Snapshot") & (F.col("Country")=="SV")).collect()[0]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

kpi_rows = [("Homicide Rate", float(homicide_row["Homicide_Rate_Per100k"]), "per 100k", str(homicide_row["Year"]), homicide_row["Source"]), ("GDP Growth", float(gdp_row["GDP_Growth_Pct"]), "%", str(gdp_row["Year"]), "World Bank"), ("FDI Net Inflows", float(fdi_row["FDI_USD"]), "USD", str(fdi_row["Year"]), "World Bank"), ("Bitcoin Treasury", float(btc_row["BTC_Holdings"]), "BTC", "Current", btc_row["Source"])]; gold_kpi_summary = spark.createDataFrame(kpi_rows, ["Metric", "Value", "Unit", "As_Of", "Source"]); gold_kpi_summary.show(truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

gold_kpi_summary.write.format("delta").mode("overwrite").saveAsTable("ElSalvador_03_Gold.dbo.gold_kpi_summary")

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
