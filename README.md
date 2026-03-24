# Medicare Part D Pharmacy Cost Analytics
Project Overview

This project analyzes Medicare Part D prescriber-level drug spending data to identify key drivers of pharmacy cost growth, prescribing variation across provider specialties, and concentration of spending among high-cost prescribers. The analysis also includes a forecasting model to estimate future drug spending trends.

The objective of this project is to replicate real-world healthcare payer analytics workflows used in pharmacy benefit management and healthcare consulting environments.

Business Problem

Healthcare payers must manage rising pharmacy costs driven by specialty drugs, chronic disease prevalence, and prescribing behavior variation. This project investigates:

Which drugs and specialties drive the highest costs
How prescribing behavior varies across providers
Whether pharmacy spending is concentrated among a small subset of prescribers
How future drug spending may evolve
Data Source

Data is sourced from the Centers for Medicare & Medicaid Services (CMS):

Medicare Part D Prescriber Public Use File (PUF)

This dataset contains:

Prescriber identifiers and specialty
Drug-level spending and utilization metrics
Beneficiary counts
Geographic prescribing patterns
Key Analyses Performed
Cost Trend Analysis

Identified major drug cost drivers and utilization patterns contributing to Medicare pharmacy spending.

Provider Variation Analysis

Evaluated prescribing differences across specialties and geographic regions.

Cost Concentration (Pareto Analysis)

Measured the extent to which pharmacy spending is concentrated among high-cost prescribers.

Specialty-Driven Cost Intensity

Analyzed cost per beneficiary and cost per claim across provider specialties.

Forecasting Model

Built a predictive model to estimate future pharmacy spending based on historical cost patterns.

Tools & Technologies
Python
Pandas
NumPy
Matplotlib
Scikit-learn
CMS Public Healthcare Data
Key Insights
Pharmacy spending is highly concentrated among specialty care providers.
A small percentage of prescribers account for a disproportionate share of total drug costs.
Cost growth appears structurally driven by high-intensity specialty treatments.
Forecasting results indicate continued upward pressure on pharmacy spending.
Project Structure
medicare-part-d-spending/
│
├── data/
├── notebooks/
├── output/
├── scripts/
└── README.md
Future Enhancements
Time-series forecasting using ARIMA / Prophet
Patient risk stratification modeling
Geographic cost variation deep dive
SQL analytics pipeline replication
Interactive dashboard development
