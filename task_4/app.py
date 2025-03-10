from flask import Flask
from threading import Thread

app1 = Flask(__name__)
app2 = Flask(__name__)


@app1.route('/app11')
def app11():
    return f"app11"

@app1.route('/app12')
def app12():
    return f"app12"

@app2.route('/app21')
def app21():
    return f"app21"

@app2.route('/app22')
def app22():
    return f"app22"


def run_app1():
    app1.run(host='0.0.0.0', port=9999)

def run_app2():
    app2.run(host='0.0.0.0', port=9998)

if __name__ == '__main__':
    
    thread1 = Thread(target=run_app1)
    thread2 = Thread(target=run_app2)
    
    thread1.start()
    thread2.start()
    
    
    thread1.join()
    thread2.join()
