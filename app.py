from flask import Flask, render_template, request
from pymongo import MongoClient

app=Flask(__name__, template_folder='templates')

client=MongoClient('mongodb://localhost:27017')
db=client['Registration_and_Enrollment']
collection1=db['Users']
collection2=db['Courses_Registered']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registeringcourse/<course_name>/<user_name>/<phone_number>/<email>/<dor>/<amnt>')
def RegistringCourse(course_name,user_name,amnt,phone_number,email,dor):

    collection2.insert_one({
        'Course Name': course_name,
        'User Name' :user_name,
        'E-mail' : email,
        'Date of Registration' : dor,
        'Fees Paid' : amnt,
    })
    return 'Course Registered'



@app.route('/signup',methods=['GET','POST'])
def createUser():
    name=request.form['name']
    email=request.form['email']
    username=request.form['username']
    password=request.form['password']
        
    email_exists=collection1.find_one({'email': email})
    if email_exists:
        return render_template('index.html',message='Email Already Exists')
    
    username_exists=collection1.find_one({'username':username})
    if username_exists:
        return render_template('index.html',message='Username Already Exists')
    
    collection1.insert_one({
        'Name': name,
        'email': email,
        'username': username,
        'password': password,
        'No. of Courses': 0,
        'dor':{},
        'Course Name':{},
    })

    return render_template('index.html',message='Account Created Successfully! Login Now',name=name,email=email)
    
    # return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/authLogin',methods=['GET','POST'])
def authLogin():
    username=request.form['username']
    password=request.form['password']
    auth=collection1.find_one({'username':username,'password':password})

    if auth:
        return render_template('dashboard.html')
    else:
        return "Enter Correct Login Credentials"
    
if __name__=='__main__':
    app.run(debug=True)
