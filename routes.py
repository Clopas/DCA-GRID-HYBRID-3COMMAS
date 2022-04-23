from flask import Flask, render_template, request
from forms import SignupForm
import credentials
from main import main
from functions import close_all, cleanup
from celeryflask import make_celery

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='amqp://',
    CELERY_RESULT_BACKEND='rpc://'
)

celery = make_celery(app)


@celery.task
def celery_close_all():
    return close_all()


# def get_or_create_eventloop():
#    try:
#        return asyncio.get_event_loop()
#    except RuntimeError as ex:
#        if "There is no current event loop in thread" in str(ex):
#            loop = asyncio.new_event_loop()
#            asyncio.set_event_loop(loop)
#            return asyncio.get_event_loop()

# firebase
app.secret_key = 'b5943ed7668424f03997a729a4d7a08adc53e59983dd6710d84bc1e4c0ac75d4'


# @app.route("/")
# def index():
#     return 'hello'  # render_template("index.html")


# @app.route("/result-run/")
# def result_run():
#    return render_template("result-run.html")
#
#
# @app.route("/result-closeall/")
# def result_close_all():
#    return render_template("result-closeall.html")
#
#
# @app.route("/result-cleanup/")
# def result_cleanup():
#    return render_template("result-cleanup.html")


@app.route("/", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template('signup.html', form=form)

        else:
            # asyncio.set_event_loop(asyncio.SelectorEventLoop())
            credentials.account_id_3commas = form.account_id_3commas_signup.data
            credentials.api_key_3commas = form.api_key_3commas_signup.data
            credentials.api_secret_3commas = form.api_secret_3commas_signup.data
            credentials.api_key_ftx = form.api_key_ftx_signup.data
            credentials.api_secret_ftx = form.api_secret_ftx_signup.data

            if form.run_button.data:
                # get_or_create_eventloop().run_until_complete(main())
                return render_template("result-run.html")

            elif form.close_all_button.data:
                result_close_all = celery_close_all.delay()
                result_close_all.ready()
                # get_or_create_eventloop().run_until_complete(close_all())
                return render_template("result-closeall.html")

            elif form.cleanup_button.data:
                # get_or_create_eventloop().run_until_complete(cleanup())
                return render_template("result-cleanup.html")

    elif request.method == "GET":
        return render_template('signup.html', form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
