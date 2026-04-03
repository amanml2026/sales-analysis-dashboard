#Modules/Libraries
import pandas as pd
from matplotlib import pyplot as plt
from dateutil.parser import parse

#Opening file and retrieving data
df=pd.read_csv('sales.csv')
pd.set_option('display.max_columns',113)
pd.set_option('display.max_rows',85)
#Structure of data
# print(df.shape)
print(df.dtypes)

#Exploring data
print(df.head())
print(df.info())
print(df.describe())

#Data clean
df.dropna(axis='index',how='any',subset=['order_id','product_id'],inplace=True)
df.drop_duplicates(inplace=True)

#Parsing the date:
df['order_date']=(df['order_date']).apply(lambda x:parse(x))
df['ship_date']=(df['ship_date']).apply(lambda x:parse(x))



#Plot data(Sales Over time)

fig1,(ax1,ax2)=plt.subplots(nrows=1,ncols=2)
fig2,(ax3,ax4)=plt.subplots(nrows=1,ncols=2)
fig3,(ax5,ax6)=plt.subplots(nrows=1,ncols=2)


df['sales']=df['sales'].str.replace(',','').astype(float)
# print(df.dtypes)

df['quarter']=df['order_date'].dt.to_period('Q')
quarter_sales=df.groupby('quarter')['sales'].sum()
quarter_sales=quarter_sales.sort_index() 

quarter_sales_median=quarter_sales.median()


plt.style.use('seaborn-v0_8-paper')
ax1.plot(quarter_sales.index.astype(str),quarter_sales.values,color="#046AF9",linewidth=2,label='Sales')

ax1.fill_between(quarter_sales.index.astype(str),quarter_sales.values,quarter_sales_median,
                 where=(quarter_sales.values>quarter_sales_median),interpolate=True,color='green',
                 alpha=0.25,label='Above Median Sales')

ax1.fill_between(quarter_sales.index.astype(str),quarter_sales.values,quarter_sales_median,
                 where=(quarter_sales.values<=quarter_sales_median),
                 interpolate=True,color='red',
                 alpha=0.25,label='Below Median Sales')

ax1.legend()
plt.tight_layout()
ax1.set_title('SALES TREND')
ax1.set_xlabel("Year-Quarter")
ax1.grid(True)
ax1.set_ylabel('Sales(USD)')
ax1.tick_params(axis='x',rotation=45)
plt.savefig('sales_trend.png')
# plt.show()
'''From This Plot , We can conclude that the sales Increased after first Quarter Of 2013
and around mid first quarter i.e around March 2013 , The sales crossed the median sales
and in the end of 2014 were at their peak.'''


#SALES IN EACH CATEGORT PLOT--

categ_sales=df.groupby('category')['sales'].sum()
ax2.bar(categ_sales.index,categ_sales.values,color='green',label='Sales',width=0.28)
ax2.legend()

ax2.set_title('SALES IN EACH CATEGORY')
ax2.set_xlabel("Category")

ax2.set_ylabel('Sales(USD)')

# plt.show()
'''From this plot, We can see that the sales from each category are quite balanced
,However, Most sales are from technology category but their is not very much difference.'''

#COUNTRIES WITH MOST SALES

country_sales=df.groupby('country')['sales'].sum()
country_sales.sort_values(ascending=False,inplace=True)

countries=[]
sales_each_country=[]

for i in range(0,16):
    countries.append(country_sales.index[i])
    sales_each_country.append(int(country_sales.values[i]))
# print(countries)
# print(sales_each_country)

countries.reverse()
sales_each_country.reverse()

ax3.barh(countries,sales_each_country,color="#F403F8")
ax3.set_title('COUNTRIES WITH MOST SALES')
ax3.set_xlabel("Sales(USD)")

ax3.set_ylabel('Countries')

# plt.show()
'''From this plot , we get insight that United States is the country with most amount of sales
and the difference between US and other countries in terms of sales is Very High.'''

#print(df['region'].unique())
region_sales=df.groupby('region')['sales'].sum()

region_sales.sort_values(ascending=False,inplace=True)

regions=[]
sales_region=[]
for value in range(0,7):
    regions.append(region_sales.index[value])
    sales_region.append(int(region_sales.values[value]))
other_region_sales=[]
for region in range(7,13):
    other_region_sales.append(int(region_sales.values[region]))

# print(sum(other_region_sales))

regions.append('Others')
sales_region.append(sum(other_region_sales))
# print(regions)
# print(sales_region)
explode=[0.1,0,0,0,0,0,0,0]
ax4.pie(sales_region,labels=regions,shadow=True,explode=explode,
         autopct='%1.1f%%',
         wedgeprops={'edgecolor':'black'})

ax4.set_title('REGIONS WITH MOST SALES')

# plt.show()
'''This plot provides us information that the central region has significant amount of sales
compared to other regions and the other regions which are not in pie chart has also good
amount of shares in sales.'''

#HISTOGRAM OF SALES DISTRIBUTION

median_sales=df['sales'].median()

bins=[0,500,1000,1500,2000,2500,3000,3500]
ax5.hist(df['sales'],bins=bins,color="#0743FA",edgecolor='black')
ax5.axvline(median_sales,color="#F90606",label='Median Sales',linewidth=2)
ax5.set_xlabel('Sales(USD)')
ax5.set_ylabel('Frequency')
ax5.set_title('SALES DISTRIBUTION')
plt.legend()
ax5.grid(True)
# plt.show()
'''This plot shows that mainly all the sales are from range 0-500 USD with over frequency
 of more than 40000 while the sales from other price ranges is very low. So this
 showcases that small value purchases have higher frequency.'''

#Sales V/S Quantity Plot

ax6.scatter(df['quantity'],df['sales'],edgecolor='black',linewidth=1)
ax6.set_title('SALES V/S QUANTITY')
ax6.set_ylabel('Sales(USD)')
ax6.set_xlabel('Quantity')
ax6.grid(True)

plt.show()
'''This plot showcases that most of the no. of sales were at lower range of sales
and the quantity of sales more than 10000USD was around 10-15 which is very low compared
to lower end of sales.'''
