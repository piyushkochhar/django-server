from django.http import JsonResponse
from django.shortcuts import render
from django.core.files import File

# third-party import
from rest_framework.response import Response
from rest_framework.views import APIView


import os
from django.conf import settings
import json


class TestView(APIView):
    def get(self, request, *args, **kwargs):
        if 'phone' in request.query_params:
            phone = request.query_params["phone"]
            if(len(phone) == 10):
                path = os.path.join(settings.BASE_DIR, "users", phone+'.json')
                if os.path.exists(path):
                    f = open(path, "r")
                    return Response(json.loads(f.read()))
                else:
                    return Response({'Error': "User Doesn't Exist"}, 400)
            else:
                return Response({'Error': "Invalid Phone"}, 400)
        else:
            return Response({'Error': "Phone doesn't exist"}, 400)

    def post(self, request, *args, **kwargs):
        if (len(request.data['phone']) == 10):
            if('firstName' in request.data and 'lastName' in request.data and 'password' in request.data):
                path = os.path.join(settings.BASE_DIR,
                                    "users", request.data['phone']+'.json')
                if not os.path.exists(path):
                    f = open(path, "a+")
                    f.write(json.dumps(request.data))
                    f.close()
                    return Response({'status': "User Created Successfully"})
                else:
                    return Response({'Error': "User Already Exists"}, 400)
            else:
                return Response({'Error': "Missing fields"}, 400)
        else:
            return Response({'Error': "Invalid Phone"}, 400)

    def put(self, request, *args, **kwargs):
        if (len(request.data['phone']) == 10):
            if('firstName' in request.data or 'lastName' in request.data or 'password' in request.data):
                path = os.path.join(settings.BASE_DIR,
                                    "users", request.data['phone']+'.json')
                if os.path.exists(path):
                    f = open(path, "r")
                    userData = json.loads(f.read())
                    if('firstName' in request.data):
                        userData['firstName'] = request.data['firstName']

                    if('lastName' in request.data):
                        userData['lastName'] = request.data['lastName']

                    if('password' in request.data):
                        userData['password'] = request.data['password']
                    f.close()
                    f = open(path, "w")
                    f.write(json.dumps(userData))
                    f.close()
                    return Response({'status': "User Updated Successfully"})
                else:
                    return Response({'Error': "User Doesn't Exist"}, 400)
            else:
                return Response({'Error': "Missing fields"}, 400)
        else:
            return Response({'Error': "Invalid Phone"}, 400)

    def delete(self, request, *args, **kwargs):
        if 'phone' in request.query_params:
            phone = request.query_params["phone"]
            if(len(phone) == 10):
                user = os.path.join(settings.BASE_DIR,
                                    "users", phone+'.json')
                if os.path.exists(user):
                    os.remove(user)
                    return Response({'status': "User Deleted Successfully"})
                else:
                    return Response({'Error': "Deletion Error"}, 400)
            else:
                return Response({'Error': "Invalid Phone"}, 400)
        else:
            return Response({'Error': "Phone doesn't exist"}, 400)
