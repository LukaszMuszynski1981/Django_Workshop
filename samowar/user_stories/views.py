from django.shortcuts import render
import random
from user_stories.models import *
from django.http import HttpResponse, request
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.

person_form = '''
    <label>Name: {}</label><br>
    <label>Surname: {}</label><br>
    <label>Who are you: {}</label><br>
'''
id_form = '''
        <label>Id: {}<label><br>
'''
form_action = '''
    <form action="#" method="POST">
'''
base_form = '''
    <form action="#" method="POST">
        <label> Name: 
            <input type = 'text', name = 'name'>
        </label>
        <label> Surname: 
            <input type = 'text', name = 'surname'>
        </label>
        <label> Who are you:
            <input type = 'text', name = 'who_are_you'>
        </label><br>
'''
button = '''
        <label> {}
            <input type = 'submit' value = 'Send'>
        </label> 
'''
address_form = '''
    <form action="#" method="POST">
        <label> City: 
            <input type = 'text', name = 'city'>
        </label>
        <label> Poscode: 
            <input type = 'text', name = 'pos_code'>
        </label><br>
        <p></p>
        <label> Street:
            <input type = 'text', name = 'street'>
        </label>
        <label> Street #:
            <input type = 'text', name = 'street_no'>
        </label>
        <label> Flat #:
            <input type = 'text', name = 'flat_no'>
        </label>
'''


@csrf_exempt
def show_all(request):
    answer = ''
    persons = Person.objects.order_by('surname')
    for person in persons.iterator():
        answer += id_form.format(person.id) + \
                  person_form.format(person.name, person.surname, person.who_are_you) + \
                  '<p></p>'
    return HttpResponse(answer)


@csrf_exempt
def show_person(request, id):
    person = Person.objects.get(id=id)
    answer = person_form.format(person.name, person.surname, person.who_are_you)
    return HttpResponse(answer)


@csrf_exempt
def new_person(request):
    if request.method == 'GET':
        return HttpResponse(base_form + button.format('Add: '))
    else:
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        who_are_you = request.POST.get('who_are_you')
        new = Person.objects.create(name=name, surname=surname, who_are_you=who_are_you)
        last = Person.objects.last()
        return HttpResponse(person_form.format(last.name, last.surname, last.who_are_you))


@csrf_exempt
def delete(request, id):
    per_to_del = Person.objects.get(id=id)
    if request.method == 'GET':
        answer = form_action + \
                 id_form.format(per_to_del.id) + \
                 person_form.format(per_to_del.name, per_to_del.surname,
                                    per_to_del.who_are_you) + \
                 button.format('Delete: ')
    elif request.method == 'POST':
        per_to_del.delete()
        answer = 'Record was deleted'
    else:
        answer = "Something went wrong. Check all settings, persons and theirs' ID as it is unique identifier"
    return HttpResponse(answer)


@csrf_exempt
def modify_person(request, id):
    per_to_mod = Person.objects.get(id=id)
    answer = ''
    if request.method == 'GET':
        answer = person_form.format(per_to_mod.name, per_to_mod.surname, per_to_mod.who_are_you) + \
                 '<p><u>Type new values in the corresponding fields below.</u></p>' + \
                 base_form + \
                 button.format('Modify: ')
    elif request.method == 'POST':
        per_to_mod.name = request.POST.get('name')
        per_to_mod.surname = request.POST.get('surname')
        per_to_mod.who_are_you = request.POST.get('who_are_you')
        per_to_mod.save()
        answer = '''Personal date were modify. 
                    To check if they are correct click the link below<br>
                '''
    else:
        answer = 'Date were not modified. Check if provided values were correct and try again'
    return HttpResponse(answer)


@csrf_exempt
def add_address(request, id):
    person = Person.objects.get(id=id)
    answer = ''
    if request.method == 'GET':
        answer = person_form.format(person.name, person.surname, person.who_are_you) + \
                 '<p></p>' + \
                 address_form + \
                 button.format('Add')
    elif request.method == 'POST':
        pass
        c = request.POST.get('city')
        pc = request.POST.get('pos_code')
        s = request.POST.get('street')
        sn = request.POST.get('street_no')
        f = request.POST.get('flat_no')
        a = Address.objects.create(city=c, pos_code=pc, street=s, street_no=sn, flat=f,\
                                   person_id=person.id)
        answer = 'Address was added'
    else:
        answer = 'Something went wrong. Check consistency of provided data'

    return HttpResponse(answer)
