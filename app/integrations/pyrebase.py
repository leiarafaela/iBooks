
import pyrebase






def SendResetPassword(email):
    config = {
    'apiKey': "AIzaSyDMAChNn_jeQKdiqwPQWOLNPiB3GX_PAtM",
    'authDomain': "ibooks-1fa58.firebaseapp.com",
    'projectId': "ibooks-1fa58",
    'storageBucket': "ibooks-1fa58.appspot.com",
    'messagingSenderId': "516281803999",
    'appId': "1:516281803999:web:31b0d833009469f4c1b56a",
    'measurementId': "G-V8JNJ11FDL",
    'databaseURL': ""
    }
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()

    user = auth.send_password_reset_email(email)
    return user



def AuthenticationByFirebase(email, senha):
    config = {
    'apiKey': "AIzaSyDMAChNn_jeQKdiqwPQWOLNPiB3GX_PAtM",
    'authDomain': "ibooks-1fa58.firebaseapp.com",
    'projectId': "ibooks-1fa58",
    'storageBucket': "ibooks-1fa58.appspot.com",
    'messagingSenderId': "516281803999",
    'appId': "1:516281803999:web:31b0d833009469f4c1b56a",
    'measurementId': "G-V8JNJ11FDL",
    'databaseURL': ""
    }
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()

    user = auth.sign_in_with_email_and_password(email,senha)
    return user



def CreateAuthenticationByFirebase(email, senha):
    config = {
    'apiKey': "AIzaSyDMAChNn_jeQKdiqwPQWOLNPiB3GX_PAtM",
    'authDomain': "ibooks-1fa58.firebaseapp.com",
    'projectId': "ibooks-1fa58",
    'storageBucket': "ibooks-1fa58.appspot.com",
    'messagingSenderId': "516281803999",
    'appId': "1:516281803999:web:31b0d833009469f4c1b56a",
    'measurementId': "G-V8JNJ11FDL",
    'databaseURL': ""
    }
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()

    user = auth.create_user_with_email_and_password(email,senha)
    return user







#print(user)