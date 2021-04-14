from flask import Flask, render_template, request, url_for, flash
import string
from db.model import tools_db, user_stories, work_roles

app = Flask(__name__)

def strip_punctuation(submission):
    print(submission['feature'].translate(str.maketrans('','',string.punctuation)))
    submission['feature'] = submission['feature'].translate(str.maketrans('','',string.punctuation))
    submission['rationale'] = submission['rationale'].translate(str.maketrans('','',string.punctuation))

    return submission


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/about_user_stories")
def about_user_stories():
    return render_template("about_user_stories.html")



@app.route("/new_submission", methods=["GET", "POST"])
def new_submission():
    if request.method == "POST":

        submission = {"tool": request.form["tool"],
                      "work_role": request.form["role"],
                      "feature": request.form["feature"],
                      "rationale": request.form["rationale"]
                    }

        submission = strip_punctuation(submission)
        return render_template("confirm_submission.html", submission=submission)
    else:
        return render_template('new_submission.html', tools=tools_db, work_roles=work_roles)



@app.route("/successful_submission")
def successful_submission():
    return render_template("successful_submission.html")


@app.route("/previous_submissions")
def previous_submissions():
    return render_template("previous_submissions.html", user_stories=user_stories)


@app.route("/upvote")
def upvote():
    return render_template("upvote.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/confirm_vote")
def confirm_vote():
    return render_template("confirm_vote.html")


