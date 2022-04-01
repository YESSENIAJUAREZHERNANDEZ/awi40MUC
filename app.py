import web
import pyrebase
import firebase_config as token
import json  #incluir libreria JSON
firebase = pyrebase.initialize_app(token.firebaseConfig)
auth = firebase.auth()

urls = (
    '/', 'Login',
    '/bienvenida', 'Bienvenida', 
    '/recuperar', 'Recuperar',
    '/registrar', 'Registrar',
    '/logout','Logout'
)
app = web.application(urls, globals())
render = web.template.render("views")

class Bienvenida:
    def GET(self): # se invoca al entrar a la ruta /bienvenida
        try: # prueba el siguiente bloque de codigo
            print("Bienvenida.GET localID: ",web.cookies().get('localID')) # se imprime el valor de localID para verificarlos
            if web.cookies().get('localID') == None: # Si localID es None se redirecciona a login.html
                return render.login()  # se redirecciona al login.html
            else: # si la cookies no esta vacia 
                # Conectar con la base de datos de firebase para verificar que el usuario esta registrado, y obtener otros datos 
                return render.bienvenida() # renderiza bienvenida.html
        except Exception as error: # se atrapa algun error
            print("Error Bienvenida.GET: {}".format(error)) # se imprime el error atrapado 

class Recuperar:
    def GET(self): # se invoca al entrar a la ruta 
        try: # prueba el siguiente bloque de codigo
            print("Recuperar.GET localID: ",web.cookies().get('localID')) # se imprime el valor de localID para verificarlos
            if web.cookies().get('localID') == None: # Si localID es None se redirecciona a login.html
                return render.login()  # se redirecciona al login.html
            else: # si la cookies no esta vacia 
                # Conectar con la base de datos de firebase para verificar que el usuario esta registrado, y obtener otros datos 
                return render.recuperar() # renderiza bienvenida.html
        except Exception as error: # se atrapa algun error
            print("Error Recuperar.GET: {}".format(error)) # se imprime el error atrapado 

class Registrar:
    def GET(self): # se invoca al entrar a la ruta /bienvenida
        try: # prueba el siguiente bloque de codigo
            print("Registrar.GET localID: ",web.cookies().get('localID')) # se imprime el valor de localID para verificarlos
            if web.cookies().get('localID') == None: # Si localID es None se redirecciona a login.html
                return web.seeother("login") # se redirecciona al login.html
            else: # si la cookies no esta vacia 
                # Conectar con la base de datos de firebase para verificar que el usuario esta registrado, y obtener otros datos 
                return render.registrar() # renderiza login.html
        except Exception as error: # se atrapa algun error
            print("Error Registrar.GET: {}".format(error)) # se imprime el error

class Logout:
        def GET(self): 
            return render.login()  

class Login:
    def GET(self): # se invoca al entrar a la ruta /login
        try: # prueba el bloque de codigo
            message = None
            return render.login() # renderiza la pagina login.html 
        except Exception as error: # atrapa algun error
            message = "Error en el sistema"
            print("Error Login.GET: {}".format(error)) # se alamacena un mensaje de error ..... print("Error Login.POST: {}".format(error.args[0]))
            return render.login(message) 

    def POST(self): # se invoca al recibir el formulario
        try: # prueba el bloque de codigo 
            firebase = pyrebase.initialize_app(token.firebaseConfig) # se crea un objeto para conectarse con firebase
            auth = firebase.auth() # se crea un objeto para usar el servicios de autenticacion de firebase
            formulario = web.input() # Se crea una variable formulario para recibir los datos del login.html
            email = formulario.email # se almacena el valor de email del formulario
            password = formulario.password # se almacena el valor de password del formulario
            print(email,password) # se imprimen para verificar los valores recibidos
            user = auth.sign_in_with_email_and_password(email, password) #  autenticacion con firebase
            print(user["localId"]) # si los datos son correctos se recibe informacion del usuario imprime el localID
            web.setcookie('localID', user['localId'], 3600) # se almacena en una cookie el localID
            print("localId: ",web.cookies().get('localID')) # se imprime la cookie para verificar que se almaceno correctamente
            return web.seeother("bienvenida") # Redirecciona a otra pagina web 
        except Exception as error:
            formato = json.loads(error.args[1])
            error = formato['error'] 
            message = error['message']
            print("Error Login.POST: {}".format(message)) # se imprime el message enviado por firebase
            web.setcookie('localID', None, 3600)
            
    
if __name__ == "__main__":
    web.config.debug = False
    app.run()
    