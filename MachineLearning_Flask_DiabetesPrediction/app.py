import os
from flask import Flask, render_template, flash, request, jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import pandas as pd                 
import matplotlib.pyplot as plt      
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn import metrics


DEBUG = True
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
path = os.path.join(SITE_ROOT, 'templates', 'diabetes.csv')
app = Flask(__name__, template_folder='templates')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
df = pd.read_csv('diabetes.csv', encoding="utf-8-sig")
feature_col_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
predicted_class_names = ['Outcome']
X = df[feature_col_names].values     # predictor feature columns (8 X m)
y = df[predicted_class_names].values # predicted class (1=true, 0=false) column (1 X m)
split_test_size = 0.30
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_test_size, random_state=42)
nb_model=SVC(kernel="linear")
nb_model.fit(X_train, y_train.ravel())
nb_predict_train = nb_model.predict(X_train)
nb_predict_test = nb_model.predict(X_test)


class ReusableForm(Form):
    pregnancies = TextField('pregnancies:', validators=[validators.required()])
    glucoselevel = TextField('glucoselevel:', validators=[validators.required()])
    skinthickness = TextField('skinthickness:', validators=[validators.required()])
    bmi = TextField('bmi:', validators=[validators.required()])
    dpf = TextField('dpf:', validators=[validators.required()])
    age = TextField('age:', validators=[validators.required()])
    bp = TextField('bp:', validators=[validators.required()])
    insulin = TextField('insulin:', validators=[validators.required()])



@app.route('/', methods=['GET', 'POST'])
def predictForm():
    form = ReusableForm(request.form)
    predicted_class_names = ['Outcome']
    print(form.errors)
    if request.method == 'POST':
        pregnancies = request.form['pregnancies']
        glucoselevel = request.form['glucoselevel']
        skinthickness = request.form['skinthickness']
        bmi = request.form['bmi']
        dpf = request.form['dpf']
        age = request.form['age']
        bp = request.form['bp']
        insulin = request.form['insulin']
        print(pregnancies, " ", glucoselevel, " ", skinthickness, " ", bmi, " ", dpf, " ", age, " ", bp, " ", insulin)

        if form.validate():
            # Save the comment here.
            flash('Thanks for registration ')
        else:
            flash('Error: All the form fields are required. ')

    return render_template('predictForm.html', form=form)


@app.route('/diabetesPredictionApi', methods=['POST'])
def diabetesPredictionApi():
    form = ReusableForm(request.form)
    # read the posted values from the UI
    pregnancies = request.form['pregnancies']
    glucose = request.form['glucoselevel']
    skinthickness = request.form['skinthickness']
    insulin = request.form['insulin']
    bmi = request.form['bmi']
    dpf = request.form['dpf']
    age = request.form['age']
    bp = request.form['bp']


    # validate the received values
    if pregnancies and glucose and skinthickness and bmi and dpf and age and bp and insulin:
        da=nb_model.predict([pregnancies,glucose,bp,skinthickness,insulin,bmi,dpf,age])
        if(da[0]==0):
            outcome="no"
        else:
            outcome="yes"
        return (outcome)
    else:

        return "values not there"


if __name__ == "__main__":
    app.run()
    





