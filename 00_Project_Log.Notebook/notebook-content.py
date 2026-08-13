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

