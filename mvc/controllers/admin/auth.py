import web
import pyrebase
import firebase_config as token
firebase = pyrebase.initialize_app(token.firebaseConfig)
auth = firebase.auth()
db = firebase.database()
urls = (
    '/registrar', 'Registrar'
)
app = web.application(urls, globals())
render = web.template.render('views')


class Registrar:
    def GET(self):
        return render.registrar()

    def POST(self):
        formulario = web.input()
        auth = firebase.auth()
        db = firebase.database()
        name = formulario.name
        phone = formulario.phone
        email = formulario.email
        password = formulario.password
        print(email,password)
        user = auth.create_user_with_email_and_password(email, password)
        print('localId: ',user['localId'])
        data ={
            "name": name,
            "phone": phone,
            "email": email
        }
        results = db.child("users").child(user['localId']).set(data)
        print(results)

        return render.registrar()
    
if __name__ == "__main__":
    app.run()

