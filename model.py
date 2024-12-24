from mongoengine import Document, StringField, IntField, connect

connect(host="mongodb+srv://dattisai02:Dkumar02@cluster0.efrhv.mongodb.net/")


class User(Document):
    name = StringField(required=True, max_length=50)
    phone_number = StringField(required=True)
    email = StringField(required=True)








