from flask import Flask, render_template, request, url_for, flash, Markup
import string
from db.model import tools_db, user_stories, work_roles
from flask_table import Table, Col, ButtonCol

app = Flask(__name__)


class SortableTable(Table):
    id = Col('ID')
    tool = Col('Tool')
    work_role = Col('Work Role')
    user_story = Col('User Story', allow_sort=False)
    vote = ButtonCol('Vote', 'upvote', text_fallback='+',allow_sort=False)
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'

        return url_for('previous_submissions', sort=col_key, direction=direction)

class Item(object):
    def __init__(self, id, tool, work_role, user_story):
        self.id = id
        self.tool = tool
        self.work_role = work_role
        self.user_story = user_story

    @classmethod
    def get_elements(cls):
        element_list = []

        for story in user_stories:
            element_list.append(Item(story['id'], story['tool'],
                                story['work_role'], story['user_story']))
        return element_list

    @classmethod
    def get_sorted_by(cls, sort, reverse=False):
        return sorted(
            cls.get_elements(),
            key=lambda x: getattr(x, sort),
            reverse=reverse)
            


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
    sort = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    table = SortableTable(Item.get_sorted_by(sort, reverse),
                                                sort_by=sort,
                                                sort_reverse=reverse)
    table_html = Markup(table.__html__())
    print(table_html)
    return render_template("previous_submissions.html", table_html=table_html)

    # return table.__html__()



@app.route("/upvote", methods=["GET", "POST"])
def upvote():
    return render_template("upvote.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/confirm_vote")
def confirm_vote():
    return render_template("confirm_vote.html")


