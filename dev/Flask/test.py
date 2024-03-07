# from flask import Flask, redirect, url_for , render_template ,
# import re
#
# #redirecting user
# # instance of web application
# #render_html - help us render html template
# app = Flask(__name__)
# # run app
# # where to access page - definning path to get to function
# if __name__ == "__name__":
#     # mapping to 8080
#     app.run(host="0.0.0.0", port=int(8080), debug=True)
#
# @app.route("/")
# def return_html():
# return render_template("index.html")
#
#
# #definging pages on website- represnt what were displaying3
# def home(name):
#     #inline html- when we return to function
#     return render_template("index.html")
# #tags like that allow you to type and pass into func and will display
# #@app.route("/<name>")
# #def login(name):
#    # return render_template("index.html", content=name)
#
#     #return render_template("index.html", content=name)
#
#     #return f"Hello {name}!"
#
# # def picture(name):
# #     return <img src"{{ url_for('static',filename = 'myproject/logo.png'  }}" class="image" />
# # # @app.route("/PendingCuisineLogo/")
# # def gettingpic(picture):
# #     # can use if conditional to check a = False --> if a...
# #     # name of function inside string- to redirect too
# #     return redirect(url_for(name, name= picture()))
# @app.route("^myproject/logo.png$")
# def gettingpic(picture):
#     # Assuming the pictures are stored in a directory named 'static'
#     picture_url = url_for('static', filename='logo.png')
#     return redirect(picture_url)
#
#
#
#
# #redirecting user
# @app.route("/admin/")
# def admin():
#     # can use if conditional to check a = False --> if a...
#     # name of function inside string- to redirect too
#     return redirect(url_for("name", name= "Admin!"))



from api import app # Flask instance of the API

def test_index_route():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Testing, Flask!