from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clone.db"
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Post %r>" % self.id

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == "POST":
        post_content = request.form['content']
        post = Post(content=post_content)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect("index")
        except:
            return "There was an error adding post"
    
    posts = Post.query.order_by(Post.date_created).all()
    return render_template("index.jade",posts=posts)
    

if __name__ == "__main__":
    app.run(debug=True)

