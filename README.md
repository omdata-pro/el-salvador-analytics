# El Salvador Analytics: Security, Economy & Bitcoin Transformation

## Overview
A data analytics case study examining El Salvador's national transformation 
(2015–2026) across three interconnected pillars: public security, macroeconomic 
growth, and the national Bitcoin adoption strategy. The project asks a central 
question: how did one government's centralized approach to security policy and 
monetary policy reshape the country's trajectory — and what does the data reveal 
about the trade-offs behind that transformation?

## Motivation
El Salvador has undergone one of the most dramatic security turnarounds in the 
Western Hemisphere, alongside a globally unprecedented experiment adopting Bitcoin 
as legal tender (later reversed in 2025 under IMF pressure). This project brings 
together security, economic, and blockchain data to tell that story with evidence 
— including the parts often left out of the simpler "success story" narrative.

## Data Sources
- **Security:** Policía Nacional Civil (PNC) homicide statistics, UNODC Global 
  Study on Homicide
- **Economic:** World Bank Open Data (GDP, FDI, poverty, unemployment), IMF Data
- **Bitcoin:** bitcoin.gob.sv treasury tracker, on-chain blockchain data

## Architecture & Tech Stack
- **Microsoft Fabric** — Lakehouse (OneLake), Dataflow Gen2, Data Warehouse
- **Medallion architecture** — Bronze (raw) → Silver (cleaned) → Gold (modeled)
- **Power BI** — semantic model, DAX measures, report/dashboard
- **Git integration** — version-controlled via GitHub

## Key KPIs
- Homicide rate per 100k, YoY % change
- GDP growth, FDI inflows, remittances (% of GDP)
- Bitcoin holdings (BTC + USD value), unrealized P/L over time

## Project Status
🚧 In development — started 2026-07-30

## Documentation
Full build log, architecture decisions, and troubleshooting notes are maintained 
in-platform via a Fabric Notebook (`00_Project_Log`), version-controlled alongside 
the project.

## Author
Orquidea Mohammed  
[LinkedIn](https://www.linkedin.com/in/orquidea-mohammed/) · [Portfolio](https://orquideamohammed.wixsite.com/portfolio)
