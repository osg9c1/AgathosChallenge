# CarRepairCodingChallenge
## Pre-requites
* python 2.7
* Django 1.4

##  Local Setup Environment
* Install pip
    * sudo apt-get install python-pip
* Install django 
    * sudo pip install django=1.4
* Install git
    * sudo apt-get install git
* Install numpy
    * pip install numpy

* Checkout AgathosChallenge from github
    * git clone https://github.com/osg9c1/CarRepairCodingChallenge.git
    * cd AgathosChallenge/lengthOfService
* python manage.py syncdb
* python manage.py runserver    
* Browse http://localhost:8000/admin/upload_seed    to Upload a CSV file
    * http://localhost:8000/admin/download_seed/  to Download a CSV file with randomly generated records
    * http://localhost:8000/admin/lengthOfService/shopworkflowfact/  to see ShopWorkFlowFact django admin view (admin credentials- username: admin password:password)

## Heroku Link
* The app is also setup on heroku - http://limitless-inlet-23271.herokuapp.com/admin/upload_seed/
 
 ## Assumptions
 * Every job is considered mutually independent and Length of Service is computed as Pickup Date - Dropoff Date + 1,  
 
 ## Computation of Average LOS and Ratio with National Average :
    * Average LOS  = Sum(los for each  (mechanic, repair type) ) / No. of records for (mechanic, repair type)
 
 ## Ranking Metrics:
 * Repair type : Ranking each repair type separately 
 * Ratio of Average: Ranking by ratio of average in descending order.
 
## Seed File
 * The seed file being used for every transaction is stored in lengthOfService/seed.csv. 

## Run the Calculations from UI:
 * Upload the Seed File http://localhost:8000/admin/upload_seed and submit, you can see the output in a tabular format.

## Run the Calculations from Shell:
*  place/replace the seed file as seed.csv in the lengthOfService folder
*  python manage.py shell
*  from print_to_screen import *
*  write_to_shell()
 
 
## Run the Tests
* python manage.py test lengthOfService.LosComputationTest.compute_los_test

 

    
    
