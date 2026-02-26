import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore

# Load the data
file_path = r"C:\Users\smiti\OneDrive\Desktop\Internship Related\Comparative Analysis of Salaries for Engineering Graduates in Core vs. IT Companies - Form responses 1.csv"
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe to understand its structure
print("Initial DataFrame:")
print(data.head())

# Display the columns to check for exact names
print("Columns in the DataFrame:")
print(data.columns)

# Data Cleaning
data.dropna(inplace=True)  # Drop rows with missing values

# Standardize the 'Type of company' column for consistency
data['Type of company'] = data['Type of company'].apply(lambda x: 'Core' if 'core' in x.lower() else 'IT')

# Define a function to convert salary ranges to their midpoints
def convert_salary(salary_range):
    if pd.isna(salary_range):
        return None
    salary_range = salary_range.lower()
    if 'less than 3 lakhs' in salary_range:
        return 2.5
    elif '3-5 lakhs' in salary_range:
        return 4
    elif '5-7 lakhs' in salary_range:
        return 6
    elif '7-10 lakhs' in salary_range:
        return 8.5
    elif '10-15 lakhs' in salary_range:
        return 12.5
    else:
        return None

# Apply the function to create a new column with numerical salary values
data['Salary (lakhs)'] = data['current salary range(per annum)'].apply(convert_salary)

# Print the DataFrame after cleaning
print("Cleaned DataFrame:")
print(data.head())

# Separate data for core companies and IT companies
core_data = data[data['Type of company'] == 'Core']
it_data = data[data['Type of company'] == 'IT']

# Calculate average salaries
core_avg_salary = core_data['Salary (lakhs)'].mean()
it_avg_salary = it_data['Salary (lakhs)'].mean()

# Analyze job satisfaction
satisfaction_counts = data['Satisfaction with current salary'].value_counts()
switch_to_core = data[data['Would you like to switch to another carries for better pay or career growth'] == 'yes']['Type of company'].value_counts()
switch_to_it = data[data['Would you like to switch to another carries for better pay or career growth'] == 'no']['Type of company'].value_counts()

# Plot average salaries
plt.figure(figsize=(10, 6))
sns.barplot(x='Company Type', y='Average Salary (lakhs)', data=pd.DataFrame({
    'Company Type': ['Core', 'IT'],
    'Average Salary (lakhs)': [core_avg_salary, it_avg_salary]
}))
plt.title('Comparative Analysis of Average Salary of Engineering Graduates')
plt.ylabel('Average Salary (lakhs)')
plt.show()

# Plot job satisfaction
plt.figure(figsize=(10, 6))
satisfaction_counts.plot(kind='bar')
plt.title('Job Satisfaction of Engineering Graduates')
plt.xlabel('Satisfaction Level')
plt.ylabel('Number of Respondents')
plt.show()

# Plot switch preference to Core and IT
fig, ax = plt.subplots(1, 2, figsize=(14, 6))
switch_to_core.plot(kind='bar', ax=ax[0], color='blue')
ax[0].set_title('Preference to Switch to Core Companies')
ax[0].set_xlabel('Company Type')
ax[0].set_ylabel('Number of Respondents')

switch_to_it.plot(kind='bar', ax=ax[1], color='blue')
ax[1].set_title('Preference to Switch to IT Companies')
ax[1].set_xlabel('Company Type')
ax[1].set_ylabel('Number of Respondents')

plt.tight_layout()
plt.show()

# Generate a report
report = {
    'Core Companies Average Salary (lakhs)': core_avg_salary,
    'IT Companies Average Salary (lakhs)': it_avg_salary,
    'Difference (lakhs)': it_avg_salary - core_avg_salary,
    'Satisfaction Counts': satisfaction_counts.to_dict(),
    'Switch to Core Preference': switch_to_core.to_dict(),
    'Switch to IT Preference': switch_to_it.to_dict()
}

print(report)
