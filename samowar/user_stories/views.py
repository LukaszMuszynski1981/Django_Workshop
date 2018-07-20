from django.shortcuts import render, redirect
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

button_set = '''
    <input type = 'submit' name = 'Send' value = 'Modify'>
    <input type = 'submit' name = 'Send' value = 'Add Address'>
    <input type = 'submit' name = 'Send' value = 'Add Phone'>
    <input type = 'submit' name = 'Send' value = 'Add Email'>
    <input type = 'submit' name = 'Send' value = 'Add to Group'>
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
            <input type = 'submit' name = 'Send' value = 'Send'>
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

phone_form = '''
    <form action="#" method="POST">
        <label> Phone: 
            <input type = 'text', name = 'phone'>
        </label>
        <label> Type: 
            <select name='Phone Type'>
                <option value ='1'>Private</option>
                <option value ='2'>Office</option>
            </select>
        </label>
'''

email_form = '''
    <form action="#" method="POST">
        <label> Email: 
            <input type = 'text', name = 'email'>
        </label>
        <label> Type: 
            <select name='Email Type'>
                <option value ='1'>Private</option>
                <option value ='2'>Office</option>
            </select>
        </label>
'''
show_detail_button = '''
        <label>
            <input type = 'submit' name = 'Send' value = 'Details'>
        </label>
'''

group_form = '''
    Choose group you want to assign contact 
        <label>
            <select name='Group_type'>
                <option value ='1'>Favourite</option>
                <option value ='2'>Family</option>
                <option value ='3'>Work</option>
                <option value ='4'>Other</option>
            </select>
        </label> 
'''

show_group_form = '''
    <form action="#" method="POST">
        <label> Name: 
            <input type = 'text', name = 'name'>
        </label>
        <label> Surname: 
            <input type = 'text', name = 'surname'>
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
    answer = ''

    if request.method == 'GET':
        answer = form_action + \
            person_form.format(person.name, person.surname, person.who_are_you) + \
            button_set + '<br>' + show_detail_button

    elif request.method == 'POST':

        if request.POST.get('Send') == 'Modify':
            answer = '{}/modify'.format(id)

        elif request.POST.get('Send') == 'Add Address':
            answer = '{}/addAddress'.format(id)

        elif request.POST.get('Send') == 'Add Phone':
            answer = '{}/addPhone'.format(id)

        elif request.POST.get('Send') == 'Add Email':
            answer = '{}/addMail'.format(id)

        elif request.POST.get('Send') == 'Add to Group':
            answer = '{}/addGroup'.format(id)

        elif request.POST.get('Send') == 'Details':
            ph = person.phone_set.all()
            em = person.email_set.all()
            ad = person.address_set.all()
            gr = person.group_set.all()

            answer += '<p></p>Addresses:<p></p>'
            for x in ad.iterator():
                answer += '<li>Street: {} {}/{}, City: {}'.format(x.street, x.street_no, \
                                                                  x.flat, x.city)
            answer += '<p></p>Phones:<p></p>'
            for y in ph.iterator():
                answer += '<li>{} {}'.format(y.phone, y.get_phone_type_display())

            answer += '<p></p>Emails:<p></p>'
            for z in em.iterator():
                answer += '<li><a href={}> {} </a> {}'.format(z.email, z.email, z.get_email_type_display())

            answer += '<p></p>Groups:<p></p>'
            for q in gr.iterator():
                answer += '<li>{}'.format(q.get_group_type_display())

            return HttpResponse(person_form.format(person.name, person.surname, person.who_are_you) +
                                answer)

        return redirect(answer)

    else:
        answer = 'Something went wrong'

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
        a = request.POST.get('name')
        b = request.POST.get('surname')
        c = request.POST.get('who_are_you')
        if not (a == '' or b == ''):
            per_to_mod.name = a
            per_to_mod.surname = b
            per_to_mod.who_are_you = c
            per_to_mod.save()
            answer = '''Personal date were modify. 
                    To check if they are correct click the link below<br>
                    '''
        else:
            answer = "Name or surname can't be empty"
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


@csrf_exempt
def add_phone(request, id):

    person = Person.objects.get(id=id)
    answer = ''

    if request.method == 'GET':
        answer = person_form.format(person.name, person.surname, person.who_are_you) + \
                 '<p></p>' + \
                 phone_form + \
                 button.format('Add')

    elif request.method == 'POST':
        phone = request.POST.get('phone')
        phone_type = request.POST.get('Phone Type')
        p = Phone.objects.create(phone=phone, phone_type=phone_type, person_id=person.id)
        answer = 'Phone was added'

    else:
        answer = 'Something went wrong. Check consistency of provided data'

    return HttpResponse(answer)


@csrf_exempt
def add_mail(request, id):

    person = Person.objects.get(id=id)
    answer = ''

    if request.method == 'GET':
        answer = person_form.format(person.name, person.surname, person.who_are_you) + \
                 '<p></p>' + \
                 email_form + \
                 button.format('Add')

    elif request.method == 'POST':
        email = request.POST.get('email')
        mail_type = request.POST.get('Email Type')
        e = Email.objects.create(email=email, email_type=mail_type, person_id=person.id)
        answer = 'Email was added'

    else:
        answer = 'Something went wrong. Check consistency of provided data'

    return HttpResponse(answer)


@csrf_exempt
def assign_group(request, id):

    person = Person.objects.get(id=id)
    answer = ''

    if request.method == 'GET':
        answer = form_action + group_form + button.format(' Assign: ')

    elif request.method == 'POST':
        a = request.POST.get('Group_type')
        b = Group.objects.get(group_type=a)
        b.person.add(person)
        answer = 'Group was assigned'

    else:
        answer = 'Something went wrong. Check consistency of provided data'

    return HttpResponse(answer)


@csrf_exempt
def search_group(request):

    answer = ''

    if request.method == 'GET':
        answer = show_group_form + button.format('')

    elif request.method == 'POST':

        name = request.POST.get('name')
        surname = request.POST.get('surname')
        groups = ''

        if name != '' and surname != '':
            person = Person.objects.get(name=name, surname=surname)
            groups = person.group_set.all()

        elif name == '':
            person = Person.objects.filter(surname=surname)
            groups = person.group_set.all()

        elif surname == '':
            person = Person.objects.filter(name=name)
            groups = person.group_set.all()

        else:
            answer = 'Something went wrong. Try again'

        for group in groups:
            answer += 'Group - {}<br>'.format(group.get_group_type_display())

    return HttpResponse(answer)








