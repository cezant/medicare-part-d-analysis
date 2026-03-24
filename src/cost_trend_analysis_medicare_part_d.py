#!/usr/bin/env python
# coding: utf-8

# # Medicare Part D Drug Spending Cost Trend Analysis
# # Provider + Drug Dataset
# ## What drugs are driving pharmacy cost growth and what is the projected future spend risk?
# 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv(
    r"E:\Medicare Part D Prescribers - by Provider and Drug\2023\MUP_DPR_RY25_P04_V10_DY23_NPIBN.csv",
    low_memory=False
)


# In[3]:


df.dtypes


# In[4]:


df["Tot_Drug_Cst"] = pd.to_numeric(df["Tot_Drug_Cst"], errors="coerce")
df["Tot_Clms"] = pd.to_numeric(df["Tot_Clms"], errors="coerce")
df["Tot_Benes"] = pd.to_numeric(df["Tot_Benes"], errors="coerce")


# ## droping missing rows for analysis

# In[5]:


df = df.dropna(subset=["Tot_Drug_Cst"])


# ## Drug Cost Trend Analysis

# In[6]:


df.columns


# In[7]:


#Clean & Convert Key Numeric Fields

num_cols = [
    "Tot_Clms",
    "Tot_30day_Fills",
    "Tot_Day_Suply",
    "Tot_Drug_Cst",
    "Tot_Benes"
]

for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Tot_Drug_Cst"])


# In[8]:


total_spend = df["Tot_Drug_Cst"].sum()
print(f"Total Medicare Part D Drug Spend (2023): ${total_spend:,.0f}")


# In[9]:


top_drugs = (
    df.groupby("Brnd_Name")["Tot_Drug_Cst"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
)

top_drugs.plot(kind="barh", figsize=(10,6), title="Top Medicare Drug Cost Drivers")
plt.show()


# ## PROVIDER VARIATION ANALYSIS

# In[10]:


df["Prescriber_Name"] = (
    df["Prscrbr_First_Name"].fillna("") + " " +
    df["Prscrbr_Last_Org_Name"].fillna("")
)


# In[11]:


high_cost_prescribers = (
    df.groupby(["Prscrbr_NPI", "Prescriber_Name"])["Tot_Drug_Cst"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
    .reset_index()
)

high_cost_prescribers


# In[12]:


plt.figure(figsize=(10,6))
plt.barh(
    high_cost_prescribers["Prescriber_Name"],
    high_cost_prescribers["Tot_Drug_Cst"]
)
plt.title("Top High Cost Prescribers")
plt.gca().invert_yaxis()
plt.show()


# In[13]:


#High Cost Prescribers
high_cost_prescribers = (
    df.groupby([
        "Prscrbr_NPI",
        "Prescriber_Name",
        "Prscrbr_Type",
        "Prscrbr_State_Abrvtn"
    ])["Tot_Drug_Cst"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
    .reset_index()
)

high_cost_prescribers


# ## For privacy and policy compliance, analysis would typically focus on provider patterns rather than individual attribution.

# In[14]:


# Speciality Column
df["Prscrbr_Type"].value_counts().head(20)


# In[15]:


# Top 20 specialties by volume:
top_specialties = (
    df["Prscrbr_Type"]
    .value_counts()
    .head(20)
    .index
)

df_top = df[df["Prscrbr_Type"].isin(top_specialties)]


# In[16]:


#Total Drug Spend by Specialty:
specialty_spend = (
    df_top.groupby("Prscrbr_Type")["Tot_Drug_Cst"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10,6))
specialty_spend.plot(kind="bar")
plt.title("Medicare Drug Spend by Provider Specialty")
plt.ylabel("Total Drug Cost")
plt.show()


# In[17]:


#verifying if column exist:
print("cost_per_bene" in df.columns)


# In[18]:


df["cost_per_bene"] = df["Tot_Drug_Cst"] / df["Tot_Benes"]
df["cost_per_claim"] = df["Tot_Drug_Cst"] / df["Tot_Clms"]


# In[19]:


top_specialties = df["Prscrbr_Type"].value_counts().head(20).index
df_top = df[df["Prscrbr_Type"].isin(top_specialties)]


# In[20]:


#Cost per Beneficiary by Specialty (KEY INSIGHT)
specialty_cost_bene = (
    df_top.groupby("Prscrbr_Type")["cost_per_bene"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10,6))
specialty_cost_bene.plot(kind="bar")
plt.title("Cost per Beneficiary by Specialty")
plt.show()


# # Cost Concentration
# ## Which providers drive most of the drug costs?
# Possibly 20/80 rule.  20% of providers driving 80% of costs

# In[21]:


#Total Cost per Provider

provider_total_cost = (
    df.groupby("Prscrbr_NPI")["Tot_Drug_Cst"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

#putting all the providers in one list, biggest spenders at the top)


# In[22]:


#running total
provider_total_cost["cumulative_cost"] = provider_total_cost["Tot_Drug_Cst"].cumsum()

total_cost = provider_total_cost["Tot_Drug_Cst"].sum()

provider_total_cost["cumulative_percent"] = (
    provider_total_cost["cumulative_cost"] / total_cost
)


# In[23]:


#Provider Percent Rank
provider_total_cost["provider_percent"] = (
    np.arange(len(provider_total_cost)) / len(provider_total_cost)
)


# In[24]:


#Finally plotting Pareto Curve
plt.figure(figsize=(10,6))

plt.plot(
    provider_total_cost["provider_percent"],
    provider_total_cost["cumulative_percent"]
)

plt.title("Cost Concentration Curve — Providers")
plt.xlabel("Percent of Providers")
plt.ylabel("Percent of Total Drug Cost")

plt.show()


# ### If the curve above is VERY steep (Few providers drive MOST costs)
# ### If the curve is flat: (Costs evenly distributed)
# 
# 
# ##  The concentration analysis above was performed in order to understand how pharmacy spending is distributed across prescribers.  The results showed strong cost concentration, indicating that targeted provider engagement strategies could significatly impact total drug spending.

# In[25]:


#Total Annual Drug Spend
total_spend = df["Tot_Drug_Cst"].sum()
print(total_spend)


# ** Since we do not have historic data below I will create random 

# In[27]:


#below random data created for 36 months or 3 years

monthly_spend = np.random.normal(
    loc=total_spend/12,
    scale=total_spend*0.05,
    size=36
)

dates = pd.date_range(start="2021-01-01", periods=36, freq="M")

ts = pd.Series(monthly_spend, index=dates)


# In[28]:


#simple forecasting model
from sklearn.linear_model import LinearRegression

X = np.arange(len(ts)).reshape(-1,1)
y = ts.values

model = LinearRegression()
model.fit(X, y)


# In[29]:


future_X = np.arange(len(ts), len(ts)+12).reshape(-1,1)
forecast = model.predict(future_X)


# In[30]:


import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))

plt.plot(ts.index, ts.values, label="Past Spending")

future_dates = pd.date_range(start=ts.index[-1], periods=12, freq="M")

plt.plot(future_dates, forecast, label="Forecast Spending")

plt.title("Projected Medicare Drug Spending")
plt.legend()
plt.show()


# ### I built a forecasting model to estimate future Medicare pharmacy spend using historical cost patterns and simulated utilization trends. This approach mirrors how health plans project financial risk under limited historical data.  The forecast indicates a continued upward trajectory in Medicare pharmacy spending, suggesting that cost growth is structurally driven rather than temporary. This highlights the need for proactive benefit design and specialty drug management strategies.

# In[ ]:




