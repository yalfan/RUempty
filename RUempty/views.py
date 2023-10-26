import json
import requests
from datetime import datetime, date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django import forms

from .models import *
from .utils import *

days = {"Saturday": "S", "S": "Saturday", "Monday": "M", "M": "Monday", "Tuesday": "T", "T": "Tuesday",
        "Wednesday": "W", "W": "Wednesday", "Thursday": "TH", "TH": "Thursday", "Friday": "F", "F": "Friday"}


class SelectForm(forms.Form):
    """Defining form which will be rendered on the main page via WTForms."""
    dayChoices = [("Monday", 'Monday'), ("Tuesday", 'Tuesday'),
                  ("Wednesday", 'Wednesday'), ("Thursday", 'Thursday'),
                  ("Friday", 'Friday'), ("Saturday", "Saturday"),]

    # Initial choice set to prompt user to change the campus, which fires the
    # GET request which will get all buildings for that campus.
    campusChoices = [("Please choose a campus", 'Please choose a campus'),
                     ("Busch", 'Busch'), ("College Avenue", 'College Avenue'),
                     ("Cook/Douglass", 'Cook/Douglass'),
                     ("Livingston", 'Livingston')]

    # Initially set to a single option because it will be populated by the
    # client based on the chosen campus.
    defaultBuildings = [("Please choose a campus first",
                         'Please choose a campus first')]
    day = forms.ChoiceField(label="Day", choices=dayChoices,
                            widget=forms.Select(
                                attrs={'class': 'form-control'}
                            ))
    campus = forms.ChoiceField(label="Campus", choices=campusChoices,
                               widget=forms.Select(
                                   attrs={'class': 'form-control'}
                               ))
    building = forms.ChoiceField(label="Building", choices=defaultBuildings,
                                 widget=forms.Select(
                                     attrs={'class': 'form-control select-form'}
                                 ))


def index(request):
    form = SelectForm()
    return render(request, "index.html", {
        "something": "something",
        "form": form,
    })


def update_db(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("index"))
    subject = 10
    semester = 92023
    room_nums = []
    while subject <= 991:
        if len(str(subject)) == 2:
            subject = f"0{subject}"
        url = f"http://sis.rutgers.edu/oldsoc/courses.json?subject={subject}&semester={semester}&campus=NB&level=UG"
        response = requests.get(url)
        response = json.loads(response.content.decode('utf-8', 'replace'))
        if len(response) == 0:
            subject = int(subject) + 1
            continue
        subject = str(subject)
        for course in response:
            sections = course["sections"]
            # save_course(course, subject)
            for section in sections:
                meeting_times = section["meetingTimes"]
                # section_instructors = section["instructors"]
                # save_section(course["courseNumber"], subject, section["number"], section_instructors)
                for time in meeting_times:
                    # save_location(time)
                    # save_time((time["startTime"], time["endTime"]))
                    # save_meeting_time(time, course["courseNumber"], subject, section["number"])
                    if time["buildingCode"] == "ARC":
                        print(time["buildingCode"], time["roomNumber"])
        subject = int(subject) + 1

    return JsonResponse({"success": "succeeded"}, status=200)


def rooms(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    campus = request.POST["campus"].upper()
    building = request.POST["building"]
    day = days[request.POST["day"]]
    rooms = list(Room.objects.filter(building__name=building).filter(building__campus__name=campus))
    room_times = {}
    room_courses = {}
    for room in rooms:
        meeting_times = list(MeetingTime.objects.filter(room__building__campus__name=campus,
                                                        room__building__name=building,
                                                        room=room, day=day))
        meeting_times.sort(key=lambda time: time.time_block.start_time.time)
        room_times[room.number] = [[], []]

        start = StartTime.objects.get(time=datetime.time(8, 0))
        for time in meeting_times:
            instructors = list(time.section.instructors.all())
            instructors = [instructor.name for instructor in instructors]

            room_courses[f'{room.number},{time.time_block}'] = [time.section.__str__(), instructors]

            # add occupied time to room_times[room.number][0]
            room_times[room.number][0].append(time.time_block)

            # add open time to room_times[room.number][1]
            if type(start) == RUempty.models.StartTime:
                time_diff = datetime.datetime.combine(date.min, time.time_block.start_time.time) - \
                            datetime.datetime.combine(date.min, start.time)
            else:
                time_diff = datetime.datetime.combine(date.min, time.time_block.start_time.time) - \
                            datetime.datetime.combine(date.min, start.time_block.end_time.time)
            if time_diff > datetime.timedelta(0, 0, 0, 0, 30):
                if type(start) == RUempty.models.StartTime:
                    room_times[room.number][1].append(f"{start.stime} -> {time.time_block.start_time.stime}")
                else:
                    room_times[room.number][1].append(f"{start.time_block.end_time.stime}"
                                                      f" -> {time.time_block.start_time.stime}")
            start = time
        closing = EndTime.objects.get(time=datetime.time(23, 00))
        if len(meeting_times) > 0:
            last_meeting_time = meeting_times[-1]
            time_diff = datetime.datetime.combine(date.min, closing.time) - \
                        datetime.datetime.combine(date.min, last_meeting_time.time_block.end_time.time)
            if time_diff > datetime.timedelta(0, 0, 0, 0, 30):
                room_times[room.number][1].append(f"{last_meeting_time.time_block.end_time.stime} -> {closing.stime}")

    return render(request, "rooms.html", {
        "campus": request.POST["campus"],
        "building": building,
        "day": request.POST["day"],
        "room_times": room_times,
        "room_courses": json.dumps(room_courses),
    })


def get_buildings(request, campus):
    buildings = list(Building.objects.filter(campus__name=campus.upper()))
    buildings = [building.name for building in buildings]
    buildings.remove("None")
    return JsonResponse({"buildings": buildings}, status=200)


def get_classes(request):
    """
    get a json object
    {
    "day":...
    "campus":...
    "building":...
    "101": times
    "102": times
    ...
    """
    return JsonResponse({"data": "wassup"}, status=200)

