[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"], DestinationTypeSettings = [Kind = "Table"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[BindToDefaultDestination = true]
shared bronze_bitcoin_treasury_snapshot = let
  Source = Json.Document(Web.Contents("https://api.coingecko.com/api/v3/governments/public_treasury/bitcoin", [Headers=[#"x-cg-demo-api-key"="CG-Nv1r4grPmtGMNaxqNJV1gdzv"]])),
  Navigation = Source[governments],
  #"Converted to table" = Table.FromList(Navigation, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to table", "Column1", {"name", "symbol", "country", "total_holdings", "total_entry_value_usd", "total_current_value_usd", "percentage_of_total_supply"}, {"name", "symbol", "country", "total_holdings", "total_entry_value_usd", "total_current_value_usd", "percentage_of_total_supply"}),
  #"Renamed columns" = Table.RenameColumns(#"Expanded Column1", {{"total_holdings", "BTC_Holdings"}, {"total_current_value_usd", "Current_Value_USD"}, {"percentage_of_total_supply", "Pct_Of_Total_Supply"}}),
  #"Removed columns" = Table.RemoveColumns(#"Renamed columns", {"symbol"}),
  #"Renamed columns 1" = Table.RenameColumns(#"Removed columns", {{"total_entry_value_usd", "Entry_Value_USD"}, {"name", "Name"}, {"country", "Country"}}),
  #"Changed column type" = Table.TransformColumnTypes(#"Renamed columns 1", {{"Name", type text}, {"Country", type text}, {"BTC_Holdings", type number}, {"Entry_Value_USD", type number}, {"Current_Value_USD", type number}, {"Pct_Of_Total_Supply", type number}})
in
  #"Changed column type";
shared DefaultDestination = let
  Source = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  #"Navigation 1" = Source{[workspaceId = "54e503e8-ffac-4107-9d85-2a67491b6def"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[lakehouseId = "4655e07e-cb64-4682-9fba-394ce86b8a98"]}[Data],
  #"Navigation 3" = #"Navigation 2"{[Id = "dbo", ItemKind = "Schema"]}[Data]
in
  #"Navigation 3";
