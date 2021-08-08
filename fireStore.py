from itertools import product
from typing import Any
from pyasn1.type.univ import Integer
import pyrebase
from requests.api import put
from six import integer_types, string_types 

firebaseConfig={
    'apiKey': "AIzaSyCnk43YOREq6cJh3sIxNztlYqmxRQKN07U",
    'authDomain': "fir-python-15061.firebaseapp.com",
    'databaseURL': "https://fir-python-15061.firebaseio.com",
    'projectId': "fir-python-15061",
    'storageBucket': "fir-python-15061.appspot.com",
    'messagingSenderId': "1016641562728",
    'appId': "1:1016641562728:web:909fb58a1c6958f7f873dd",
    'measurementId': "G-3HP6MVYYHC"}
firebase = pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()
storage=firebase.storage()
defaultUser= auth.sign_in_with_email_and_password("default@mysecret.com","237y7w8ey87r3")

def getUserImg(uid):
    return storage.child("user"+ str(uid)+".png").get_url(defaultUser["idToken"])

def putUserImG(uid):
    storage.child("user"+ str(uid)+".png").put("user"+str(uid)+".png")

    
def getProductImg(pid):
    return storage.child("product"+str(pid)+".png").get_url(defaultUser["idToken"])

def putProductImg(pid):
    storage.child("product"+str(pid)+".png").put("product"+str(pid)+".png")

def putDefaultImg(uid):
    storage.child("user"+ str(uid)+".png").put("user.png")


