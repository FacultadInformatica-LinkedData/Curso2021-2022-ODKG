# Instuction of project

## How to running project:

### I. Install all libriries:

1. ``` python3 -m pip install Flask==2.0.2 ``` - install flask
2. ``` pip install rdflib ``` - install open graph library
3. ``` pip install python-dotenv ``` - reads key-value pairs from a . env file. 
    - During development, you normally want to reload your application automatically whenever you make a change to it. You can do this by passing an environment variable in *.env* file

### II. Run the project (on MacOS):

Running these commands: 
1. ``` source venv/bin/activate ``` 
2. ``` flask run ``` 

By default, Flask will run the application you defined in app.py on port 5000. While the application is running, go to http://127.0.0.1:5000/ using your web browser.
