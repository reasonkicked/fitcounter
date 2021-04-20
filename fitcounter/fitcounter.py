from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

def main():
    pass



if __name__ == "__main__":
    main()
    #  print("File one executed when ran directly")