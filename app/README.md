# About COVID-19 Nursing Home Dashboard App
COVID-19 Nursing Home Dashboard app was created to visualize COVID-19 Nursing Home Dataset from the Centers for Medicare & Medicaid Services.

Dataset source: https://data.cms.gov/Special-Programs-Initiatives-COVID-19-Nursing-Home/COVID-19-Nursing-Home-Dataset/s2uc-8wxp

This app was designed to be hosted on free tier Heroku. Because RAM and HDD are limited on Heroku, we decided to generate plotly graphs as html files and load up those visualizations. 

If you are planning to host this app on free tier Heroku, make sure `data` directory is not on the root folder where app.py is located. 

# Installation Process

Before running Heroku CLI, run generate_plotly.py on command line to generate plotly graphs on `datasets` folder. 

```
python generate_plotly.py
```

## Step 1:
Install Heroku CLI.

## Step 2:
Login to Heroku CLI.

```
$ heroku login
```

## Step 3:
Create new app on Heroku website.

## Step 4: 
Replace [app-name] with the name of the app.
`my-project` should be the directory where `app.py` is located.

```
$ cd my-project/
$ git init
$ heroku git:remote -a [app-name]
```

## Step 5:
```
$ git add .
$ git commit -am "make it better"
$ git push heroku master
```