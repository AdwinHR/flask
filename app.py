from flask import Flask, redirect , url_for, render_template , request , Response
import cv2
app=Flask(__name__)
import pickle
model = pickle.load(open('model.pkl', 'rb'))
import numpy as np
@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    print(prediction , final_features)

    output = round(prediction[0], 2)

    return render_template('index2.html', prediction_text='Employee Salary should be $ {}'.format(output))


@app.route('/sucess/<int:score>')
def sucess(score):
    return "your score osis" +str(score)

@app.route('/not_sucess/<int:score>')
def not_sucess(score):
    return "your score osis" +str(score)


# @app.route('/results/<int:score>')
# def results(score):
#     if score>50:return 'sucess'
#     else: return 'not_sucees'

@app.route('/results1/<int:marks>')
def results(marks):
    if marks>50:return redirect(url_for('sucess', score=marks))
    else: return redirect(url_for('not_sucess', score=marks))


@app.route('/submit', methods=['POST' , 'GET'])
def submit():
    total=0
    if request.method=='POST':
        fname=int(request.form['fname'])
        sname =int(request.form['lname'])
    total=fname + sname
    a={ 'b' :total,
       'c' :556,
       'd' : 567
       }
    return render_template('res.html', res1=a )


camera=cv2.VideoCapture(0)

def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/call')
def call():
    return render_template('video.html')

if __name__=='__main__':
    app.run(debug=True)