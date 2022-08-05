from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

# Create your views here.

employee_list = [
    {"name" : "nora", "salary" : 4},
    {"name" : "haya", "salary " : 4}
]

@api_view('GET')
def list_employee(request: Request):

    response_data = {
        "msg" : "list of employee",
        "employee" : employee_list
    }
    return Response (response_data)