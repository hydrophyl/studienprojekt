from flask import Flask

app = Flask(__name__)

@app.route('/api',methods=['GET'])
def index():
    return {
        'name':'Hallo Duy'
    }

if __name__ == '__main__':
    app.run(debug=True)