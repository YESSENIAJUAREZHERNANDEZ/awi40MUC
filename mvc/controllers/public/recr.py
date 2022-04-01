import web
import pyrebase
import firebase_config as token
import json  #incluir libreria JSON
firebase = pyrebase.initialize_app(token.firebaseConfig)
auth = firebase.auth()

urls = (
    '/recuperar', 'Recuperar'
)
app = web.application(urls, globals())
render = web.template.render('views')

class Recuperar:
    def GET(self):
        return render.recuperar()

    def POST(self):
        firebase = pyrebase.initialize_app(token.firebaseConfig) # se crea un objeto para conectarse con firebase
        auth = firebase.auth()
        formulario = web.input()
        email = formulario.email
        print(email)
        user = auth.send_password_reset_email(email)
        print(user)
        return render.recuperar()

if __name__ == "__main__":
    app.run()
