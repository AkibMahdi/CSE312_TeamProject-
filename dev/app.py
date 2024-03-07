from flask import Flask, redirect, url_for , render_template
# instance of web application
app = Flask(__name__)






app.run(host="0.0.0.0", port=int(8000), debug=True)

    # where to access page - definning path to get to function
@app.route('/')
#definging pages on website- represnt what were displaying
def homepage():
    #inline html- when we return to function
    return render_template("index.html")


    return render_template("style.css")


    #return "<h2>Hello! This is our main page<h2>"


# DIRECT TO THE FUNCTION
@app.route('/PendingLogo')
def design():
    return render_template("myproject/logo.png")
#     return redirect(url_for(""))

#
# from flask import Flask, redirect, url_for , render_template
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
#
# # html rendering
#@app.route("/")
#     #definging pages on website- represnt what were displaying3
#def home():
#     #inline html- when we return to function
    #return(render_template("index.html"))
#tags like that allow you to type and pass into func and will display

#photo hosting
# pass the string of text to the user - displared on webpage
#@app.route("/<name>")
#def login(name):
    #return render_template("index.html", content=name)

    #return render_template("index.html", content=name)

    #return f"Hello {name}!"


#redirecting js?
#@app.route("/admin/")
#def admin():
    # can use if conditional to check a = False --> if a...
    # name of function inside string- to redirect too
   # return redirect(url_for("name", name= "Admin!"))









# run app
if __name__ == "__main__":
         app.run()