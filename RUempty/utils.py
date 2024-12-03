import datetime

import django.db.utils

import RUempty.models
from .models import *


def convert24hour(start, end):
    if start == "None" or end == "None" or start is None or end is None:
        return None, None
    first2digits_start = start[:2]
    first2digits_end = end[:2]
    if int(first2digits_start) < 8:
        first2digits_start = int(first2digits_start) + 12
        first2digits_end = int(first2digits_end) + 12
    elif int(first2digits_end) < 8:
        first2digits_end = int(first2digits_end) + 12
    new_start = str(first2digits_start) + start[2:]
    new_end = str(first2digits_end) + end[2:]
    return new_start, new_end


def save_time(start_s, end_s):
    if start_s is None or end_s is None:
        start_s = "0000"
        end_s = "0000"
    else:
        start_s, end_s = convert24hour(start_s, end_s)
    start_t = datetime.time(int(start_s[:2]), int(start_s[2:]))
    end_t = datetime.time(int(end_s[:2]), int(end_s[2:]))
    start, _ = StartTime.objects.get_or_create(time=start_t)
    end, _ = EndTime.objects.get_or_create(time=end_t)
    TimeBlock.objects.get_or_create(start_time=start, end_time=end)


def save_location(time):
    campus_name, building_code, room_number = set_location(time)
    campus, _ = Campus.objects.get_or_create(name=campus_name)
    building, _ = Building.objects.get_or_create(name=building_code, campus=campus)
    Room.objects.get_or_create(building=building, number=room_number)


def save_instructor(section_instructors):
    for i in section_instructors:
        if i is None:
            continue
        Instructor.objects.get_or_create(name=i["name"])


def save_subject(subject):
    Subject.objects.get_or_create(id=subject)


def save_course(course, subject, semester):
    subj = Subject.objects.get(id=subject)
    course_number = course["courseNumber"]
    course_title = course["title"]
    if course["credits"] is None:
        course_credits = 0
    else:
        course_credits = int(course["credits"])

    Course.objects.get_or_create(subject=subj, number=course_number, title=course_title, credits=course_credits,
                    semester=semester)


def save_meeting_time(time, course_number, subject, section_number, semester, course_title):
    campus_name, building_code, room_number = set_location(time)
    campus = Campus.objects.get(name=campus_name)
    building, _ = Building.objects.get_or_create(name=building_code, campus=campus)
    room, _ = Room.objects.get_or_create(building=building, number=room_number)

    start_s, end_s = convert24hour(time["startTime"], time["endTime"])
    if start_s is None or end_s is None:
        start_s = "0000"
        end_s = "0000"
    start_t = datetime.time(int(start_s[:2]), int(start_s[2:]))
    end_t = datetime.time(int(end_s[:2]), int(end_s[2:]))
    start = StartTime.objects.get(time=start_t)
    end = EndTime.objects.get(time=end_t)
    block = TimeBlock.objects.get(start_time=start, end_time=end)

    day = time["meetingDay"]
    if day is None:
        day = "None"

    section, _ = Section.objects.get_or_create(section_number=section_number, course__number=course_number,
                                  course__subject=subject, course__semester=semester, course__title=course_title)

    meeting, _ = MeetingTime.objects.get_or_create(day=day, time_block=block, room=room, section=section,
                                                   section__course__semester=semester)


def save_section(course_number, subject, section_number, section_instructors, course_title):
    subj = Subject.objects.get(id=subject)
    course = Course.objects.get(subject=subj, number=course_number, title=course_title)

    section, _ = Section.objects.get_or_create(course=course, section_number=section_number)

    for i in section_instructors:
        instructor, _ = Instructor.objects.get_or_create(name=i["name"])
        section.instructors.add(instructor)


def set_location(time):
    if time["campusName"] is None:
        campus_name = "HOURS BY ARRANGEMENT"
        building_code = "HOURS BY ARRANGEMENT"
        room_number = "HOURS BY ARRANGEMENT"
    elif time["campusName"] == "** INVALID **":
        campus_name = "ASYNCHRONOUS"
        building_code = "ASYNCHRONOUS"
        room_number = "ASYNCHRONOUS"
    else:
        campus_name = time["campusName"]
        building_code = time["buildingCode"]
        room_number = time["roomNumber"]
    if building_code is None:
        building_code = "None"
    if room_number is None:
        room_number = "None"
    return campus_name, building_code, room_number
