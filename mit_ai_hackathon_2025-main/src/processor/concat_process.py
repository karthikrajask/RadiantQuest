



# #############################################################################
# IMPORTS
# #############################################################################
import pandas as pd



# #############################################################################
# MAIN
# #############################################################################

main_df = pd.read_csv("../../processed_data/data/template_data.csv")
df1 = pd.read_csv("../../data/processed_data/company_azure_power_projects_processed.csv")
df2 = pd.read_csv("../../data/processed_data/company_renew_projects_processed.csv")
df3 = pd.read_csv("../../data/processed_data/company_tata_projects_processed.csv")
main_df = pd.concat([main_df, df1, df2, df3], ignore_index=True)
main_df.to_csv("../../data/processed_data/data_processed.csv", index=False)
