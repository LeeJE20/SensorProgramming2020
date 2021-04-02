from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def flask_02():
    return render_template('flask_02.html', name='jeon’)
if __name__ == "__main__":
app.run(host='0.0.0.0', port=80, debug=True)