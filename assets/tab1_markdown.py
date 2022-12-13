dashboard_desc_md = '''

After using this dashboard, you should have a clearer picture of the relationship between covid vaccination doses, efficacy and covid breakthrough rates, over time and by country.  You should &nbsp;&nbsp;be able to answer key questions such as:  
    
* Where in the world have different vaccines been administered? Are there certain vaccine manufacturers that are more popular globally than others? How about by country? Has this changed over time?
* What is the % of COVID19 vaccine doses given that are protected from infection by country and over time for different COVID19 variants? Is it higher for certain variants than others?
* What is the COVID19 breakthrough rate over time and by country for different variants?
* What can we look to help us understand the increase or decrease in breakthrough rates for different countries?
* Is there a difference in efficacy for different vaccine manufacturers and COVID19 variants? What is this difference? 
Can it help us understand the above questions?
  
---  
###### **Assumptions: NEED HELP HERE**    
* Important to note is that doses administered does not equal number of people vaccinated
* The data fed into our visualizations, including efficacy rates and vaccine doses administered has been collected and reported on accurately
* Time series data obtained from external sources missing the total vaccines administered on a specific date for specific vaccine manufacturers are assumed to have remained constant from the last recorded total. 
* First, second, and booster doses are not factored into the efficacy rates and calculations for breakthrough. The mixing 
of vaccines is also not factored into the data, calculations, and visualizations. – Probs put this one near the top since I believe the prof called this one out 
  
---  
###### **Dashboard Components**  
**Section Topics**: Each section will have a short description called **Topics** containing the topics that section answers. Look out for these when you view each section.  
  
**Guiding Questions**: Look out for tiles marked **Guiding Questions** for additional tips and/or questions to help guide you along the dashboard.  

'''

section_1_md ='''
##### **Section 1.** Understanding the Basics: *Global Prevalence of Vaccine Manufacturers*  
---  
  
**Topics:**  
* Which countries have received which vaccine types?
* What is the breakout of vaccine type by 
country?

'''

section_2_md = '''
##### **Section 2.** 
##### Going Deeper: *Country Analysis*  
---    
  
**Topics:**  
* How has the prevalence of different vaccine manufacturers changed over time?
* How has the % of doses administered that are not protected from infection changed over time and by variant? Can we use the above to help us understand why?
* How has breakthrough rate changed over time and by variant? Can we use the above questions to help us understand why this might be?

'''
perc_total_doses_by_manufacturer_md = '''
**Description**: This area chart shows the percentage of total doses administered over time by vaccine type.  
  
**Guiding Questions**:  
  
* How has the percentage total of different vaccine manufacturers changed over time? Do certain vaccine manufacturers become more or less prevalent?
* Of the vaccine manufacturers that become more or less prevalent, what do we know about their efficacy against different variants?

'''

protected_over_time_agg_md = '''
**Description:** The above line chart shows the % of total doses administered that do not offer protection from infection over time and by variant for a given country.  
  
**Guiding Questions:** NEED HELP HERE   
  
* How has the percentage of total doses administered that do not offer protection from infection changed over time? Is it different for different variants?
* How can we use what we know from the above visualization to potentially offer an explanation for the above? 

'''

breakthrough_over_time_md = '''
**Description:** This line chart shows the breakthrough rate per 100 people over time and by variant for a given country. Note that this refers to the total population, not just those have received a dose.  
  
**Guiding Questions:** NEED HELP HERE
  
* How has the breakthrough rate changed over time for different vaccine manufacturers?
* What causes breakthrough rates to increase or decrease over time? Is this related to the prevalence of certain vaccine variants and their efficacy rates?

'''

section_3_md = '''
##### **Section 3.** 
##### Understanding the Efficacy of Different Vaccine Manufacturers 
---  
'''

efficacy_md = '''
**Description:** The above is a bubble plot that shows the efficacy rate per 100 people for different vaccine manufacturers and variants.  
  
**Guiding Questions:**  
* What is the efficacy for different vaccine manufacturers and variants? Are some higher or lower than others?

'''