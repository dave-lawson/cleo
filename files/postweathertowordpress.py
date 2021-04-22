#!/bin/env python3
import requests
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

# This is the specific location for Chicago with its WOEID
# This could also be pretty trivially fetched via the API's query
# but that's really just adding abstraction without value
# unless you're adding some parameters or otherwise making this dynamic
url = 'https://www.metaweather.com/api/location/2379574/'

weather = requests.get(url).json()

# This is a forecast, the first element of consolidate_weather is the current conditions
weather_state = weather['consolidated_weather'][0]['weather_state_name']
# And we can use the abbreviation to pull an image
weather_abbr = weather['consolidated_weather'][0]['weather_state_abbr']
weather_icon = 'https://www.metaweather.com/static/img/weather/{!s}.svg'.format(weather_abbr)
weather_date = weather['consolidated_weather'][0]['applicable_date']

# This is a bit gross, in prod we'd pull these out of another file with tighter permissions
# but since it's templated out, it's a bit six of one, half dozen of the other for a POC.
wp = Client('http://localhost/xmlrpc.php', '{{ wp_admin_user }}', '{{ wp_admin_password }}')
post = WordPressPost()
post.title = 'Weather for Chicago, IL - {}'.format(weather_date)
post.content = 'The current weather in Chicago is {}'.format(weather_state)
post.content = post.content + '<img src="{}">'.format(weather_icon)
post.post_status = 'publish'
post.id = wp.call(NewPost(post))
