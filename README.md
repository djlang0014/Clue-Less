# Clue-Less
Repository for the Clue-Less game, a lite version of the traditional Clue game. This game was developed for JHU WSE's Foundations of Software Engineering course.

## Required Programs
PostgreSQL must be installed for psycopg to function. Additionally, a database must be restored from the Skeletal file which pgAdmin4, a tool included in the PostgreSQL installation, is able to do.
https://www.postgresql.org/download/

### How-To
(Disclaimer: these steps are what I have taken on my Linux/Ubuntu computer.  Steps may differ for Mac or Windows)
1. It is assumed you have already cloned the Clue-Less GitHub repo and have a terminal open in the top folder of the repo folder structure.  It is also highly recommended to run `git pull` before editing the project.

2. It is recommended to set up a virtual environment.  You can do so by running
```
python -m venv ./<venv name>
```
where "<venv name>" should be replaced by the name of your virtual environment.  I recommend naming it either `env` or `venv`.  If you name it anything else, please add the name to the end of the `.gitignore` file.
After your virtual environment has been created, you can activate it by running
```
source <venv name>/bin/activate
```
3. Ensure you have the required dependencies. In order to install the required dependencies, run
```
pip install -r requirements.txt
```
If it is necessary to download new dependencies during development, you can update the dependencies file by running
```
pip freeze > requirements.txt
```
Please only run the above command if you are in a virtual environment created exclusively for this project.  Otherwise, add the dependency manually to the `requirements.txt` file.

4. Run the server locally by calling
```
python application.py
```
After starting the server, the console will include a link to the front-end, typically at `http://127.0.0.1:8000`.  There you can see and test the project.

5. Push to GitHub.  Once you have made your updates, run the following:
```
git add .
git commit -m "commit message here, normally describing what you updated"
git push
```
I am still working on getting the CI/CD pipeline up-and-running to test this on AWS.  Until then, please use the local server option in step 4 to test your code.
(Guidance will be provided in the future regarding git commands to use during development, including how to create a new branch, and how to merge).
