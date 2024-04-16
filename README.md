# FetcherAPI

This api can handle incoming post request, take username and password form the user, and returns their profile data along with their attendance data.

## Libraries Used

+ Flask
+ BeautifulSoup4
+ Requests
+ CORS
+ Gunicorn for WSGI

## Running

Navigate to the main folder. Activate virtualenvs if any. And then type this into the cmd

<code>flask --app:app --debug run</code>

or simple type this 

<code>python app.py</code>

Head over to your local host, nothings going to pop up. Head over to PostMan and then check the api by providing a post request. 

Provide your localhost as the url. Send out a POST request.

Should look something like this:

<code>
{ 
   "username" : "230xxx",
   "password" : "yourPassword"
} 
</code>

This should work or await an appropriate error message. 