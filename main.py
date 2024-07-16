from flask import Flask ,render_template,redirect,url_for,request,session,send_file
from models.users import User


app = Flask(__name__)
app.secret_key = "A_A"

application_id = "633727"
access_key = "KzqvEfxpO_OpX9EJPcsbfaCTh6mAsStbTG67gvRt1ok"
secret_key = "Xn6yHrNWNH6J11HkZo5jvzw9GLku1m5wdK46PPfu5Ck"

params = {
    "client_id": access_key,
    "per_page": 20,
    "page": 1
}




@app.route('/',methods=['GET','POST'])
def main():
    #sup_infos = infos_supplementaires , elles peuvent etres facultatives
    return render_template('home.html',sup_infos=["azerty","qwerty","01001"])


@app.route('/login',methods=['POST','GET'])
def loger():
    return render_template('login.html',sup_infos=["azerty","qwerty","01001"])

@app.route('/sign-up',methods=['GET','POST'])
def signer():
    return render_template('sign-up.html',sup_infos=["azerty","qwerty","01001"])

if __name__ == '__main__':
    app.run(debug=True)
    