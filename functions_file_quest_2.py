#!/usr/bin/env python
# coding: utf-8

# ### Data wrangling and cleaning functions/methods

# In[ ]:


#columns in lowercase
df_new.columns.str.lower()

# eliminating rows with all the values missing
df_new = df_new.dropna(how='all')

# checking if there are any null values in columns
df_new.isna().any()

# summing the number of null values in each variable
df_new.isnull().sum()

#dropping columns that were not necessary/redundant for our analysis
df_new.drop(columns=["country_clustered"], inplace=True)

# replacing invalid values for usable values
sex_cleaning = {'F ':'F', 'M ':'M', ' M':'M', 'M x 2':'M', 'N':'M'}
df_new["sex"] = df_new["sex"].replace(sex_cleaning)

# Removing the last unique values that weren't "F" or "M" in "sex" variable
df_new = df_new[(df_new['sex'] != "lli") & (df_new['sex'] != ".")]

# Apply + lambda function to make lowercase all strings with the variable "country"
df_new["country"] = df_new["country"].apply(lambda x: x.lower() if type(x) == str else x )

# Function for clustering countries into regions to simplify analysis
def cluster_country(country):
    if pd.isna(country):
        return 'Unknown'

    country = country.lower()

    if country in ['australia', 'new zealand', 'papua new guinea', 'fiji', 'samoa', 'solomon islands', 'vanuatu', 'kiribati', 'micronesia', 'tuvalu', 'marshall islands']:
        return 'Australia & Oceania'
    elif country in ['usa', 'canada', 'mexico']:
        return 'North America'
    elif country in ['brazil', 'argentina', 'colombia', 'peru', 'venezuela', 'chile', 'ecuador', 'guyana', 'suriname', 'paraguay', 'uruguay']:
        return 'South America'
    elif country in ['france', 'united kingdom', 'germany', 'italy', 'spain', 'portugal', 'greece', 'netherlands', 'croatia', 'ireland', 'sweden', 'norway', 'slovenia', 'switzerland', 'monaco']:
        return 'Europe'
    elif country in ['egypt', 'morocco', 'south africa', 'nigeria', 'ghana', 'algeria', 'kenya', 'namibia', 'mozambique', 'libya', 'liberia', 'senegal', 'sierra leone', 'djibouti', 'tanzania', 'sudan', 'angola']:
        return 'Africa'
    elif country in ['china', 'india', 'japan', 'south korea', 'north korea', 'bangladesh', 'vietnam', 'thailand', 'malaysia', 'indonesia', 'sri lanka', 'taiwan', 'myanmar']:
        return 'Asia'
    elif country in ['iran', 'iraq', 'saudi arabia', 'united arab emirates', 'jordan', 'israel', 'palestine', 'yemen', 'kuwait', 'lebanon', 'turkey', 'syria']:
        return 'Middle East'
    elif country in ['bahamas', 'jamaica', 'dominican republic', 'haiti', 'barbados', 'trinidad', 'antigua', 'cuba', 'puerto rico', 'aruba', 'belize', 'grenada', 'saint kitts and nevis', 'turks and caicos']:
        return 'Caribbean'
    else:
        return 'Other'

# Applying the function to execute the clustering
df_new['country'] = df_new['country'].apply(cluster_country)

# Checking what we clustered into "Other" to refine our grouping (e.g. for the activity variable)
other_activities = df_new[df_new["activity_clustered"] == "Other"]["activity"]


# ### Exploratory data analysis functions and methods

# In[ ]:


# Filtering for males who have a know age and fatalities that are not marked as unknown
df3_clean = df[(df["fatal"] == "Y") | (df["fatal"] == "N")]
df3_male = df3_clean[(df3_clean["sex"] == "M") & (df3_clean["age"].notnull())]

# Using apply function to create two groups for males who are 25 years or younger and more than 25 years old
df3_male["age_group"] = df3_male["age"].apply(lambda x: "≤25" if x <= 25 else ">25")

# Using grouoby to check fatalities per age group
df3_male.groupby("age_group")["fatal"].value_counts()

# Creating pivot tables
df3_pivot = df3_male.pivot_table(index="age_group", columns="fatal", aggfunc="size", fill_value=0)
df3_pivot

# Overviewing the dataset
df3_pivot.describe()


# In[6]:


get_ipython().system('jupyter nbconvert --to script Functions file (Quest 2).ipynb')

