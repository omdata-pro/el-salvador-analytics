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

