import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
import seaborn as sns
import matplotlib.pyplot as plt

# Generate sample data
np.random.seed(42)
village_population = ['Small', 'Medium', 'Large']
employment_type = ['Agriculture', 'Business', 'Service']

data = []
for pop in village_population:
    for emp in employment_type:
        for _ in range(10):  # 10 samples per category combination
            if pop == 'Small':
                base_income = 200  
            elif pop == 'Medium':
                base_income = 350  
            else:
                base_income = 500  

            if emp == 'Agriculture':
                income = base_income + np.random.randint(-50, 50)
            elif emp == 'Business':
                income = base_income + np.random.randint(20, 100)
            else:
                income = base_income + np.random.randint(-30, 70)

            data.append([pop, emp, income])

# Create DataFrame
df = pd.DataFrame(data, columns=['PopulationSize', 'EmploymentType', 'Income'])

# Perform Two-Way ANOVA
model = ols('Income ~ C(PopulationSize) + C(EmploymentType) + C(PopulationSize):C(EmploymentType)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print("\nANOVA Results:\n", anova_table)

# Visualizations
sns.set_style("whitegrid")

# Boxplot: Income by Population Size
plt.figure(figsize=(10, 5))
sns.boxplot(x="PopulationSize", y="Income", data=df, palette="Set2")
plt.title("Income Distribution by Population Size")
plt.xlabel("Village Population Size")
plt.ylabel("Average Monthly Income (USD)")
plt.show()

# Boxplot: Income by Employment Type
plt.figure(figsize=(10, 5))
sns.boxplot(x="EmploymentType", y="Income", data=df, palette="Set1")
plt.title("Income Distribution by Employment Type")
plt.xlabel("Employment Type")
plt.ylabel("Average Monthly Income (USD)")
plt.show()

# Heatmap for Correlation Matrix
correlation_matrix = df.corr(numeric_only=True)
plt.figure(figsize=(5, 4))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=1)
plt.title("Correlation Matrix of Variables")
plt.show()

plt.figure(figsize=(8,5))
sns.pointplot(x="EmploymentType", y="Income", hue="PopulationSize", data=df, ci=None)
plt.title("Interaction Effect of Population Size and Employment Type on Income")
plt.xlabel("Employment Type")
plt.ylabel("Average Monthly Income")
plt.show()

# Descriptive Statistics
desc_stats = df.groupby(['PopulationSize', 'EmploymentType'])['Income'].describe()
print("\nDescriptive Statistics:\n", desc_stats)
