#!/usr/bin/env python
# coding: utf-8

# In this project, I use Python Pandas & Python Matplotlib to analyze and answer business questions about 12 months worth of sales data. The data contains hundreds of thousands of electronics store purchases broken down by month, product type, cost, purchase address, etc.

# In[49]:


import pandas as pd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:





# PROBLEMS
# What was the best month for sales? How much was earned that month?
# What city sold the most product?
# What time should we display advertisements to maximize likelihood of customer’s buying products?
# What Products are most often sold together?
# What product sold the most? Why do you think it did?

# # 1. What was the best month for sales? How much was earned that month?

# In[54]:


df = pd.read_csv("Sales_April_2019.csv")
df.head()


# In[55]:


df = pd.read_csv("Sales_August_2019.csv")
df.head()


# In[51]:


df = pd.read_csv("Sales_December_2019.csv")
df.head()


# In[5]:


df = pd.read_csv("Sales_February_2019.csv")
df.head()


# In[6]:


df = pd.read_csv("Sales_January_2019.csv")
df.head()


# In[7]:


df = pd.read_csv("Sales_July_2019.csv")
df.head()


# In[8]:


df = pd.read_csv("Sales_June_2019.csv")
df.head()


# In[9]:


df = pd.read_csv("Sales_March_2019.csv")
df.head()


# In[10]:


df = pd.read_csv("Sales_May_2019.csv")
df.head()


# In[11]:


df = pd.read_csv("Sales_November_2019.csv")
df.head()


# In[12]:


df = pd.read_csv("Sales_October_2019.csv")
df.head()


# In[13]:


df = pd.read_csv("Sales_September_2019.csv")
df.head()


# In[14]:


all_months_data = pd.concat(map(pd.read_csv, ['Sales_April_2019.csv', "Sales_August_2019.csv", "Sales_December_2019.csv", "Sales_February_2019.csv", "Sales_January_2019.csv", "Sales_July_2019.csv", "Sales_June_2019.csv", "Sales_March_2019.csv", "Sales_May_2019.csv", "Sales_November_2019.csv", "Sales_October_2019.csv", "Sales_September_2019.csv"]), ignore_index=True)
print(all_months_data)


# In[48]:


df.head()


# In[16]:


df.tail()


# In[17]:


df.describe()


# In[18]:


df.info()


# In[19]:


all_months_data = pd.concat([all_months_data, df])


# In[20]:


all_months_data.head()


# In[21]:


all_months_data.info()


# In[22]:


all_months_data.tail()


# Now we’re ready to answer the problem number 1. To remind you, the question is: What was the best month for sales? How much was earned that month?

# In[23]:


#There are NaN values in our data. You could spot on of NaN value
#Now we need to clean up the data by dropping rows of NaN. 
#Let’s spot more NaN value here. You don’t have to do this, I am just curious.
non_df = all_months_data[all_months_data.isna().any(axis=1)]

non_df.head()


# In[24]:


#Removing Non Values in our data
all_months_data = all_months_data.dropna(how="all")

#Removing rows based on the condition, finding 'Or' and delete it
df_dummy = all_months_data[all_months_data["Order Date"].str[0:2]=="Or"]
df_dummy.head()


# In[25]:


#Removing Nan Values in our data

all_months_data=all_months_data.dropna(how="all")

#Removing rows based on condition, finding 'Or' and delete it
all_months_data = all_months_data[all_months_data["Order Date"].str[0:2]!="Or"]

all_months_data["Month"]=all_months_data["Order Date"].str[0:2]
all_months_data["Month"] = all_months_data["Month"].astype("int32")
all_months_data.head()

#we successfully created “Month” column and make its data type to integer.


# Now, are we ready to answer the question? Not yet, we need obviously one more column called “Sales” Column. How can we get that? We get “Sales” by multiplying “Quantity Ordered” and “Price Each” values. Let’s create it.

# In[26]:


#So the next task is to convert these columns to the correct type (“Quantity Ordered” is integer and “Price Each” is float). 
#We’re gonna use pd.to_numeric() method to convert them to numeric

#Removing Nan Values in our data
all_months_data=all_months_data.dropna(how="all")

#Removing rows based on condition, finding "Or" and delete it
all_months_data = all_months_data[all_months_data["Order Date"].str[0:2]!="Or"]

#Add "Month" Column
all_months_data["Month"] = all_months_data["Order Date"].str[0:2]
all_months_data["Month"]= all_months_data["Month"].astype("int32")

#Convert "Quantity Ordered" and "Price Each" to numeric
all_months_data["Quantity Ordered"] = pd.to_numeric(all_months_data["Quantity Ordered"]) #becoming an integer
all_months_data["Price Each"] = pd.to_numeric(all_months_data["Price Each"])#becoming a float

#Add "Sales" Column
all_months_data["Sales"] = all_months_data["Quantity Ordered"]*all_months_data["Price Each"]
all_months_data.head()


# In[27]:


all_months_data.tail()


# Now the “Sales” Column is successfully created, we can answer the first question. What was the best month for sales? How much was earned that month? We can easily answer it by using groupby(‘Month’).sum() method.

# In[28]:


all_months_data.groupby("Month").sum()


# We can clearly see that month 12 (December) is the highest sales in 2019 with approximately $4,810,000. But we need to visualize it to make our bussiness partner easier to understand. So we’re gonna import matplotlib and visualizing our results with bar chart.

# In[29]:


#Importing Matplotlib
import matplotlib.pyplot as plt


# In[30]:


#Lets Visualize our results
#Visualizing our results using matplotlib library.

months = range(1,13) #For X axes
results = all_months_data.groupby("Month").sum()

plt.bar(months, results["Sales"])
plt.show()


# It’s good. But we need to make it looks neater. So we’re just gonna add a little code.

# In[31]:


import matplotlib.pyplot as plt


# In[32]:


months = range(1,13) #For X axes
results = all_months_data.groupby("Month").sum()

plt.bar(months, results["Sales"])
plt.xticks(months)
labels, location = plt.yticks()
plt.ylabel("Sales in million USD")
plt.xlabel("Month Number")
plt.show()


# # 2. What city sold the most product?

# In[33]:


#To answer this question, obviously we need to create a new column called “City” column
#To figure out where can we get our “City” column using .head() method.


# In[34]:


all_months_data.head()


# The “Purchase Address” Column contain the city. We can’t get it directly, we need to extract the data. We can use one of most useful function in pandas, .apply() method.

# In[35]:


#Add a "City" Column

all_months_data["City"] = all_months_data["Purchase Address"].apply(lambda x: x.split(",")[1])
all_months_data.head()


# We successfully created a “City” column. So are we ready to answer the second question? Not yet. We get an issue here. It’s not error, it’s the value of the “City” Column. This is just a rare case when there are 2 cities are named exactly the same. Example someone in New England and someone in West Coast would think Portland in different way. Someone in New England thinks Portland as Portland Maine and someone in West Coast thinks Portland as Portland Oregon. So in our dataset we actually had the overlapping cities between these two. So, we should also grab the state.

# In[36]:


#Function
def get_city(address):
    return address.split(",")[1]
def get_state(address):
    return address.split(",")[2].split(" ")[1]

#Exract the city and the state
all_months_data["city"] = all_months_data["Purchase Address"].apply(lambda x: get_city(x) + '' + get_state(x))
all_months_data.head()

#Extracting the state to “City” Column


# In[37]:


results2 = all_months_data.groupby("city").sum()
results2


# If you look carefully you can see that San Fransisco is the highest sold product of all cities with approximately $8,200,000. We clearly need to visualize it because it’s so hard to conclude anything just based on that numbers and also it will make our bussiness partner easier to understand.

# In[38]:


#We have  imported the matplotlib
import matplotlib.pyplot as plt

cities = [city for city, df in all_months_data.groupby("city")]

plt.bar(cities, results2["Sales"])
plt.xticks(cities, rotation="vertical", size = 8)
labels, location = plt.yticks()
plt.yticks(labels, (labels/1000000).astype(int)) #Scaling in million USD
plt.ylabel("Sales in millions USD")
plt.xlabel("City Name")
plt.show()


# Plotting the Sales Grouped by Cities.
# We need to figure out why San Fransisco is the highest sale compare to other cities. Maybe Sillicon Valley need more electronic products. Maybe the advertisement is better in San Fransisco. We can use this data to improve the sales of bussiness.

# #  3. What Time Should We Display Advertisements to Maximize Likelihood of Customer’s Buying Product?

# In[39]:


all_months_data.head()


# In[40]:


all_months_data.tail()


# If we’re gonna use our data to answer this question, we need to aggregate the period in 24 hours distribution. Look carefully at Figure 23. In “Order Date” column, there are times data. We could extract it like we did before. But to make it more consistent, we need to convert the “Order Date” Column into date time object. We’re gonna use pd.to_datetime() method.

# In[63]:


#Create new Column in date-time Object (DTO)

all_months_data["Order_Date_DTO"] = pd.to_datetime(all_months_data["Order Date"])

all_months_data


# It will take a little bit longer because of the heavy calculation. Now we can create a new column called “Hour” contain the extraction of “Order_Date_DTO” data. We only need the hours data, so we can extract them by doing this

# In[57]:


#Create new column in date-time object (DTO)

all_months_data ["Order_Date_DTO"] = pd.to_datetime(all_months_data["Order Date"])

#Extraction the hours data

all_months_data["Hour"]= all_months_data["Order_Date_DTO"].dt.hour

all_months_data.head()

# Extracting The Hours Data Into The New Column


# In[ ]:





# Now we can answer the third question, what time should we display advertisements to maximize likelihood of customer’s buying product? To answer this, we’re gonna group it by the hours and counting all of the orders.

# In[65]:


results3 = all_months_data.groupby(["Hour"]).count()
results3


# To answer the third question, we only need the “Quantity Ordered” column. Now let’s visualize it. We want it to be the line chart because this spesific data (hours) are more logical to show using line chart than bar chart because the data has to be continue.

# In[66]:


#Plotting

results3 = all_months_data.groupby(["Hour"])["Quantity Ordered"].count()

hours = [hour for hour, df in all_months_data.groupby("Hour")]

plt.plot(hours, results3)
plt.xticks(hours)
plt.xlabel("Hours")
plt.ylabel("Number of Orders")
plt.grid()
plt.show()


# There are approximately 2 peaks at the data. They are 12 (12 PM) and 19 (7 PM). It makes sense since most people shopping during the day. From this data, we can suggest to our bussiness partner to advertise their product right before 12 PM and/or 7 PM. It could be 11.30 AM and/or 6.30 PM.

# # 4. What Products Are Most Often Sold Together?

# In[67]:


all_months_data.head()


# In[68]:


all_months_data.tail()


# We can see that “Order ID” indicate the transaction. So by grouping the product by the Order ID, we are able to know what products are often sold together. We’re gonna use .duplicated() method to find a duplicate values of “Order ID”.

# In[69]:


#Make a new dataframe to separate the duplicate values of Order ID


new_all = all_months_data[all_months_data["Order ID"].duplicated(keep=False)]

new_all.head(20)


# In[70]:


new_all.tail(20)


# Now we want to create a column called “Product Bundle” that contain example Google Phone and Wired Headphone (transaction 17650) at the same line. We’re gonna use the .transform() method to join values from two rows into a single row.

# In[74]:


#Make a new dataframe to separate the duplicated values of order ID

new_all = all_months_data[all_months_data["Order ID"].duplicated(keep=False)]

#Joining few products with the same Order ID into the same line

new_all["Product_Bundle"] = new_all.groupby("Order ID")["Product"].transform(lambda x:  ",".join(x))

new_all.head()


# Dropping rows with duplicate values

# In[76]:


#Make a new dataframe to separate the duplicated values of order ID

new_all = all_months_data[all_months_data["Order ID"].duplicated(keep=False)]

#Joining few products with the same Order ID into the same line.

new_all["Product_Bundle"] = new_all.groupby("Order ID")["Product"].transform(lambda x: ",".join(x))

#Dropping the duplicates values

new_all = new_all[["Order ID", "Product_Bundle"]].drop_duplicates()

new_all.head()


# We need to count the pair of products. We need new libraries because they have all we need to count all the combination of products bundle. We’re gonna use itertools and collections libraries.

# In[77]:


from itertools import combinations
from collections import Counter

count = Counter()

for row in new_all["Product_Bundle"]:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))
    
    
print(count)


# In[78]:


from itertools import combinations
from collections import Counter

count = Counter()

for row in new_all["Product_Bundle"]:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))
    
    
count.most_common(10)


# We can clearly see that the most often products sold together are iPhone and Lightning Charging Cable with 1005 transactions. We could count the 3 product bundles by just changing the count.update index into 3.

# In[79]:


from itertools import combinations
from collections import Counter

count = Counter()

for row in new_all["Product_Bundle"]:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 3)))

count.most_common(10)


# We can see the most often sold products (3 products) together are Google Phone, USB-C Charging Cable, and Wired Headphones with 87 transactions. It’s not really significant compare to the 2-Product Bundle. So we’re gonna ignore the 3-Product bundle.
# What would we do with this data? Well, we could offer a smart deal to the customer that buy iPhone, you could recommend the charging cable with discount. That’s one of the possibility and you can bundle the remaining products if you need to

# # 5. What product sold the most? Why do you think it did?

# In[80]:


all_months_data.head()


# In[81]:


all_months_data.tail()


# We need to sum up the “Quantity Ordered” based on grouping the Product. So let’s do it.

# In[82]:


product_group = all_months_data.groupby("Product")
product_group.sum()


# To make it easier to understand, let’s visualize it.

# In[85]:


product_group = all_months_data.groupby("Product")

#Visualizing

quantity_ordered = product_group.sum()["Quantity Ordered"]

keys = [pair for pair, df in product_group]
plt.bar(keys, quantity_ordered)
plt.xticks(keys, rotation='vertical', size=8)
plt.show()


# Now we can see what product sold the most, it’s AAA Batteries(4 pack). We can also see that AA Batteries (4 pack), Lightning Charging Cable, USB-C Charging Cable, and Wired Headphones are sold more than other products. Why are they sold the most? The first impression is that they are cheaper than other products. As a data scientist, let’s prove this hypothesis. We could do it by overlaying the graph by their actual price and see if they have direct correlation.

# In[87]:


prices = all_months_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(keys, quantity_ordered, color='g')
ax2.plot(keys, prices, color='b')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(keys, rotation='vertical', size=8)

fig.show()


# Our hypothesis is true if the high sold products have low price. From the graph we can see it is the case for AAA Batteries and all products except the Macbook Pro Laptop and ThinkPad Laptop. They have decent orders eventhough they are expensive. We can say that there are many people in the world need laptops. So the laptops are the exception because the laptops have high demand.

# CONCLUSION
# 1. What was the best month for sales? 
# How much was earned that month?
# The best month for sales is December. The company earned approximately $4,810,000.
# 2. What city sold the most product?
# San Fransisco is the city with the highest sales.
# 3. What time should we display advertisements to maximize likelihood of customer’s buying products?
# We can suggest to advertise the products right before 12 PM and/or 7 PM. It could be 11.30 AM and/or 6.30 PM.
# 4. What Products are most often sold together?
# The most often products sold together are iPhone and Lightning Charging Cable with 1005 transactions.
# 5. What product sold the most? Why do you think it did?
# AAA Batteries(4 pack) is the most sold product. Because it’s cheaper than other products and has high demand.

# In[ ]:




