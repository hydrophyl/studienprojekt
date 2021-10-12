from flask import Flask
app = Flask(__name__)

@app.route('/api')
def hello_world():
    return [{'item1':'Hello, World!'},{'item2':'Hello, Duy!'}]
    

if __name__ == '__main__' :
    app.run(debug=True)