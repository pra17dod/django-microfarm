# Django Microfarm

| Metadata |                                             |
| -------- | ------------------------------------------- |
| WEP      | 0001                                        |
| Version  | 1.0                                         |
| Title    | Django Microfarm                            |
| Authors  | Prashant Dodiya <mailto:pra17dod@gmail.com> |
| Status   | Proposed                                    |
| Type     | Process                                     |

## Abstract

This proposal describes the approaches and implementation of the [Django Microfarm][1]
GSoC 2021 project. The aim is to create a tool that allows anyone to become a
market gardener, given some space. As a first step, the user will merely sign up
and enter the amount of space that they want to use. The system will then
trigger tasks that the user has to do to farm on their space efficiently. Those
tasks are triggered by simple rules e.g., Is the bed new? and may depend on
weather for e.g., Is it going to rain today? There will be other triggers also
such as if tomorrow forecast is no rain then water the plants. Thus, anyone can
be a market gardener, and this tool will be beneficial and easy to use.

## Introduction

This project is under the Sub Organization named [WeField e.V.][2]
It is a German NGO that takes regenerative and climate actions on monocultural
used Wasteland. This project will promote market gardening among the people.
They will be growing their vegetables, fruits all by themselves. They can even
sell their products as a source of passive income. To understand this project
Market Gardening and No-dig Method are essential to be understood first.

### Market Gardening

Market gardening is both a very old way to farm and a very new and popular one.
The market gardener is someone who has a small area of land. The term small can
be used compared to most large commercial farms, where acres possessed can
be in the tens of thousands. Typically small could mean anywhere from one to
a couple of acres to 50 or over. On this land, the farmer grows whatever he or
she wishes. Instead of growing it for commercial markets, produce is usually
sold at places like farmer’s markets or to small local grocery stores and
restaurants. Sometimes the market gardener maintains a sales site on their land
and sells directly to customers from the farm.

### No-Dig Gardening

No-dig gardening simply means disturbing existing soil as little as possible.
Here is one example. When starting a new garden bed, instead of digging or
tilling the site, the gardener puts layers of cardboard over the existing grass
lawn or weeds with a layer of compost or some other mulch on top and waters
everything. The idea is that the smothered grass or weeds will gradually die off
over weeks and months, and the cardboard decomposes, leaving a bed ready to
plant. When planting in subsequent years, the existing soil is left as-is and a
new layer of compost is added on top to replenish nutrients.

In this project, we are making a tool that can make anyone a market gardener.
Not everyone has very fertile land, and as we are aiming this for everyone, we
are adapting the no-dig method for gardening.

## Proposal

### Project Setup

`Django Rest Framework` for this project will be the best because the backend is
meant to be kept separate from the frontend. In the future, anyone working on
the frontend will have ease working with the APIs. For Continuous Integration, I
will prefer `Travis CI` as it is more reliable and does the job best. For the
database, `PostgreSQL` will be a great choice. For the deployment, in my opinion,
`Heroku` will be better as it has good support for Django apps, from my personal
experience. I am comfortable with any if suggested. The user Model will be
created with the following fields: `Name, Password, Email, Planting Space.`

### Database Handling

The Database is the key element. It will hold rules required for the watering
tasks, mulching, etc. Also, we need custom rules for specific items. Thus, this
can be achieved by making Custom Rule, Mulching Rule and Watering Rule. In
Django Models, there is a concept of Foreign Key so, the Custom Rule will hold
the id of the Parent Rule and thus, we can access all the rules for an
item. Below is the psuedo code of Database Structure for Watering and Mulching.

```python

class MulchingRule:
    type_of_mulching
    is_bed_new
    bed_width
    path_width
    list_of_custom_rule

# Functions for Mulching

def ask_every_bed():
    return is_bed_new

class WateringRule:
    plants_name
    timerange_to_water
    weekrange_to_water
    temprange_to_water
    water_if_rain_today
    list_of_custom_rule

# Functions for Watering

def ask_if_today_fall_in_week_range():
    return boolean

def ask_rain_for_today():
    return boolean

def if not rain for today():
    return boolean

# To add Custom Rules

class CustomRule:
    foreign_key_of_parent_rule
    rule_description
    for_numerical_value
    for_boolean_value
    for_string_value

```

As initially data is stored in csv format, we need to run a script to read
the csv and fill the database tables.

### Mulching

We need to give the information of the Compost required for the Mulching to the
user. And also about when to make the beds so that the beds are ready before the
planting season. For that, there will be a python script calculation based on
the rules predefined in the database. For e.g., if the bed is new, then mulching
need to be done. Along with the compost requirement, we need to return following
parameters to the user:

    - number of the beds affected
    - the compost required for one bed
    - date and time to prepare beds

### Weather API and Watering

The Weather API is needed to forecast the rain. If it is going to rain, then
some crops don’t need watering. There are many options available For e.g.,
[Open Weather Map API][3], [WeatherBit API][4], [AccuWeather API][5], etc. For
more accurate predictions of the weather API, we will use GPS to get the
latitude and longitude of the land because it could be on the city’s outskirts,
so using the city name  is not preferable. Almost all the weather API has the same
functionality. If any other specific requirements occur, we will look for an API
that fulfills our requirements.

There will be rules specific to a type of crop predefined in the database for
the watering tasks. After fetching the weather forecast then considering along
with the other rules, we will tell the user whether to water the farm or not.

| Area      | Rule 1      | Rule 2      | Rule 3     | Rule 4      | Rule 5     | Trigger     |
| --------- | ----------- | -------------------------- | -------------------------- | ------------------------------------------ | ----------------------------------------- | ---------------------------------------------- |
| Section 1 | 08:00-12:00 | Today is between W10 - W48 | If raining today, then no  | If no rain, ask forecast for the next rain | T < 12 ℃ then no and ask next day again   | If the forecast predicts no rain tomorrow, yes |
| Section 2 | 18:00-20:00 | Today is between W10 - W48 | If raining today, then yes | If no rain, ask forecast for the next rain | T < 8 ℃ then no and ask the next day again | If the forecast predicts no rain tomorrow, yes |

### Notifications and Admin View

The next step will be to send mail notifications for the routine tasks, e.g.,
watering, opening and closing polytunnel, etc. There will be following parameters in
an email regarding the task:

    - task name
    - duration in which it must be completed (due in a day, in a week or in a month)
    - short description
    - resources to learn more about the task
    - feedback for suggestion

This can be achieved with Django SMTP Emailbackend. Admin Views and Filters for
the specific user can be done by using Generic Views and registering in the admin file.

[1]: https://projects.coala.io/#/projects?project=django-microfarm&lang=en "Django Microfarm Proposal"
[2]: https://www.wefield.org/ "WeField Website"
[3]: https://rapidapi.com/community/api/open-weather-map "Open Weather Map API"
[4]: https://rapidapi.com/weatherbit/api/weather "WeatherBit API"
[5]: https://rapidapi.com/stefan.skliarov/api/AccuWeather "AccuWeather API"
