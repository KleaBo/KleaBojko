from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Client:

    def __init__(self, data):
        self.id = data['id']
        self.thought = data['thought']
        self.likes=data['likes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_who_liked=[]



    @classmethod
    def get_all(cls):
        query = "SELECT * FROM clients;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query)
        clients = []
        for row in results:
            clients.append( cls(row))
        return clients

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM clients WHERE id = %(client_id)s;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query,data)
        return cls( results[0] )

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO clients (thought) VALUES ( %(thought)s );'
        return connectToMySQL('dojos_and_ninjas').query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = 'UPDATE clients SET likes = %(likes)s WHERE id=%(clients_id)s;'
        return connectToMySQL('dojos_and_ninjas').query_db(query, data)

    @classmethod
    def addLike(cls, data):
        query = "INSERT INTO clients_has_users (clients_id,users_id) VALUES (%(client_id)s,%(user_id)s);"
        return connectToMySQL('dojos_and_ninjas').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM clients WHERE id = %(id)s;"
        return connectToMySQL('dojos_and_ninjas').query_db(query,data)

    @classmethod
    def getUsersWhoLiked(cls, data):
        query = "SELECT * FROM clients_has_users LEFT JOIN clients ON clients_has_users.clients_id = clients.id LEFT JOIN users ON clients_has_users.users_id = users.id WHERE clients.id = %(client_id)s;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query,data)
        myClient = Client.get_one(data)
        for row in results:
            myClient.users_who_liked.append(row['email'])
        myClient.likes=len(myClient.users_who_liked)
        print(myClient.users_who_liked)
        return myClient


    

    @staticmethod
    def validate_client(client):
        is_valid = True
       
        if len(client['thought']) < 3:
            flash("Thoughts must be at least 3 characters","thought")
            is_valid= False
       
        return is_valid