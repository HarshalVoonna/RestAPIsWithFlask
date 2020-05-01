from flask import Flask

# print(__name__)
app = Flask(__name__)

@app.route('/')
def home():
  return "Home Page says 'Hello World!'"

app.run(port=5000)
