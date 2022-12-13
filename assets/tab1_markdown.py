dashboard_desc_md = '''

After using this dashboard, you should have a clearer picture of the relationship between COVID19 vaccine doses administered, efficacy and covid breakthrough rates, over time and by country.  You should &nbsp;&nbsp;be able to answer key questions such as:  
    
* Where have different vaccines been administered? Where are different vaccine manufacturers more popular than others? Has this changed over time?
* What is the % of COVID19 vaccine doses given that are protected from infection by country and over time for different COVID19 variants? Is it higher for certain variants than others?
* What is the COVID19 breakthrough rate over time and by country for different variants?
* Can we look at the above to help us understand the change in breakthrough rates for different countries?
* What is the difference in efficacy for different vaccine manufacturers and COVID19 variants?
  
---  
###### **Assumptions:**    
* First, second, and booster doses are not factored into the efficacy rates and calculations for breakthrough. The mixing of vaccines is also not factored into the data, calculations, and visualizations.
* Time series data obtained from external sources missing the total vaccines administered on a specific date for specific vaccine manufacturers are assumed to have remained constant from the last recorded total. 

'''

section_1_md ='''
##### **Section 1.** The Basics: *Global Prevalence of Vaccine Manufacturers*  
---  
  
**Visualizations**:

* World Map Graphic
* Number of Vaccine Variants by Country
* Percentage of Total Doses by Manufacturer by Country

**Topics:**  
* Which countries have received which vaccine types?
* What is the breakdown of vaccine manufacturer by 
country?

'''
section_2_md = '''
##### **Section 2.** 
##### Going Deeper: *Country Analysis*  
---    
  
**Topics:**  
* How has the prevalence of different vaccine manufacturers changed over time?
* How has the % of doses administered that are not protected from infection changed over time and by variant? Could this be related to the above question?
* How has breakthrough rate changed over time and by variant? Can we use the above questions to help us understand why this might be?

'''
perc_total_doses_by_manufacturer_md = '''
  
**Visualization**: Percentage of Total Doses by Manufacturer over Time

**Guiding Questions**:  
  
* How has the percentage total of different vaccine manufacturers changed over time? Do certain vaccine manufacturers become more or less prevalent?
* Of the vaccine manufacturers that become more or less prevalent, what do we know about their efficacy against different variants?

'''

protected_over_time_agg_md = '''
  
**Visualization**: Percentage of Total Doses Administered not Protected from Infection over Time, by Variant

**Guiding Questions:**    
  
* How has the percentage of total doses administered that do not offer protection from infection changed over time? Is it different for different variants?
* How can we use what we know from the above visualization to potentially offer an explanation for the above? 

'''

breakthrough_over_time_md = '''

**Visualization**: Breakthrough Rate per 100 People over Time, by Variant

**Guiding Questions:** 
  
* How has the breakthrough rate changed over time for different vaccine manufacturers?
* What causes breakthrough rates to increase or decrease over time? Is this related to the prevalence of certain vaccine variants and their efficacy rates?

'''

section_3_md = '''
##### **Section 3.** 
##### Efficacy of Different Vaccine Manufacturers 
---  
'''

efficacy_md = '''
  
**Visualizations**:

* Vaccine Efficacy by Variant, Manufacturer
* Table of Efficacy Rates

**Guiding Questions:**  
* What is the efficacy for different vaccine manufacturers and variants?

'''