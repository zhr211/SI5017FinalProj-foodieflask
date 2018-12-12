## Data Sources Used:
#### Yelp Fusion:
* Requires an API key - How to obtain API Key:
* Create a Yelp Account here by clicking Sign Up: https://www.yelp.com/login?return_url=%2Fdevelopers%2Fv3%2Fmanage_app
* Get your API key on this page: https://www.yelp.com/developers/v3/manage_app
* Required getting more than the 20 returned

#### OpenWeathermap:

* Requires an API key - How to obtain API Key:
* API documentation:http://openweathermap.org/api
* Example of API call:api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=d9183db6b9b
b464275abb670161f6ded

#### API Secrets Location:

* My Secrets File: secrets_finalproj.py
(I have hidden this file, please apply your API key)


#### Plotly Visualizations

* How to sign up: https://plot.ly/
* Create a free account: https://plot.ly/ssu/ pip install Plotly if not already on your machine with the following command: pip install plotly
Then grab the API here: https://plot.ly/python/getting-started/
* Set up your credentials with the following: import plotly plotly.tools.set_credentials_file(username='DemoAccount', api_key='lr1c37zw81')
* Fill in username with your Plotly username
* Fill in api_key with your API key (found here :https://plot.ly/settings/api)
* For tutorials and other visualization options, go here: https://plot.ly/python/

## Brief description of code:

#### Main Function:

* get_city_restaurant(location, type, number):
This function specifies which data to get from the Yelp Fusion API
* get_city_weather(location):
This function specifies which data to get from the Openweathermap API
* init(): initiates database for csv files, which contains living cost at different locations.
* init_update_insert_db_for_job(): scraping and crawling from Yelp and Openweathermap into db and returns the required information of restaurants.
* offline_plotly():uses plotly offline module to store the plot into local directory.

#### Class Definitions
Food_intro()--make details output of category more neat


## User guide
Flask
* Run the app.py in terminal and go to http://127.0.0.1:5000/. Don't close the terminal when working on the website.
* In the main web, you can input the **location** you show interest and the **number** and **category** of restaurant. And at the bottom of website, you can also leave your message like "I recommend a restaurant called Kang Korea in Ann Arbor ", which increases interactive fun.
* Entering restaurant list website, you can see local weather information, you update your restaurant list by rating and price. Click the image, you can also check the picture of restaurant.
* Button "MAP", you will see the actual address of restaurant on the map
* If you are not sure about the type of food, you can click the restaurant's category, you will be led to another page, you can see a recommended search list, then you can type down the words you show interest for knowing further.
