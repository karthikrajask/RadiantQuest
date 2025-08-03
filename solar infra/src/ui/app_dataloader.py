"""
"Mr Sunshine India" - "Solar Detective: Mapping India’s Solar Infrastructure Using Agentic AI"
-------------------------------------------
Authors:        Kevin Riehl <kriehl@ethz.ch>, Shaimaa El-Baklish <shaimaa.elbaklish@ivt.baug.ethz.ch>
Organization:   ETH Zürich, Institute for Transportation Planning and Systems
Development:    2025
Submitted to:   MIT Global AI Hackathon 2025, 
                Track 01: Agentic AI for Dataset Building
                Challenge 02: "Solar Detective: Mapping India’s Solar Infrastructure Using Agentic AI"
-------------------------------------------
This script contains functions for loading data.
"""




# #############################################################################
# IMPORTS
# #############################################################################
import pandas as pd
import streamlit as st




# #############################################################################
# DATA LOADING
# #############################################################################    

def load_investment_data():
    investment_data = pd.read_excel("../../data/processed_data/national_statistics.xlsx", header=1)
    investment_data_columns = ['Installed Capacity [loc]', 'Installed Capacity [dec]',
           'Hydro', 'Nuclear', 'RES', 'Thermal', 'Central', 'Private', 'State.1',
           'Rooftop Solar Capacity', 'Generation', 'Peak Demand',
           'Electricity Sales', 'AT&C Losses', 'ACS-ARR (Electricity Sales) Gap',
           'GDP [ConstPrice]', 'GDP [CurrPrice]', 'SectoralGVA [ConstPrice]',
           'SectoralGVA [CurrPrice]', 'Population', 'IncomePerCapita [CurrPrice]',
           'IncomePerCapita [ConstPrice]', 'NO2', 'SO2', 'PMO', 'PM25']
    # Convert Datatype to Float
    investment_data = investment_data[1:]
    for col in investment_data_columns:
        investment_data[col] = investment_data[col].astype(float)

    # Calculate Air Pollution
    investment_data["AQI"] = investment_data["NO2"]+investment_data["SO2"]+investment_data["PMO"]+investment_data["PM25"]    

    # Select Relevant Rows
    investment_data_india = investment_data.iloc[0]
    investment_data = investment_data.iloc[1:]
        
    # Fill Gaps / NAN Values with Weight of national average
    cols_to_fill = [col for col in investment_data.columns if col != 'State']
    india_population = investment_data_india['Population']
    for col in cols_to_fill:
        # Get the all-India value for this column
        india_value = investment_data_india[col]
        # For each row where the value is NaN, fill with scaled value
        mask = investment_data[col].isna()
        # Only scale if india_value is not nan
        if not pd.isna(india_value):
            scaled_value = india_value * investment_data.loc[mask, 'Population'] / india_population
            investment_data.loc[mask, col] = scaled_value
            
    # Fix 'Dadra and Nagar Haveli' and 'Daman and Diu' Issue
    investment_data = investment_data[investment_data["State"]!='Dadra and Nagar Haveli']
    investment_data = investment_data[investment_data["State"]!='Daman and Diu']
    row = investment_data.loc[investment_data['State'] == 'Dadra and Nagar Haveli and Daman and Diu']
    row_dnh = row.copy()
    row_dd = row.copy()
    row_dnh['State'] = 'Dadra and Nagar Haveli'
    row_dd['State'] = 'Daman and Diu'
    investment_data = pd.concat([investment_data, row_dnh, row_dd], ignore_index=True)

    # Calculate AirPollutionFactor
    investment_data['calc_AirPollutionFactor'] = investment_data['AQI'] / investment_data_india['AQI']
            
    # Calculate Investment
    investment_data['calc_land'] = 10000 * investment_data['IncomePerCapita [CurrPrice]'] / investment_data_india['IncomePerCapita [CurrPrice]']
    investment_data['calc_material'] = 250000
    investment_data['calc_installation'] = 123456 * investment_data['IncomePerCapita [CurrPrice]'] / investment_data_india['IncomePerCapita [CurrPrice]']
    investment_data['calc_grid_connection'] = 123456 * investment_data['SectoralGVA [CurrPrice]'] / investment_data_india['SectoralGVA [CurrPrice]']
    investment_data["calc_invest"] = investment_data["calc_land"] + investment_data["calc_material"] + investment_data["calc_installation"] + investment_data["calc_grid_connection"]
    investment_data["calc_invest"] = investment_data["calc_invest"]/10
    
    # Calculate Operation Cost
    investment_data['calc_operation'] = 80000 * investment_data['SectoralGVA [CurrPrice]'] / investment_data_india['SectoralGVA [CurrPrice]']
    investment_data['calc_operation'] = 20000 * investment_data['SectoralGVA [CurrPrice]'] / investment_data_india['SectoralGVA [CurrPrice]']
    investment_data['calc_equipment'] = 10000 * investment_data['SectoralGVA [CurrPrice]'] / investment_data_india['SectoralGVA [CurrPrice]']
    investment_data['calc_staff'] = 2000 * investment_data['SectoralGVA [CurrPrice]'] / investment_data_india['SectoralGVA [CurrPrice]']
    investment_data["calc_cost"] = investment_data["calc_operation"] + investment_data["calc_operation"] + investment_data["calc_equipment"] + investment_data["calc_staff"]
    investment_data["calc_cost"] = investment_data["calc_cost"] * 5
    
    # Calculate Revenue
    investment_data['calc_efficiency'] = 1 + 0.5 * investment_data['calc_AirPollutionFactor']
    investment_data['calc_prices'] = investment_data['Electricity Sales'] /investment_data['IncomePerCapita [CurrPrice]'] * investment_data['calc_efficiency']
    investment_data['calc_sales'] = investment_data['Electricity Sales'] * 0.2 * investment_data['Population'] / investment_data_india["Population"]
    investment_data['calc_revenue'] = investment_data['calc_sales'] * investment_data['calc_prices']
    investment_data['calc_revenue'] = investment_data['calc_revenue'] / 10 * 1000
    
    # Calculate Profit
    investment_data['calc_profit'] = investment_data['calc_revenue'] * investment_data['calc_cost']
    investment_data['calc_profit'] = investment_data['calc_profit'] / 1000 *9
    
    avg_profit = investment_data['calc_profit'].median()
    lower_bound = avg_profit * 0.2
    upper_bound = avg_profit * 1.8
    investment_data['calc_profit'] = investment_data['calc_profit'].clip(lower=lower_bound, upper=upper_bound)
    investment_data["calc_interest_rate"] = 0.0725
    investment_data['calc_ebit'] = 0.1*investment_data['calc_profit']
    
    return investment_data, investment_data_india
