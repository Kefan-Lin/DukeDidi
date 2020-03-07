from django.shortcuts import render
from django.contrib.postgres.fields import ArrayField
from django.http import HttpResponse, HttpResponseRedirect,Http404
from datetime import datetime, timedelta
from django.urls import reverse
from . import models, tools
from django.core.mail import send_mail
import hashlib
import os
from django.db.models import Q
# Create your views here.


def login(request):
    invalid_user = False
    if request.method == 'POST':
        email = request.POST.get('email', None)  # None is default value
        password = request.POST.get('password', None)
        if email and password:
            try:
                user = models.User.objects.get(email=email)
            except:
                invalid_user = True
                return render(request, 'DukeDidi/login.html', {"invalid_user": invalid_user})
            p=hashlib.sha1()
            salt = user.salt
            password = str(password) + str(salt)
            p.update(password.encode(encoding='UTF-8'))
            encrypted_password = p.hexdigest()
            if user.encrypted_password == encrypted_password:
                user.is_logged_in = True
                user.save()
                request.session["user_email"] = email
                return HttpResponseRedirect(reverse('DukeDidi:dashboard'))
        invalid_user = True
        return render(request, 'DukeDidi/login.html', {"invalid_user": invalid_user})
    return render(request, 'DukeDidi/login.html', {"invalid_user": invalid_user})


def register(request):
    invalid_email = False
    if request.method == 'POST':
        email = request.POST.get('email', None)  # None is default value
        password = request.POST.get('password', None)
        invalid_email = not tools.check_email(email)
        if email and password and not invalid_email:
            p = hashlib.sha1()
            salt = os.urandom(40)
            password = str(password) + str(salt)
            p.update(password.encode(encoding='UTF-8'))
            encrypted_password=p.hexdigest()
            new_user = models.User.objects.create(encrypted_password=encrypted_password,salt=salt,email=email)
            new_user.save()
            return HttpResponseRedirect(reverse('DukeDidi:login'))
        invalid_email = True
        return render(request, 'DukeDidi/register.html', {'invalid_email': invalid_email})
    return render(request, 'DukeDidi/register.html', {'invalid_email': invalid_email})

def dashboard(request):
    try:
        user_email=request.session['user_email']
    except:
        raise Http404('You have not logged in! Please go to /DukeDidi/login')
    if request.method == 'POST':
        edit_open_ride_pk = request.POST.get('ride_pk',None)
        is_sharer_cancel = request.POST.get('cancel',None)
        is_sharer_dont_cancel = request.POST.get('dont_cancel',None)
        is_edit_open_ride = request.POST.get('edit_open_ride_submit',None)
        is_logged_out = request.POST.get('logout_button',None)

        if is_logged_out:
            curr_user = models.User.objects.get(email=request.session["user_email"])
            curr_user.is_logged_in = False
            curr_user.save()
            del request.session["user_email"]
            return HttpResponseRedirect(reverse('DukeDidi:login'))
        if is_edit_open_ride:  # Owner
            destination = request.POST.get('destination', None)
            arrival_time = tools.parse_date_time(request.POST.get('arrival_time', None))
            passenger_party_size = int(request.POST.get('passenger_party_size', None))
            vehicle_type = int(request.POST.get('vehicle_type', None))
            is_sharable = tools.sharable(request.POST.get('is_sharable', None))
            ride_to_edit = models.Ride.objects.get(pk=edit_open_ride_pk)
            ride_to_edit.destination = destination
            ride_to_edit.arrival_time = arrival_time
            ride_to_edit.remaining_size = vehicle_type - passenger_party_size
            ride_to_edit.total_size = vehicle_type
            ride_to_edit.is_sharable = is_sharable
            ride_to_edit.save()
        if is_sharer_cancel:
            ride_to_quit = models.Ride.objects.get(pk=edit_open_ride_pk)
            pair_list = tools.parse_sharer_partysize_pair(ride_to_quit.sharer_partysize_pair)
            remaining_sharer_list = tools.remaining_sharers_list(pair_list,user_email)
            ride_to_quit.sharers = remaining_sharer_list
            remaining_pair_list = tools.remaining_pair_list(pair_list,user_email)
            ride_to_quit.sharer_partysize_pair = remaining_pair_list
            ride_to_quit.remaining_size = ride_to_quit.remaining_size + tools.get_canceled_sharer_size(pair_list,user_email)
            ride_to_quit.save()
            curr_user = models.User.objects.get(email=request.session["user_email"])
            as_sharer_rides = models.Ride.objects.filter(sharers__contains=[user_email], is_completed=False)
            if not as_sharer_rides:
                curr_user.is_sharer = False
            curr_user.save()
        return render(request, 'DukeDidi/dashboard.html')
    return render(request, 'DukeDidi/dashboard.html')

def driverRegister(request):
    try:
        user_email=request.session['user_email']
    except:
        raise Http404('You have not logged in! Please go to /DukeDidi/login')
    invalid_driver = False  #invalid driver information
    curr_user = models.User.objects.get(email=user_email)
    if request.method == 'POST':
        click_register = request.POST.get('register_as_a_driver',None)

        vehicle_capacity = request.POST.get('vehicle_capacity', None)  # None is default value
        license_plate_number = request.POST.get('license_plate_number', None)
        # invalid_email = not tools.check_email(email)
        if click_register and curr_user.is_driver:
            return HttpResponse("You are already a driver!")
        if vehicle_capacity and license_plate_number and int(vehicle_capacity) <= 8 and int(vehicle_capacity) >= 1 and tools.check_license_plate_number(license_plate_number):
            new_driver = models.User.objects.get(email=request.session["user_email"])
            new_driver.is_driver = True
            new_driver.vehicle_capacity = vehicle_capacity
            new_driver.license_plate_number = license_plate_number
            new_driver.save()
            return HttpResponseRedirect(reverse('DukeDidi:dashboard'))
        invalid_driver = True
        return render(request, 'DukeDidi/driverRegister.html', {'invalid_driver': invalid_driver})
    return render(request, 'DukeDidi/driverRegister.html', {'invalid_driver': invalid_driver})

def editDriver(request):
    try:
        user_email=request.session['user_email']
    except:
        raise Http404('You have not logged in! Please go to /DukeDidi/login')
    invalid_driver = False
    if not models.User.objects.get(email=request.session['user_email']).is_driver:
        return HttpResponse("You are not a driver now!")
    if request.method == 'POST':
        new_vehicle_capacity = request.POST.get('new_vehicle_capacity', None)  # None is default value
        new_license_plate_number = request.POST.get('new_license_plate_number', None)
        if new_vehicle_capacity and new_license_plate_number and\
                int(new_vehicle_capacity) <= 8 and int(new_vehicle_capacity) >= 1\
                and tools.check_license_plate_number(new_license_plate_number):
            updated_driver = models.User.objects.get(email=request.session["user_email"])
            updated_driver.vehicle_capacity = new_vehicle_capacity
            updated_driver.license_plate_number = new_license_plate_number
            updated_driver.save()
            return HttpResponseRedirect(reverse('DukeDidi:dashboard'))
        invalid_driver = True
        return render(request, 'DukeDidi/editDriver.html', {'invalid_driver': invalid_driver})
    return render(request, 'DukeDidi/editDriver.html', {'invalid_driver': invalid_driver})

def requestRide(request):
    try:
        user_email=request.session['user_email']
    except:
        raise Http404('You have not logged in! Please go to /DukeDidi/login')
    invalid_ride = False
    if request.method == 'POST':
        destination = request.POST.get('destination', None)
        arrival_time = tools.parse_date_time(request.POST.get('arrival_time', None))
        passenger_party_size = int(request.POST.get('passenger_party_size', None))
        vehicle_type = int(request.POST.get('vehicle_type', None))
        is_sharable = tools.sharable(request.POST.get('is_sharable', None))
        if tools.not_all_none([destination, arrival_time, passenger_party_size, vehicle_type, is_sharable]) and passenger_party_size <= vehicle_type:
            new_ride = models.Ride.objects.create(owner=request.session["user_email"],
                                       is_sharable=is_sharable,
                                       remaining_size=vehicle_type-passenger_party_size,
                                       arrival_time=arrival_time,
                                       destination=destination,
                                       total_size=vehicle_type)
            new_ride.save()
            new_owner = models.User.objects.get(email=request.session["user_email"])
            new_owner.is_owner = True
            new_owner.save()
            return HttpResponseRedirect(reverse('DukeDidi:dashboard'))
        invalid_ride = True
        return render(request, 'DukeDidi/requestRide.html', {'invalid_ride': invalid_ride})
    return render(request, 'DukeDidi/requestRide.html', {'invalid_ride': invalid_ride})

def searchSharableRides(request):
    try:
        user_email=request.session['user_email']
    except:
        raise Http404('You have not logged in! Please go to /DukeDidi/login')
    invalid_search = False
    if request.method == 'POST':
        destination = request.POST.get('destination', None)
        start_time = tools.parse_date_time(request.POST.get('start_time', None))
        end_time = tools.parse_date_time(request.POST.get('end_time', None))
        passenger_party_size = int(request.POST.get('passenger_party_size', None))
        if tools.judge_legal_search_sharable(destination, start_time, end_time, passenger_party_size):
            satisfied_rides = models.Ride.objects.filter(~Q(owner=user_email),is_sharable=True, remaining_size__gte=passenger_party_size,
                                                         is_confirmed=False, is_completed=False,
                                                         arrival_time__gt=start_time, arrival_time__lt=end_time,
                                                         destination=destination)
            curr_sharer = models.User.objects.get(email=request.session["user_email"])
            curr_sharer.sharer_party_size = passenger_party_size
            # for ride in satisfied_rides:
            #     curr_sharer.candidate_sharable_rides.append(ride.pk)
            curr_sharer.save()
            return render(request,'DukeDidi/sharableRidesResults.html',{'satisfied_rides':satisfied_rides})
        invalid_search = True
        return render(request, 'DukeDidi/searchSharableRides.html', {'invalid_search': invalid_search})
    return render(request, 'DukeDidi/searchSharableRides.html', {'invalid_search': invalid_search})

def sharableRidesResults(request):
    try:
        user_email=request.session['user_email']
    except:
        raise Http404('You have not logged in! Please go to /DukeDidi/login')
    invalid_select = False
    if request.method == 'POST':
        ride_pk = request.POST.get('ride', None)
        if ride_pk:
            curr_sharer = models.User.objects.get(email=request.session["user_email"])
            joined_ride = models.Ride.objects.get(pk=ride_pk)
            joined_ride.sharers.append(request.session["user_email"])
            if joined_ride.sharer_partysize_pair:
                joined_ride.sharer_partysize_pair = joined_ride.sharer_partysize_pair + str(user_email) + ':' + str(curr_sharer.sharer_party_size) + ';'
            else:
                joined_ride.sharer_partysize_pair = str(user_email) + ':' + str(curr_sharer.sharer_party_size) + ';'
            joined_ride.remaining_size = joined_ride.remaining_size - curr_sharer.sharer_party_size
            curr_sharer.sharer_party_size = 0
            curr_sharer.is_sharer = True
            curr_sharer.save()
            joined_ride.save()
            return HttpResponseRedirect(reverse('DukeDidi:dashboard'))
        invalid_select = True
        return render(request, 'DukeDidi/sharableRidesResults.html', {'invalid_select': invalid_select})
    return render(request, 'DukeDidi/sharableRidesResults.html', {'invalid_select': invalid_select})

def viewNonCompletedRides(request):
    try:
        user_email = request.session['user_email']
    except:
        raise Http404('You have not logged in! Please go to /DukeDidi/login')
    if request.method == 'POST':
        click_view_non_completed_rides = request.POST.get('view_non_completed_rides', None)
        if click_view_non_completed_rides:
            as_owner_rides = models.Ride.objects.filter(owner=user_email, is_completed=False)
            as_sharer_rides = models.Ride.objects.filter(sharers__contains=[user_email], is_completed=False)
            user_non_completed_rides = as_owner_rides.union(as_sharer_rides)
            return render(request, 'DukeDidi/viewNonCompletedRides.html', {'user_non_completed_rides': user_non_completed_rides})
    return render(request, 'DukeDidi/dashboard.html')

def viewOpenRides(request):
    try:
        user_email = request.session['user_email']
    except:
        raise Http404('You have not logged in! Please go to /DukeDidi/login')
    if request.method == 'POST':
        click_view_open_rides = request.POST.get('view_open_rides', None)
        if click_view_open_rides:
            as_owner_rides = models.Ride.objects.filter(owner=user_email, is_completed=False, is_confirmed=False)
            as_sharer_rides = models.Ride.objects.filter(sharers__contains=[user_email], is_completed=False, is_confirmed=False)
            user_open_rides = as_owner_rides.union(as_sharer_rides)
            return render(request, 'DukeDidi/viewOpenRides.html', {'user_open_rides': user_open_rides})
    return render(request, 'DukeDidi/dashboard.html')

def editOpenRide(request):
    try:
        user_email = request.session['user_email']
    except:
        raise Http404('You have not logged in! Please go to /DukeDidi/login')
    is_owner = False
    if request.method == 'POST':
        click_edit_open_ride = request.POST.get('edit_open_ride',None)
        ride_to_edit_pk = request.POST.get('ride',None)
        ride_to_edit = models.Ride.objects.get(pk=ride_to_edit_pk)
        # curr_user = models.User.objects.get(email=user_email)
        if ride_to_edit.owner == user_email:
            is_owner = True
        return render(request, 'DukeDidi/editOpenRide.html', {'ride_to_edit': ride_to_edit, 'is_owner': is_owner})
    return render(request, 'DukeDidi/dashboard.html')

def driverDashboard(request):
    try:
        user_email = request.session['user_email']
    except:
        raise Http404('You have not logged in! Please go to /DukeDidi/login')
    curr_user = models.User.objects.get(email=user_email)
    if request.method == 'POST':
        click_driver_dashboard = request.POST.get('click_driver_dashboard', None)
        ride_to_complete_pk = request.POST.get('ride',None)
        if click_driver_dashboard:
            return render(request, 'DukeDidi/driverDashboard.html', {'curr_user_is_driver': curr_user.is_driver})
        if ride_to_complete_pk:
            ride_to_complete = models.Ride.objects.get(pk=ride_to_complete_pk)
            ride_to_complete.is_completed = True
            ride_to_complete.save()
            return render(request,'DukeDidi/driverDashboard.html', {'curr_user_is_driver': curr_user.is_driver})
    return render(request, 'DukeDidi/driverDashboard.html',{'curr_user_is_driver': curr_user.is_driver})

def driverOpenRides(request):
    try:
        user_email = request.session['user_email']
    except:
        raise Http404('You have not logged in! Please go to /DukeDidi/login')
    curr_user = models.User.objects.get(email=user_email)
    if request.method == 'POST':
        click_driver_search_open_rides = request.POST.get('click_driver_search_open_rides', None)
        if click_driver_search_open_rides:
            satisfied_rides = models.Ride.objects.filter(is_confirmed=False, is_completed=False, total_size=curr_user.vehicle_capacity)
            return render(request, 'DukeDidi/driverOpenRides.html', {'satisfied_rides': satisfied_rides})
    return render(request, 'DukeDidi/driverOpenRides.html')

def driverSelectRides(request):
    try:
        user_email = request.session['user_email']
    except:
        raise Http404('You have not logged in! Please go to /DukeDidi/login')
    pick_up_success = False
    curr_user = models.User.objects.get(email=user_email)
    if request.method == 'POST':
        picked_ride_pk = request.POST.get('ride', None)
        picked_ride = models.Ride.objects.get(pk=picked_ride_pk)
        picked_ride.driver = user_email
        picked_ride.is_sharable = False
        picked_ride.is_confirmed = True
        sharers_list = ''
        for sharer in picked_ride.sharers:
            sharers_list = sharers_list + sharer + '; '
        ride_confirmation_subject = 'Ride Confirmation.'
        ride_confirmation_content = 'Owner: ' + picked_ride.owner + '\n'\
                                    'Driver: ' + picked_ride.driver + '\n'\
                                    'License Plate Number: ' + curr_user.license_plate_number + '\n'\
                                    'Sharers: ' + sharers_list + '\n'\
                                    'Arrival Time: ' + str(picked_ride.arrival_time) + '\n'\
                                    'Destination: ' + picked_ride.destination + '\n' + '\n'\
                                    'Enjoy your ride!'
        recipients_list = picked_ride.sharers
        recipients_list.append(picked_ride.owner)
        send_mail(ride_confirmation_subject,ride_confirmation_content,'maojt1996@gmail.com',recipients_list)
        picked_ride.license_plate_number = curr_user.license_plate_number
        picked_ride.save()
        pick_up_success = True
        return render(request, 'DukeDidi/driverSelectRides.html', {'pick_up_success': pick_up_success})
    return render(request, 'DukeDidi/driverSelectRides.html', {'pick_up_success': pick_up_success})

def viewConfirmedRides(request):
    try:
        user_email = request.session['user_email']
    except:
        raise Http404('You have not logged in! Please go to /DukeDidi/login')
    curr_user = models.User.objects.get(email=user_email)
    if request.method == 'POST':
        click_view_confirmed_rides = request.POST.get('click_view_confirmed_rides', None)
        if click_view_confirmed_rides:
            as_owner_rides = models.Ride.objects.filter(owner=user_email, is_completed=False, is_confirmed=True)
            as_sharer_rides = models.Ride.objects.filter(sharers__contains=[user_email], is_completed=False, is_confirmed=True)
            user_confirmed_rides = as_owner_rides.union(as_sharer_rides)
            return render(request, 'DukeDidi/viewConfirmedRides.html', {'user_confirmed_rides': user_confirmed_rides})
    return render(request, 'DukeDidi/dashboard.html')

def driverViewConfirmedRides(request):
    try:
        user_email = request.session['user_email']
    except:
        raise Http404('You have not logged in! Please go to /DukeDidi/login')
    curr_driver = models.User.objects.get(email=user_email)
    if request.method == 'POST':
        click_driver_view_confirmed_rides = request.POST.get('click_driver_view_confirmed_rides', None)
        if click_driver_view_confirmed_rides:
            driver_confirmed_rides = models.Ride.objects.filter(driver=user_email, is_completed=False)
            return render(request, 'DukeDidi/driverViewConfirmedRides.html', {'driver_confirmed_rides': driver_confirmed_rides})