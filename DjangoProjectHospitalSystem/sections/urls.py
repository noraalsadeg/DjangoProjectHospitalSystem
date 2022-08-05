from django .urls import path
from  . import views
app_name= "sections"

urlspattern= [
    path("list/",views.list_employee, name="list_employee" )
]