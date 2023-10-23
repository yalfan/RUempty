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
        return
    start_s, end_s = convert24hour(start_s, end_s)
    start_t = datetime.time(int(start_s[:2]), int(start_s[2:]))
    end_t = datetime.time(int(end_s[:2]), int(end_s[2:]))
    if end_t > start_t:
        try:
            start = StartTime(time=start_t)
            start.save()
        except django.db.utils.IntegrityError:
            start = StartTime.objects.get(time=start_t)
        try:
            end = EndTime(time=end_t)
            end.save()
        except django.db.utils.IntegrityError:
            end = EndTime.objects.get(time=end_t)
        try:
            block = TimeBlock(start_time=start, end_time=end)
            block.save()
        except django.db.utils.IntegrityError:
            return
        print("successfully saved time")


def save_location(time):
    campus_name, building_code, room_number = set_location(time)
    try:
        campus = Campus(name=campus_name)
        campus.save()
    except django.db.utils.IntegrityError:
        campus = Campus.objects.get(name=campus_name)
    try:
        building = Building(name=building_code, campus=campus)
        building.save()
    except django.db.utils.IntegrityError:
        building = Building.objects.get(name=building_code, campus=campus)
    try:
        room = Room(building=building, number=room_number)
        room.save()
        print("successfully saved room")
    except django.db.utils.IntegrityError:
        pass


def save_instructor(section_instructors):
    for i in section_instructors:
        if i is None:
            continue
        try:
            instructor = Instructor(name=i["name"])
            instructor.save()
        except django.db.utils.IntegrityError:
            pass


def save_course(course, subject):
    course_number = course["courseNumber"]
    subj = Subject.objects.get(id=subject)
    course_title = course["title"]
    if course["credits"] is None:
        course_credits = 0
    else:
        course_credits = int(course["credits"])
    course_desc = course["courseDescription"]
    if course_desc is None or course_desc == "":
        course_desc = "None"
    new_course = Course(subject=subj, number=course_number, title=course_title, credits=course_credits)

    new_course.save()


def save_meeting_time(time, course_number, subject, section_number):
    campus_name, building_code, room_number = set_location(time)
    campus = Campus.objects.get(name=campus_name)
    try:
        building = Building.objects.get(name=building_code, campus=campus)
    except Building.DoesNotExist:
        print(campus_name, building_code)
        building = Building(name=building_code, campus=campus)
        building.save()
    try:
        room = Room.objects.get(building=building, number=room_number)
    except Room.DoesNotExist:
        print(campus_name, building_code, room_number)
        room = Room(building=building, number=room_number)
        room.save()

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

    try:
        section = Section.objects.get(section_number=section_number, course__number=course_number, course__subject=subject)
    except Section.DoesNotExist:
        print(section_number, course_number, subject)
        exit()
        section = Section.objects.get(section_number=section_number, course__number=course_number, course__subject=subject)
    try:
        meeting_time = MeetingTime(day=day, time_block=block, room=room, section=section)
        meeting_time.save()
    except django.db.utils.IntegrityError:
        pass


def save_section(course_number, subject, section_number, section_instructors):
    subj = Subject.objects.get(id=subject)
    course = Course.objects.get(subject=subj, number=course_number)
    try:
        section = Section.objects.get(course=course, section_number=section_number)
    except Section.DoesNotExist:
        section = Section(course=course, section_number=section_number)
        section.save()

    for i in section_instructors:
        try:
            instructor = Instructor.objects.get(name=i["name"])
            section.instructors.add(instructor)
        except Instructor.DoesNotExist:
            temp = {"name": i["name"]}
            save_instructor([temp])
            instructor = Instructor.objects.get(name=i["name"])
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
