import pandas as pd
import numpy as np

# =======> IMPORT DATA

dados = pd.read_excel("REGREÇÃO E CORREL.xlsx")

# SELECT ROWS
# print(dados[["HOME", "Bathroom"]])


# =======> FILTERS

filtered_data = dados[(dados["Bathroom"] > 1) & (dados["SQFT"] > 2000) & (dados["School Disctrict (boolean)"] == 1)]
subset_list = [2, 5, 4.5]
filtered_by_subset = dados[dados["Bathroom"].isin(subset_list)]
# print(filtered_by_subset)
# =======> ADDING NEW COLUMN

dados["price_per_sqft"] = dados["SALES ($000)"] * 1000 / dados["SQFT"]


# =======> SORTING DATA

sorted_data = dados.sort_values(by=["price_per_sqft", "Bathroom"], ascending=[False, True])

# print(sorted_data)

# ========> AGG (APPLY A FUNCTION RESULT TO A COLUMN)

def get_first_element(column):
    return column[0]

agg_data = dados.agg([get_first_element, np.max, np.min, np.mean])

# print(agg_data)

# ==========> ADD A CUMMULATIVE SUM COLUMN TO DATA

sales_cumsum = dados.sort_values("SALES ($000)")

sales_cumsum["cum_sales"] = sales_cumsum["SALES ($000)"].cumsum()

# print(sales_cumsum)

# =========> DROP DUPLICATES

# OF A SINGLE COLUMN
dados_no_single_duplicate = dados.drop_duplicates("Bathroom")

dados_no_combined_duplicate = dados.drop_duplicates(subset=["Bathroom", "SQFT"])
# print(dados_no_combined_duplicate)

# ========> COUNTING THE INCIDENCE OF A VALUE

bathroom_counts = dados["Bathroom"].value_counts() # TOTAL INCIDENCES OF BATHROOMS TYPES ON ALL ROWS

proportional_bathrooms =  dados["Bathroom"].value_counts(normalize=True, sort=True) # PROPORTIONAL VALUE 


# ==========> GROUPING AND SUMS

# WITHOUT GROUPBY:

sales_all = dados["SALES ($000)"].sum()

sales_bath_A = dados[dados["Bathroom"] == 1.25]["SALES ($000)"].sum()

sales_bath_B = dados[dados["Bathroom"] == 2]["SALES ($000)"].sum()

sales_per_bath_type = [sales_bath_A, sales_bath_B] / sales_all

# print(sales_per_bath_type)

# WITH GROUPBY:

sales_by_bath_type = dados.groupby("Bathroom")["SALES ($000)"].sum()

proportional_sales_per_bath = sales_by_bath_type / sum(sales_by_bath_type)

proportional_sales_per_bath_alternative = sales_by_bath_type / dados["SALES ($000)"].sum()

# MULTIPLE GROUP STATS

multiple_stats_per_group = dados.groupby("Bathroom")["SALES ($000)"].agg([np.min, np.max, np.mean, np.median])

# print(multiple_stats_per_group)

print(multiple_stats_per_group)

# =======> PIVOT TABLES 

pivot_bathroom = dados.pivot_table(index="Bathroom", values="SALES ($000)", aggfunc=[np.min, np.max, np.mean, np.median])

print(pivot_bathroom)
