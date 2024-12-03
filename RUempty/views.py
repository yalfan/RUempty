import json
import requests
import datetime as dt
from datetime import date

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *
from .utils import *

days = {"Saturday": "S", "S": "Saturday", "Monday": "M", "M": "Monday", "Tuesday": "T", "T": "Tuesday",
        "Wednesday": "W", "W": "Wednesday", "Thursday": "TH", "TH": "Thursday", "Friday": "F", "F": "Friday"}


class SelectForm(forms.Form):
    """Defining form which will be rendered on the main page via WTForms."""
    dayChoices = [("Monday", 'Monday'), ("Tuesday", 'Tuesday'),
                  ("Wednesday", 'Wednesday'), ("Thursday", 'Thursday'),
                  ("Friday", 'Friday'), ("Saturday", "Saturday"), ]

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
    # print(type(request), request)
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("index"))
    subject = 10
    # semester = 12023
    # subject = 198
    semester = 92024
    while subject <= 991:
        # while subject < 199:
        if len(str(subject)) == 2:
            subject = f"0{subject}"
        # https://sis.rutgers.edu/oldsoc/courses.json?subject=090&semester=92024&campus=NB&level=UG
        url = f"https://sis.rutgers.edu/oldsoc/courses.json?subject={subject}&semester={semester}&campus=NB&level=UG"
        response = requests.get(url)
        response = json.loads(response.content.decode('utf-8', 'replace'))
        if len(response) == 0:
            subject = int(subject) + 1
            continue
        subject = str(subject)
        # print(f'Subject: {subject}')
        save_subject(subject)
        for course in response:
            sections = course["sections"]
            # print(f'Course: {course["title"]} ({course["courseNumber"]})')
            save_course(course, subject, semester)
            for section in sections:
                meeting_times = section["meetingTimes"]
                section_instructors = section["instructors"]
                # print(f'Meeting Times: {meeting_times}')
                # print(f'Instructors: {section_instructors}')
                save_section(course["courseNumber"], subject, section["number"], section_instructors, course["title"])
                for time in meeting_times:
                    # if time["startTime"] is not None:
                        # if time["startTime"][0] == "1" and time["startTime"][1] == "1":
                        # print(f'Time: {time["startTime"], time["endTime"], time["pmCode"]}')
                        # print(f'Converted Time: {convert24hour(time["startTime"], time["endTime"])}')
                    save_location(time)
                    save_time(time["startTime"], time["endTime"])
                    save_meeting_time(time, course["courseNumber"], subject, section["number"], semester, course["title"])
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

        temp = []
        for time in meeting_times:
            if time.time_block not in [t.time_block for t in temp]:
                temp.append(time)

        meeting_times = temp

        # room_times[room #][0] = occupied times
        # room_times[room #][1] = open times
        room_times[room.number] = [[], []]

        start = TimeBlock(start_time=StartTime(time=dt.time(8, 0)), end_time=EndTime(time=dt.time(8, 0)))
        for time in meeting_times:
            instructors = list(time.section.instructors.all())
            instructors = [instructor.name for instructor in instructors]

            time_block = time.time_block
            room_courses[f'{room.number},{time_block}'] = [str(time.section), instructors]

            # add occupied time to room_times[room.number][0]
            room_times[room.number][0].append(time_block)

            # if the time between occupied time blocks > 30 minutes, add open time
            next_start_time = dt.datetime.combine(date.min, time_block.start_time.time)
            time_diff = next_start_time - dt.datetime.combine(date.min, start.end_time.time)
            if time_diff > dt.timedelta(0, 0, 0, 0, 30):
                open_time = TimeBlock(start_time=StartTime(time=start.end_time.time),
                                      end_time=EndTime(time=time_block.start_time.time))
                room_times[room.number][1].append(open_time)

            start = time_block

        closing_time = EndTime.objects.get_or_create(time=dt.time(23, 00))[0].time
        if len(meeting_times) > 0:
            last_meeting_time = meeting_times[-1].time_block.end_time.time

            time_diff = dt.datetime.combine(date.min, closing_time) - dt.datetime.combine(date.min, last_meeting_time)
            if time_diff > dt.timedelta(0, 0, 0, 0, 30):
                open_time = TimeBlock(start_time=StartTime(time=last_meeting_time), end_time=EndTime(time=closing_time))
                room_times[room.number][1].append(open_time)

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
    # buildings.remove("None")
    return JsonResponse({"buildings": buildings}, status=200)
