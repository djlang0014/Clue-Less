from flask import Flask

application = Flask(__name__)


@application.route('/')
def test():
    return "<h>Clue-Less Test page.<br>Developed by Creative Engineers.</h>"



#run the app
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()