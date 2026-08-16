# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# MARKDOWN ********************

# # El Salvador Analytics — Project Log
# 
# **Project start:** 2026-07-30
# **Fabric trial expires:** ~2026-08-24
# **Workspace capacity:** Fabric Trial, SKU FTL4, Region: East US
# 
# ---
# 
# ## Decisions Log
# 
# ## Troubleshooting Log
# 
# ## Daily Progress


# MARKDOWN ********************

# ---
# 
# ## Troubleshooting Log
# 
# ### Issue: Cannot create Notebook — region mismatch error
# 
# **What I expected:** Notebook creates normally inside El Salvador Analytics workspace  
# **What happened instead:** Fabric blocked creation, prompted to create a NEW workspace instead  
# **Error message (verbatim):** "Unable to create the item in this workspace El Salvador 
# Analytics because your org's free Fabric trial capacity is not in the same region as 
# this workspace's capacity."  
# **Diagnosis steps:**
# 1. Recognized the dialog was offering to create a new workspace, not the notebook I wanted
# 2. Identified likely cause from error text: capacity region mismatch
# 3. Checked Workspace settings → Workspace type to confirm assigned capacity
# 
# **Root cause:** Workspace type was set to "Power BI Pro" — not assigned to any Fabric 
# capacity at all (trial or otherwise). Notebooks require Fabric capacity; Pro licensing 
# alone isn't sufficient.  
# **Fix:** Workspace settings → Workspace type → Edit → reassigned to Fabric Trial 
# (SKU FTL4, Region: East US)  
# **Lesson:** Workspace creation doesn't automatically inherit Fabric trial capacity — 
# must be explicitly assigned. Check this immediately after creating any new workspace, 
# before building anything in it.
# 
# ---
# 
# ### Issue: Markdown cell rendering as raw text
# 
# **What I expected:** Header/log template would render as formatted markdown  
# **What happened instead:** Cell displayed raw `**bold**` and `##` syntax with spell-check 
# squiggles, cell was set to run as PySpark (Python)  
# **Root cause:** New notebook cells default to Code type, not Markdown  
# **Fix:** Used the cell-type toggle in the cell toolbar to convert Code → Markdown  
# **Lesson:** Always confirm cell type before typing — small thing, easy to miss.


# MARKDOWN ********************

# # Daily Progress
# **Day 1:** workspace crated, capacity issue diagnosed/fixed, Notebook log established. Next: README + Git integration

# MARKDOWN ********************

# ### Issue: GitHub option greyed out in Git integration settings
# **Date:** 2026-08-01
# 
# **What I expected:** Both Azure DevOps and GitHub selectable as Git providers
# **What happened instead:** GitHub appeared disabled/greyed out, only Azure DevOps clickable
# **Root cause:** GitHub sync must be explicitly enabled at the tenant level — 
# Admin Portal → Tenant settings → Git integration has separate toggles for 
# Azure DevOps vs. GitHub, and GitHub was off by default
# **Fix:** Enabled GitHub integration toggle in Tenant settings
# **Note:** Change takes up to 15 minutes to propagate — not instant
# **Lesson:** Not every Fabric feature is on by default, even for a personal/trial 
# tenant where I'm effectively my own admin. Worth checking Tenant settings early 
# when a feature seems unexpectedly unavailable, rather than assuming it's a 
# licensing limitation.
# 
# **To verify tomorrow:** 
# 1. Confirm GitHub toggle is still ON in Admin Portal → Tenant settings
# 2. Confirm underlying Fabric admin switch is also ON (not just Git-specific toggle)
# 3. If still greyed out: full logout/login (not just refresh), check propagation up to 30 min
# 4. Re-verify workspace is still on Fabric Trial capacity, not reverted to Pro


# MARKDOWN ********************

# ### Issue: Branch dropdown search not surfacing existing "main" branch
# **Date:** 2026-08-01
# 
# **What I expected:** Typing "main" in the branch search box would show my existing 
# default branch as a selectable option
# 
# **What happened instead:** Search returned nothing but "+ New Branch," repeatedly, 
# across two separate account connections, a hard browser refresh, and a corrected 
# repository URL
# 
# **Diagnosis steps:**
# 1. Verified GitHub PAT had correct `repo` scope and hadn't expired
# 2. Verified repository URL was clean (caught and fixed a `/tree/main` suffix error)
# 3. Deleted and fully recreated the Git connection to rule out stale caching
# 4. Confirmed via GitHub UI that only one branch (`main`) genuinely existed
# 5. As a last check, manually scrolled the branch dropdown's full list instead of 
#    relying on the search filter
# **Root cause:** The branch dropdown's search/filter functionality didn't reliably 
# match "main" as a search term, even though the branch existed and appeared fine 
# in the unfiltered scrollable list.
# **Fix:** Scrolled manually through the dropdown instead of typing into search — 
# "main" was there the whole time.
# **Lesson:** When a UI search/filter returns nothing, don't assume the underlying 
# data doesn't exist — check the raw/unfiltered list before concluding there's a 
# data or connection problem. Search boxes can have their own bugs independent of 
# the data they're searching.
# 
# 
# ### Resolution: GitHub Git integration successfully connected
# **Date:** 2026-08-02
# 
# Workspace successfully connected to GitHub repo (omdata-pro/el-salvador-analytics), 
# branch `main`, root folder. Initial sync pushed 00_Project_Log Notebook to GitHub 
# without disturbing existing README.md or LICENSE. Verified via GitHub commit 
# history — 3 commits total, no conflicts.
# 
# **Total issues resolved this session:** region mismatch → Pro vs Trial capacity → 
# GitHub toggle disabled at tenant level → accidental duplicate branch (case 
# sensitivity) → branch dropdown search bug (had to scroll manually) → repository 
# URL format error (stray /tree/main suffix). Six distinct root causes, each 
# diagnosed and fixed independently.


# MARKDOWN ********************

# ### Milestone: First Bronze pipeline complete — World Bank GDP data
# **Date:** 2026-08-02
# 
# Built and published first Dataflow Gen2 (DF_Bronze_WorldBank), pulling El Salvador 
# GDP growth data from the World Bank API (NY.GDP.MKTP.KD.ZG indicator), flattening 
# nested JSON records, trimming to Country/Year/GDP_Growth_Pct, and landing as a 
# typed Delta table (bronze_worldbank_gdp) in ElSalvador_Lakehouse. Verified via 
# Recent Runs (Succeeded, 33s) and confirmed table structure in Lakehouse Explorer. 
# 50 years of historical data (1993-2025).
# 
# **Key lesson:** The Dataflow's "Save & run" had already succeeded on an earlier 
# run before I realized it — I was searching for a separate "Publish" button that 
# wasn't the actual missing step. Learned to check Recent Runs / status bar for 
# ground truth rather than assuming a UI flow is broken just because a button isn't 
# where expected.

# MARKDOWN ********************

# ### Decisions
# **Data** 2026-08-04
# - Bronze layer will use two distinct areas with different roles:
#   - `Tables/dbo/` — the queryable Bronze Delta layer. All sources land here as typed 
#     Delta tables (via Dataflow Gen2 or notebook), regardless of ingestion method.
#   - `Files/bronze/<source>/` — raw-landing staging, used only for sources without a 
#     clean API (PNC homicide data, bitcoin.gob.sv treasury tracker). Raw files land 
#     here first, then get cleaned/typed into a Tables/dbo/ Delta table.
# - World Bank sources skip the Files staging step entirely (clean JSON API → 
#   Dataflow Gen2 → Tables/dbo/ directly), so Files/bronze/worldbank/ stays 
#   intentionally unused.
# 
# ### Progress
# - bronze_worldbank_gdp: verified working end-to-end (Tables/dbo/).
# - Started bronze_worldbank_fdi following the same Dataflow Gen2 pattern.
# - Reviewed Lakehouse folder structure; clarified Bronze layer design (see Decisions).
# 
# ### Troubleshooting
# - Initially unclear whether Files/bronze/ subfolders (worldbank, security_pnc, 
#   bitcoin_treasury) created upfront should mirror Tables/dbo/ 1:1. Resolved: they 
#   don't — Files/ is only needed for sources requiring a raw-landing step before 
#   transformation.


# MARKDOWN ********************

# ### Progress
# **Date** 2026-08-04
# - bronze_worldbank_homicide: built and landed (VC.IHR.PSRC.P5, UNODC-sourced via 
#   World Bank API). 66 rows, 2015-2025, real data only 2017-2022.
# - bronze_worldbank_fdi: built and landed (BX.KLT.DINV.CD.WD). 66 rows, matches 
#   Country/Year/[metric] schema pattern.
# - All three World Bank Bronze tables (gdp, fdi, homicide) now consistent: lowercase 
#   naming, matching column structure (Country, Year, [metric]).
# - Scouted PNC and bitcoin.gob.sv as raw sources: neither has a clean API. 
#   Documented findings (see Decisions).
# 
# ### Decisions
# - Bronze layer uses Tables/dbo/ for all typed Delta tables (API and manual 
#   sources alike); Files/bronze/<source>/ reserved for raw-landing staging on 
#   non-API sources only.
# - Homicide segmentation by gang-affiliation and feminicide will NOT be sourced 
#   via API — El Salvador stopped officially publishing this breakdown after 2022. 
#   Feminicide counts will be manually compiled from ORMUSA's monthly PDF reports 
#   into a template CSV (chosen over automated PDF-table extraction due to 
#   inconsistent PDF formatting and low monthly volume).
# - 2023-2025 annual homicide totals (missing from World Bank/UNODC data) will be 
#   manually sourced from official Gabinete de Seguridad/Fiscalía announcements, 
#   landed as a SEPARATE Bronze table (not merged into bronze_worldbank_homicide) 
#   to preserve source lineage. Blending happens at Silver layer with an explicit 
#   Source column.
# 
# ### Troubleshooting
# - FDI query was built/flattened in a prior session but never had its Lakehouse 
#   destination configured or run - caught via Lakehouse Explorer audit before 
#   moving forward. Lesson: verify each query's destination status before ending 
#   a session, not just that it's been flattened.
# - Homicide query initially landed as bronze_worldbank_homicide with capitalized 
#   query-name-as-table-name (Bronze_WorldBank_Homicide) and FDI initially landed 
#   with unrenamed Country column (value.1) - both caught via Lakehouse Explorer 
#   spot-check and corrected. 
# - Found conflicting official 2023 homicide figures: Secretaria de Comunicaciones 
#   reported 194 (Jan 2, 2024 press release) one day before Gabinete de Seguridad's 
#   formal announcement of 154 (Jan 3, 2024). Using the later, formal Gabinete 
#   figure as authoritative.


# MARKDOWN ********************

# ### Progress
# **Date** 2026-08-07
# - bronze_bitcoin_treasury_snapshot: built via CoinGecko Treasuries API 
#   (governments entity), landed in Tables/dbo. 13 rows, verified El Salvador 
#   shows 7,474.37 BTC matching public reporting.
# - bronze_bitcoin_treasury_history: manually compiled checkpoint-disclosure 
#   history (6 dated entries, 2022-2025) from public purchase announcements, 
#   loaded via Lakehouse's native "Load to Tables" file-to-table feature rather 
#   than Dataflow Gen2 (deliberate choice - file was already clean, didn't need 
#   Power Query transformation overhead).
# - Bitcoin pillar Bronze layer now complete: snapshot + history tables.
# 
# ### Decisions
# - CoinGecko's Treasuries API requires a free Demo-tier API key with 
#   attribution required; documented as a data source credit.
# - No public daily purchase ledger exists for El Salvador's Bitcoin 
#   acquisitions - built bronze_bitcoin_treasury_history as a checkpoint/
#   disclosure table (dated confirmations) rather than a true daily transaction 
#   log, with a Type column distinguishing Official vs Estimated figures.
# - Noted an unexplained gap between the Nov 2023 estimate (~2,744 BTC) and 
#   May 2024 official disclosure (5,748.76 BTC) - likely mining revenue plus 
#   accelerated DCA, but not officially bridged. Documented as a real 
#   transparency/data-availability finding rather than smoothed over.
# - Used Lakehouse's native "Load to Tables" feature for the history CSV instead 
#   of Dataflow Gen2, since the file was already clean - accepted the tradeoff 
#   of no visible Applied Steps transformation history for this one table.
# 
# ### Troubleshooting
# - CoinGecko API entity filter (entity=governments) must be a URL PATH 
#   parameter (/governments/public_treasury/bitcoin), not a query string 
#   parameter (?entity=governments) - the query param was silently ignored, 
#   returning companies data instead with no error. Found via official API docs, 
#   not the summary article.
# - Fabric's Web API connector UI did not expose an "Advanced/Headers" option as 
#   expected - worked around by editing the M code directly in the formula bar 
#   to add Web.Contents(...,[Headers=[...]]) for the API key.
# - Hit a "Token Literal expected" M syntax error twice: first from a duplicate 
#   leading "=" (formula bar already implies it), second from a missing opening 
#   bracket before Headers=. Used "Show error" to pinpoint the exact character 
#   position rather than guessing.
# - Dataflow run failed with ModelBuilderDefaultOutputDestinationQueriesWith
#   OnlyUnsupportedTypeColumns - caused by skipping the explicit "Changed column 
#   type" step before setting the Lakehouse destination. Fixed by setting types 
#   via Detect Data Type before landing.
# - Table initially landed as bronze_bitcointreasury_snapshot (missing 
#   underscore) - caught via naming consistency check, corrected, old table 
#   deleted.
# - Attempted OneLake connection via Text/CSV connector using a copied URL that 
#   turned out to be a Fabric portal link (app.fabric.microsoft.com), not a true 
#   OneLake data path - connector couldn't authenticate. Worked around using the 
#   Lakehouse's native "Load to Tables" feature instead of chasing the correct 
#   OneLake URL format.


# MARKDOWN ********************

# ## 2026-08-07 (continued)
# 
# ### Progress
# - bronze_security_annual_totals: manually compiled 2023-2025 homicide totals 
#   from official Gabinete de Seguridad/Fiscalia figures, loaded via Lakehouse's 
#   native "Load to Tables" feature. 3 rows, clean load, no debugging required.
# - Bronze layer now substantively complete across all three pillars (7 tables 
#   total): macroeconomic (GDP, FDI), security (WorldBank homicide + manual 
#   annual totals), Bitcoin (treasury snapshot + history).
# 
# ### Decisions
# - Considered adding World Bank tourism indicators (ST.INT.ARVL, ST.INT.RCPT.CD) 
#   as a 4th data thread tied to the security-turnaround narrative. Found the 
#   series stops reporting around 2020 - same lagging-data pattern as homicide. 
#   Deferred: will revisit as a manual-checkpoint table (like Bitcoin history) 
#   if the tourism/investment narrative needs 2021-2026 coverage.

# MARKDOWN ********************

# ### Progress
# **Date** 2026-08-08
# - Began Silver layer work via new Fabric Notebook (PySpark): 10_Silver_Transformations
# - Built and landed silver_security_homicide_trend: blended bronze_worldbank_homicide 
#   (1994-2022, corrected from earlier undercount - originally believed to start 2017) 
#   with bronze_security_annual_totals (2023-2025) into one continuous 32-row trend, 
#   with a Source column preserving lineage per row. This table currently sits in the 
#   wrong Lakehouse (pre-migration location) and needs to be rebuilt post-migration.
# - Created ElSalvador_02_Silver and ElSalvador_03_Gold Lakehouses (schema-enabled). 
#   Renamed original ElSalvador_Lakehouse to ElSalvador_01_Bronze (all 7 existing 
#   Bronze tables intact, unaffected by rename).
# 
# ### Decisions
# - Explored separate schemas (bronze/silver/gold) within a single Lakehouse for 
#   Silver layer organization. Found Fabric Lakehouse schema support is a 
#   creation-time-only setting with no retroactive migration path for existing 
#   Lakehouses - would require recreating and re-migrating all 7 Bronze tables.
# - Initially decided to stay with single Lakehouse + bronze_/silver_/gold_ naming 
#   prefixes (all in dbo) to avoid that rework.
# - Reconsidered and reversed that decision: adopted separate Lakehouses per 
#   medallion layer instead (Bronze/Silver/Gold as distinct Lakehouse items) - this 
#   avoids migrating existing Bronze data entirely (Bronze Lakehouse just gets 
#   renamed, tables untouched) while still achieving clean architectural separation. 
#   New Silver/Gold Lakehouses created with schema support enabled for future 
#   flexibility. This is a documented, legitimate enterprise Fabric pattern 
#   (separate-Lakehouse-per-layer), often preferred for per-layer access control.
# - Naming convention: ElSalvador_01_Bronze / _02_Silver / _03_Gold. Note: Fabric 
#   Lakehouse names cannot start with a digit (attempted 01_ElSalvador_Bronze, 
#   update failed) - number placement moved after the shared prefix instead.
# 
# ### Troubleshooting
# - Lakehouse rename to "01_ElSalvador_Bronze" failed with a DisplayName validation 
#   error - root cause identified as leading-digit restriction on Fabric item names. 
#   Resolved by moving the numeric prefix after "ElSalvador_" instead.
# 
# ### Next steps
# 1. Build 3 Central American regional comparison Bronze tables (homicide, GDP, FDI) 
#    using multi-country World Bank query (SV;GT;HN;NI;CR;PA;BZ) in DF_Bronze_WorldBank, 
#    landing in ElSalvador_01_Bronze as bronze_worldbank_homicide_regional, 
#    _gdp_regional, _fdi_regional.
# 2. Migrate 10_Silver_Transformations: attach ElSalvador_02_Silver, rebuild and 
#    rewrite silver_security_homicide_trend to the correct Lakehouse, delete the 
#    misplaced copy.
# 3. Continue Silver layer: silver_macro_trend (GDP+FDI join) and Bitcoin pillar 
#    Silver tables.


# MARKDOWN ********************

# ## Progress
# 
# **Date** 2026-08-11
# 
# - Built 3 Central American regional comparison Bronze tables in DF_Bronze_WorldBank: bronze_worldbank_gdp_regional, bronze_worldbank_fdi_regional, bronze_worldbank_homicide_regional. Method: duplicated each existing single-country query and adapted the URL/destination rather than building from scratch, to reuse proven flatten logic.
# - All 3 landed successfully in ElSalvador_01_Bronze/dbo, ~462 rows each, covering El Salvador, Guatemala, Honduras, Nicaragua, Costa Rica, Panama, and Belize.
# 
# ## Troubleshooting
# 
# - **Silent row truncation on GDP regional** - Source URL was missing &per_page=1000, and the World Bank API's default of 50 rows/page happened to exactly match one country's history, so the query silently returned only Belize's data with no error. Fixed by adding &per_page=1000 to the Source step URL.
# - **Inconsistent formats across existing queries** - bronze_worldbank_gdp uses ISO3 country codes (SLV) while bronze_worldbank_fdi and bronze_worldbank_homicide use ISO2 (SV), with per_page defaults of 500 vs 100 respectively. Had to check each query's existing URL individually before editing rather than assuming a shared format.
# - **Duplicated queries publish with no data destination** - Power Query's Duplicate action copies all transformation steps but not the Lakehouse destination, so the first Save & run on GDP regional completed with no error but wrote nothing. Fixed by explicitly configuring Data destination > Lakehouse > ElSalvador_01_Bronze/dbo on each new query before running.
# - **Cosmetic connection-name truncation warning** on each new Web source URL - not blocking, resolved by renaming.
# 
# ## Decisions
# 
# - Adopted Capitalized_Underscore as the naming convention for Dataflow Gen2 connection names (e.g. WorldBank_Homicide_Regional_API), reusing one connection across related queries where the domain is the same rather than creating a new one per query.


# MARKDOWN ********************

# # Progress
# 
# **Date** 2026-08-12
# 
# - Reattached 10_Silver_Transformations to ElSalvador_01_Bronze and ElSalvador_02_Silver (found via OneLake catalog search, since the notebook's Add data items menu doesn't list existing Lakehouses directly - had to distinguish the actual Lakehouse from its auto-created same-named SQL analytics endpoint by icon/tooltip).
# - Rebuilt silver_security_homicide_trend in the correct location by fully qualifying the write path (ElSalvador_02_Silver.dbo.silver_security_homicide_trend) instead of a bare table name, then re-running the full notebook top to bottom since a fresh session had cleared previously defined DataFrame variables. Confirmed 32 rows, 1994-2025, with lineage Source column intact.
# - Deleted the misplaced silver_security_homicide_trend copy that was sitting in ElSalvador_01_Bronze from before the migration. Bronze now holds exactly 10 clean tables (7 original + 3 regional), no Silver tables mixed in.
# - Built silver_regional_comparison: one combined table (Country, Year, GDP_Growth_Pct, FDI_USD, Homicide_Rate_Per100k) outer-joining the 3 regional Bronze tables on Country/Year, chosen over 3 separate Silver tables since Silver's job is to make the downstream Gold/Power BI join once rather than push it further down the pipeline. Published successfully - 462 rows, correctly surfacing coverage gaps as nulls (e.g. Belize's FDI/homicide data starting later than its GDP data).
# 
# # Troubleshooting
# 
# - **Notebook write cell used a bare table name** - saveAsTable("silver_security_homicide_trend") had no Lakehouse prefix, so it wrote to whichever Lakehouse was "default" at runtime, landing in the wrong (pre-migration) location originally. Fixed by fully qualifying all saveAsTable() calls as "ElSalvador_02_Silver.dbo.<table>" going forward.
# - **Fresh notebook session clears variables** - re-running only the write cell after a session reset threw NameError since the DataFrames built in earlier cells no longer existed in memory. Fixed with Run all to rebuild the full chain before writing.
# - **Recurring paste bug**: pasting multi-line PySpark code into notebook cells repeatedly collapsed line breaks, merging separate statements onto the same line and causing SyntaxErrors. Worked around by writing statements as a single line joined with semicolons instead of relying on line breaks.
# 
# # Decisions
# 
# - Structured the regional Silver-layer work as one combined silver_regional_comparison table rather than three separate Silver tables mirroring the Bronze regional tables, to keep the country/year join logic centralized in Silver rather than repeated downstream.


# MARKDOWN ********************

# # Progress
# 
# **Date** 2026-08-13
# 
# - Built silver_macro_trend: joined bronze_worldbank_gdp + bronze_worldbank_fdi for El Salvador only, on Country/Year, outer join. Published to ElSalvador_02_Silver/dbo - 66 rows. Row count implies GDP/FDI actually span 1960-2025 rather than the 1996-2025 assumed in earlier notes, consistent with the pattern of other date-range corrections already documented in this log (e.g. the homicide indicator).
# - Decided to structure the Bitcoin pillar as one combined silver_bitcoin_treasury table rather than two separate Silver tables.
# - Built silver_bitcoin_treasury: unified bronze_bitcoin_treasury_snapshot (13 governments, current point-in-time, from CoinGecko) and bronze_bitcoin_treasury_history (6 dated El Salvador checkpoints, manually compiled) into one schema (Country, Record_Type, Date, BTC_Holdings, Value_USD, Pct_Of_Total_Supply, Source, Notes) using unionByName, since the two sources have different grains and no shared join key. Published to ElSalvador_02_Silver/dbo - 19 rows.
# - Silver layer is now fully complete: silver_security_homicide_trend, silver_regional_comparison, silver_macro_trend, and silver_bitcoin_treasury all confirmed live in ElSalvador_02_Silver/dbo.
# 
# # Troubleshooting
# 
# - **Recurring notebook paste bug persisted across sessions** - even previously-working cells (from last session) reverted to broken multi-line syntax after a Run all/reload, throwing SyntaxErrors on code that had already been fixed once. Confirmed this is a persistent editor/browser quirk, not a one-off mistake. Standing fix: type statements as a single unbroken line joined with semicolons rather than relying on line breaks, and avoid Run all on this notebook - run cells individually instead, since Run all tends to trigger the bug across multiple cells at once.
# - **NameError from skipped cells** - hit `name 'silver_macro' is not defined` because the join cell that actually creates the DataFrame had never been added/run, only the read and count cells existed. Lesson: when a NameError appears, check whether the defining cell was skipped entirely, not just whether the notebook needs a full re-run.
# - Confirmed `.mode("overwrite")` on writes is safe to re-run - it replaces the table's full contents each time rather than appending, so re-running earlier cells (intentionally or while troubleshooting) does not create duplicate rows.
# 
# # Decisions
# 
# - Structured the Bitcoin pillar Silver table as a union with a unified schema (Country/Record_Type/Date/BTC_Holdings/Value_USD/Pct_Of_Total_Supply/Source/Notes) rather than a join, since snapshot and history data have fundamentally different grains (cross-sectional current state vs. longitudinal single-country history).


# MARKDOWN ********************

# # Progress
# 
# **Date** 2026-08-14
# 
# - Created new notebook 20_Gold_Aggregations, attached to ElSalvador_02_Silver (read source) and ElSalvador_03_Gold (write destination) via OneLake catalog search.
# - Built gold_security_trend, gold_macro_trend, gold_bitcoin_treasury, and gold_regional_comparison as straight pass-throughs of the 4 corresponding Silver tables, using fully-qualified saveAsTable() paths from the start this time.
# - Built gold_kpi_summary: extracted the latest non-null value per headline metric across all 4 pillars into a single 4-row summary table for Power BI KPI cards - Homicide Rate 1.9/100k (2024), GDP Growth 3.9% (2025), FDI Net Inflows ~$763.7M (2025), Bitcoin Treasury 7,474.37 BTC (current).
# - Confirmed all 5 Gold tables live in ElSalvador_03_Gold/dbo. Full Bronze -> Silver -> Gold pipeline now complete across all 3 pillars plus the regional comparison layer.
# 
# # Troubleshooting
# 
# - Same recurring notebook paste bug encountered again on new cells this session; continued using the single-line-with-semicolons workaround and running cells individually rather than Run all.
# - Hit a NameError building gold_kpi_summary when referencing DataFrames from earlier cells after a session gap; resolved by re-running the defining read/write cells before the aggregation cell.
# 
# # Decisions
# 
# - Set a working process for future sessions: when a session runs long or approaches time/context limits, proactively produce a portable handoff prompt with full project context, current status, and next steps, so the project can continue without interruption. 9 days remained on Fabric trial capacity as of this session.


# MARKDOWN ********************

# # Progress
# 
# **Date** 2026-08-15
# 
# - Exported all 5 Gold tables to CSV directly from 20_Gold_Aggregations using a loop with toPandas().to_csv() into the Lakehouse Files area, as a safeguard against Fabric trial capacity expiring and to support a planned parallel Tableau Public rebuild.
# - Downloaded all 5 CSVs locally (gold_bitcoin_treasury, gold_kpi_summary, gold_macro_trend, gold_regional_comparison, gold_security_trend) via the Lakehouse's own Files browser.
# - Generated a full project handoff document covering architecture, pipeline status, recurring technical issues, and a detailed Power BI semantic layer plan (star-schema relationships, dim_year table, pillar-specific DAX measures, KPI card setup, report structure, fintech-dark design direction) to keep the project portable across sessions/tools.
# - Began Power BI planning: confirmed working in Power BI Service (web, inside Fabric) rather than Desktop. Cross-checked planned DAX measures with a second AI's review and corrected three issues before implementation: Latest Homicide Rate needed to select the latest year with non-blank data rather than the table's overall max year (2025 has no rate yet); Bitcoin checkpoint growth needed to be calculated by first/latest date rather than MIN/MAX of the holdings value directly; and the regional homicide ranking needed to use the latest year containing homicide data rather than the table's overall max year.
# 
# # Troubleshooting
# 
# - The right-click Download option for exported CSVs was missing/inconsistent depending on which Lakehouse's Files view was used to navigate to it (via a notebook's Explorer panel vs. the Lakehouse item directly). Resolved by opening the Lakehouse item directly and using its own Files browser, where Download reliably appeared.
# 
# # Decisions
# 
# - Confirmed gold_bitcoin_treasury needs two Power Query fixes before building Bitcoin measures: standardizing the inconsistent Country values (ISO2 codes on snapshot rows vs. full country names on history rows) to one format, and converting the Date column from text to a proper Date type.
# - Adopted a semantic model plan with dim_year related only to the three yearly-grain Gold tables (security, macro, regional); gold_bitcoin_treasury stays on its own date grain; gold_kpi_summary stays unrelated/standalone as the Overview page's KPI card source.
# - Confirmed sequencing for the Power BI build: connect the 5 Gold tables, clean the Bitcoin country/date columns, build dim_year and relationships, build a dedicated Measures table, then build the Overview page before the pillar-specific pages.


# MARKDOWN ********************

# # Progress
# 
# **Date** 2026-08-16
# 
# * Reviewed the completed Gold layer before beginning Power BI and identified a semantic issue in `gold_bitcoin_treasury`: the source contained national, state, and municipal government entities sharing the same country code, while the Silver transformation had dropped the source `Name` field.
# * Updated the Bitcoin Silver transformation to preserve and standardize `Entity_Name`, `Country_Code`, `Country_Name`, and `Government_Level`; classified United States as National, Texas as State, and Roswell, New Mexico as Municipal.
# * Converted the Bitcoin historical `Date` field from string to a proper date type while intentionally retaining null dates for current Snapshot rows, since the CoinGecko source does not provide an as-of date.
# * Preserved the mixed-grain Bitcoin architecture: 13 current government Snapshot records plus 6 dated El Salvador Official/Estimated treasury checkpoints, separated through `Record_Type`.
# * Validated the corrected Bitcoin DataFrame before saving: 19 total rows, date data type confirmed, zero missing country names, 11 National Snapshot/history groups plus the expected State and Municipal Snapshot records.
# * Overwrote `ElSalvador_02_Silver.dbo.silver_bitcoin_treasury` with the corrected schema and regenerated `ElSalvador_03_Gold.dbo.gold_bitcoin_treasury` using `overwriteSchema`.
# * Updated the Gold KPI extraction logic to filter El Salvador’s national Snapshot using `Country_Code = "SV"`, `Country_Name = "El Salvador"`, `Government_Level = "National"`, and `Record_Type = "Snapshot"`.
# * Rebuilt and validated `gold_kpi_summary`: Homicide Rate 1.9/100k (2024), GDP Growth 3.9059% (2025), FDI Net Inflows $763,722,779.22 (2025), and Bitcoin Treasury 7,474.37 BTC (current).
# * Re-exported all 5 Gold tables to CSV and downloaded the refreshed files into the local Tableau CSVs folder.
# * Created Direct Lake on OneLake semantic model `ElSalvador_Analytics_Model` from the 5 Gold tables: `gold_security_trend`, `gold_macro_trend`, `gold_bitcoin_treasury`, `gold_regional_comparison`, and `gold_kpi_summary`.
# * Created `dim_year` with unique values from 1960–2025 and added 3 active many-to-one, single-direction relationships to the Year columns in the Security, Macro, and Regional Comparison Gold tables.
# * Created centralized `Analytics_Measures` table, hid its technical Placeholder column, and organized report measures with documented descriptions, display folders, data formats, and hidden helper measures.
# * Built and configured 14 DAX measures across the four analytical pillars:
# 
#   * Security: Latest Homicide Year, Latest Homicide Rate, and Homicide Rate Change Since 2015.
#   * Macroeconomics: Latest GDP Growth Year, Latest GDP Growth %, Latest FDI Year, Latest FDI (USD), and FDI 5-Year Average (USD).
#   * Bitcoin Treasury: Current BTC Holdings (El Salvador) and BTC Holdings Growth (First to Latest).
#   * Regional Comparison: Latest Regional Homicide Comparison Year, El Salvador Regional Homicide Rank, Latest Regional GDP Comparison Year, and Regional Average GDP Growth (Excl. El Salvador).
# * Ran a consolidated DAX QA query across all 14 measures. Confirmed: latest homicide rate 1.9 in 2024; approximately 98% reduction since 2015; GDP growth 3.91 in 2025; latest FDI $763.7M; 5-year FDI average $683.9M; current Bitcoin holdings 7,474.37 BTC; Bitcoin growth approximately 225%; regional homicide comparison year 2022 with El Salvador ranked #1; and 2025 regional GDP average of 4.1 excluding El Salvador.
# * Prepared documentation descriptions for all 5 Gold tables; adding them and the key column descriptions in Model view is the next semantic-layer documentation step.
# 
# # Troubleshooting
# 
# * Encountered a `NameError` for `df_btc_snapshot` after a Spark session reset cleared in-memory variables. Resolved by reloading both Bronze Bitcoin tables through fully qualified `spark.table()` paths before rerunning the corrected transformation cells.
# * Hit Fabric HTTP 430 `TooManyRequestsForCapacity` when the Gold notebook attempted to start while the Silver notebook’s Spark session was still active. Resolved by running `notebookutils.session.stop()` in the Silver notebook, waiting for capacity release, and rerunning only the affected Gold cell.
# * Accidentally reran the CSV export loop before refreshing the Gold Bitcoin table. No table data was changed; reran the export after the Gold and KPI tables were correctly updated.
# * Attempted to run the Gold KPI save cell before recreating `gold_kpi_summary` in the current Spark session, resulting in a `NameError`. Resolved by rerunning the KPI source-row and DataFrame-building cells before the persistent save.
# * Confirmed that `/lakehouse/default/Files/` resolved to `ElSalvador_02_Silver/Files` because Silver is the default Lakehouse attached to `20_Gold_Aggregations`. The exports were valid and downloaded successfully; this behavior will be documented for future reruns.
# * Fabric rejected `Measures` as a reserved calculated-table name. Renamed the centralized measure table to `Analytics_Measures`.
# * The Bitcoin growth DAX initially failed because `FirstDate` conflicted with the DAX `FIRSTDATE()` function name. Resolved by renaming the variables to `FirstCheckpointDateValue`, `LatestCheckpointDateValue`, `FirstCheckpointHoldings`, and `LatestCheckpointHoldings`.
# * The Fabric model canvas appeared grayed out while the invalid Bitcoin measure remained open in DAX edit mode. Recovered by canceling the invalid edit and replacing the formula with the corrected version.
# * The DAX QA view initially displayed the sample `gold_kpi_summary` query as Result 1 of 2. Switched to Result 2 of 2 to validate the consolidated measure output.
# 
# # Decisions
# 
# * Corrected the Bitcoin schema in Silver rather than Power Query or semantic-model calculated columns. This preserves the medallion architecture: Bronze remains raw, Silver handles standardization and data quality, and Gold remains report-ready for Direct Lake.
# * Retained the unified Bitcoin table because Snapshot and historical data support related treasury analysis, but documented that they have different grains and must be separated using explicit `Record_Type` filters.
# * Preserved Texas and Roswell, New Mexico as legitimate CoinGecko records rather than aggregating them into the U.S. federal figure. Added `Government_Level` so national-government comparisons can explicitly filter to National records.
# * Kept Snapshot dates null because CoinGecko does not provide an as-of date. Adding a separately captured `Snapshot_As_Of` extraction date remains a potential future enhancement.
# * Adopted Direct Lake on OneLake for the semantic model so Power BI reads the Gold Delta tables directly without an Import refresh process.
# * Related `dim_year` only to the three annual-grain tables. `gold_bitcoin_treasury` remains on its independent Date grain, and `gold_kpi_summary` remains disconnected.
# * Retained `gold_kpi_summary` as the source for fixed, validated Overview-page KPI cards. Separate DAX measures support analytical pages and more advanced comparisons.
# * Centralized all measures in `Analytics_Measures`, organized them by pillar and purpose through display folders, and hid technical helper measures after their dependent measures were completed.
# * Stored GDP growth fields as decimal numbers rather than Power BI percentages because the source already contains percentage-point values such as 3.9. Applied Percentage formatting only to derived ratio measures such as homicide-rate change and Bitcoin-holdings growth.
# * Defined latest-year headline measures to ignore year filters for consistent portfolio KPIs. Regional comparison years are selected based on the latest year in which El Salvador has nonblank data, preventing invalid rankings against years where El Salvador is absent.
# * Set the next checkpoint as completing Gold table/key-column descriptions and configuration, then creating and validating the Overview report page before building the Security, Macroeconomic, Bitcoin Treasury, and Regional Comparison pages.

