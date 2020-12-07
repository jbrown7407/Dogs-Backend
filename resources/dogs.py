import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

from flask_login import login_required, current_user
dog = Blueprint('dogs', 'dog')

@dog.route('/', methods=["GET"])
@login_required
def get_all_dogs():
    try:
        dogs = [model_to_dict(dog) for dog in models.Dog.select()]
        # print(dogs)
        return jsonify(data=dogs, status={'code': 200, 'message': 'Success'})
    except:
        return jsonify(data={}, status={'code': 500, 'message': 'Error getting resources'})


@dog.route('/', methods=["POST"])
def create_dogs():
    body = request.get_json()
    print(body)
    new_dog = models.Dog.create(**body)
    # same exact thing as:
    # new_dog = models.Dog.create(name=body['name'], owner=body['owner'], breed=body['breed'])
    dog_data = model_to_dict(new_dog)
    return jsonify(data=dog_data, status={'code': 200, 'message': 'Success'})

##ind show route
    @dog.route('/<id>, methods=["GET"])')
    def get_one_dog(id):
        dog + models.Dog.get_by_id(id)
        print(dog.__dict__)
        return jsonify(data=model_to_dict(dog), status={"code": 200, "message":"Success"})

#update dog
@dog.route('/<id>', methods=["PUT"])
def update_dog(id):
      payload = request.get_json()
      query = models.Dog.update(**payload).where(models.Dog.id == id)
      query.execute()
      return jsonify(data=model_to_dict(models.Dog.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})

#delete
@dog.route('/<id>', methods=["Delete"])
def delete_dog(id):
    query = models.Dog.delete().where(models.Dog.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})