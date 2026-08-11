[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"], DestinationTypeSettings = [Kind = "Table"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Query_DataDestination", IsNewTarget = true], Settings = [Kind = "Manual", AllowCreation = true, ColumnSettings = [Mappings = {[SourceColumnName = "Country", DestinationColumnName = "Country"], [SourceColumnName = "Year", DestinationColumnName = "Year"], [SourceColumnName = "GDP_Growth_Pct", DestinationColumnName = "GDP_Growth_Pct"]}], DynamicSchema = true, UpdateMethod = [Kind = "Replace"], TypeSettings = [Kind = "Table"]]]}]
shared bronze_worldbank_gdp = let
  Source = Json.Document(Web.Contents("https://api.worldbank.org/v2/country/SLV/indicator/NY.GDP.MKTP.KD.ZG?format=json")),
  #"Converted to table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  Navigation = #"Converted to table"{1}[Column1],
  #"Converted to table 1" = Table.FromList(Navigation, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to table 1", "Column1", {"indicator", "country", "countryiso3code", "date", "value", "unit", "obs_status", "decimal"}, {"Column1.indicator", "Column1.country", "Column1.countryiso3code", "Column1.date", "Column1.value", "Column1.unit", "Column1.obs_status", "Column1.decimal"}),
  #"Expanded Column1.indicator" = Table.ExpandRecordColumn(#"Expanded Column1", "Column1.indicator", {"id", "value"}, {"Column1.indicator.id", "Column1.indicator.value"}),
  #"Expanded Column1.country" = Table.ExpandRecordColumn(#"Expanded Column1.indicator", "Column1.country", {"id", "value"}, {"Column1.country.id", "Column1.country.value"}),
  #"Renamed columns" = Table.RenameColumns(#"Expanded Column1.country", {{"Column1.country.value", "Country"}, {"Column1.date", "Year"}, {"Column1.value", "GDP_Growth_Pct"}}),
  #"Removed columns" = Table.RemoveColumns(#"Renamed columns", {"Column1.indicator.id", "Column1.indicator.value", "Column1.country.id", "Column1.countryiso3code", "Column1.unit", "Column1.obs_status", "Column1.decimal"}),
  #"Changed column type" = Table.TransformColumnTypes(#"Removed columns", {{"Country", type text}, {"Year", Int64.Type}, {"GDP_Growth_Pct", type number}})
in
  #"Changed column type";
shared Query_DataDestination = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "54e503e8-ffac-4107-9d85-2a67491b6def"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "4655e07e-cb64-4682-9fba-394ce86b8a98"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "bronze_worldbank_gdp", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared DefaultDestination = let
  Source = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  #"Navigation 1" = Source{[workspaceId = "54e503e8-ffac-4107-9d85-2a67491b6def"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[lakehouseId = "4655e07e-cb64-4682-9fba-394ce86b8a98"]}[Data],
  #"Navigation 3" = #"Navigation 2"{[Id = "dbo", ItemKind = "Schema"]}[Data]
in
  #"Navigation 3";
[BindToDefaultDestination = true]
shared bronze_worldbank_homicide = let
  Source = Json.Document(Web.Contents("https://api.worldbank.org/v2/country/SV/indicator/VC.IHR.PSRC.P5?format=json&per_page=100")),
  #"Converted to table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  Navigation = #"Converted to table"{1}[Column1],
  #"Converted to table 1" = Table.FromList(Navigation, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to table 1", "Column1", {"country", "countryiso3code", "date", "value"}, {"country", "countryiso3code", "date", "value"}),
  #"Expanded country" = Table.ExpandRecordColumn(#"Expanded Column1", "country", {"id", "value"}, {"id", "value.1"}),
  #"Removed columns" = Table.RemoveColumns(#"Expanded country", {"id", "countryiso3code"}),
  #"Renamed columns" = Table.RenameColumns(#"Removed columns", {{"value.1", "Country"}, {"date", "Year"}, {"value", "Homicide_Rate_Per100k"}}),
  #"Changed column type" = Table.TransformColumnTypes(#"Renamed columns", {{"Year", Int64.Type}, {"Homicide_Rate_Per100k", type number}, {"Country", type text}})
in
  #"Changed column type";
[BindToDefaultDestination = true]
shared bronze_worldbank_fdi = let
  Source = Json.Document(Web.Contents("https://api.worldbank.org/v2/country/SV/indicator/BX.KLT.DINV.CD.WD?format=json&per_page=100")),
  #"Converted to table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  Navigation = #"Converted to table"{1}[Column1],
  #"Converted to table 1" = Table.FromList(Navigation, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to table 1", "Column1", {"country", "countryiso3code", "date", "value"}, {"country", "countryiso3code", "date", "value"}),
  #"Expanded country" = Table.ExpandRecordColumn(#"Expanded Column1", "country", {"id", "value"}, {"id", "value.1"}),
  #"Removed other columns" = Table.SelectColumns(#"Expanded country", {"id", "value.1", "countryiso3code", "date", "value"}),
  #"Removed columns" = Table.RemoveColumns(#"Removed other columns", {"id"}),
  #"Renamed columns" = Table.RenameColumns(#"Removed columns", {{"date", "Year"}, {"value", "FDI_USD"}}),
  #"Removed columns 1" = Table.RemoveColumns(#"Renamed columns", {"countryiso3code"}),
  #"Changed column type" = Table.TransformColumnTypes(#"Removed columns 1", {{"Year", Int64.Type}, {"value.1", type text}, {"FDI_USD", type number}}),
  #"Renamed columns 1" = Table.RenameColumns(#"Changed column type", {{"value.1", "Country"}})
in
  #"Renamed columns 1";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "bronze_worldbank_gdp_regional_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared bronze_worldbank_gdp_regional = let
  Source = Json.Document(Web.Contents("https://api.worldbank.org/v2/country/SLV;GTM;HND;NIC;CRI;PAN;BLZ/indicator/NY.GDP.MKTP.KD.ZG?format=json&per_page=1000")),
  #"Converted to table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  Navigation = #"Converted to table"{1}[Column1],
  #"Converted to table 1" = Table.FromList(Navigation, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to table 1", "Column1", {"indicator", "country", "countryiso3code", "date", "value", "unit", "obs_status", "decimal"}, {"Column1.indicator", "Column1.country", "Column1.countryiso3code", "Column1.date", "Column1.value", "Column1.unit", "Column1.obs_status", "Column1.decimal"}),
  #"Expanded Column1.indicator" = Table.ExpandRecordColumn(#"Expanded Column1", "Column1.indicator", {"id", "value"}, {"Column1.indicator.id", "Column1.indicator.value"}),
  #"Expanded Column1.country" = Table.ExpandRecordColumn(#"Expanded Column1.indicator", "Column1.country", {"id", "value"}, {"Column1.country.id", "Column1.country.value"}),
  #"Renamed columns" = Table.RenameColumns(#"Expanded Column1.country", {{"Column1.country.value", "Country"}, {"Column1.date", "Year"}, {"Column1.value", "GDP_Growth_Pct"}}),
  #"Removed columns" = Table.RemoveColumns(#"Renamed columns", {"Column1.indicator.id", "Column1.indicator.value", "Column1.country.id", "Column1.countryiso3code", "Column1.unit", "Column1.obs_status", "Column1.decimal"}),
  #"Changed column type" = Table.TransformColumnTypes(#"Removed columns", {{"Country", type text}, {"Year", Int64.Type}, {"GDP_Growth_Pct", type number}})
in
  #"Changed column type";
shared bronze_worldbank_gdp_regional_DataDestination = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "54e503e8-ffac-4107-9d85-2a67491b6def"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "4655e07e-cb64-4682-9fba-394ce86b8a98"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "bronze_worldbank_gdp_regional", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
[BindToDefaultDestination = true]
shared bronze_worldbank_fdi_regional = let
  Source = Json.Document(Web.Contents("https://api.worldbank.org/v2/country/SV;GT;HN;NI;CR;PA;BZ/indicator/BX.KLT.DINV.CD.WD?format=json&per_page=1000")),
  #"Converted to table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  Navigation = #"Converted to table"{1}[Column1],
  #"Converted to table 1" = Table.FromList(Navigation, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to table 1", "Column1", {"country", "countryiso3code", "date", "value"}, {"country", "countryiso3code", "date", "value"}),
  #"Expanded country" = Table.ExpandRecordColumn(#"Expanded Column1", "country", {"id", "value"}, {"id", "value.1"}),
  #"Removed other columns" = Table.SelectColumns(#"Expanded country", {"id", "value.1", "countryiso3code", "date", "value"}),
  #"Removed columns" = Table.RemoveColumns(#"Removed other columns", {"id"}),
  #"Renamed columns" = Table.RenameColumns(#"Removed columns", {{"date", "Year"}, {"value", "FDI_USD"}}),
  #"Removed columns 1" = Table.RemoveColumns(#"Renamed columns", {"countryiso3code"}),
  #"Changed column type" = Table.TransformColumnTypes(#"Removed columns 1", {{"Year", Int64.Type}, {"value.1", type text}, {"FDI_USD", type number}}),
  #"Renamed columns 1" = Table.RenameColumns(#"Changed column type", {{"value.1", "Country"}})
in
  #"Renamed columns 1";
[BindToDefaultDestination = true]
shared bronze_worldbank_homicide_regional = let
  Source = Json.Document(Web.Contents("https://api.worldbank.org/v2/country/SV;GT;HN;NI;CR;PA;BZ/indicator/VC.IHR.PSRC.P5?format=json&per_page=1000")),
  #"Converted to table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  Navigation = #"Converted to table"{1}[Column1],
  #"Converted to table 1" = Table.FromList(Navigation, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to table 1", "Column1", {"country", "countryiso3code", "date", "value"}, {"country", "countryiso3code", "date", "value"}),
  #"Expanded country" = Table.ExpandRecordColumn(#"Expanded Column1", "country", {"id", "value"}, {"id", "value.1"}),
  #"Removed columns" = Table.RemoveColumns(#"Expanded country", {"id", "countryiso3code"}),
  #"Renamed columns" = Table.RenameColumns(#"Removed columns", {{"value.1", "Country"}, {"date", "Year"}, {"value", "Homicide_Rate_Per100k"}}),
  #"Changed column type" = Table.TransformColumnTypes(#"Renamed columns", {{"Year", Int64.Type}, {"Homicide_Rate_Per100k", type number}, {"Country", type text}})
in
  #"Changed column type";
