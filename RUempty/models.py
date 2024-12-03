from django.contrib.auth.models import AbstractUser
from django.db import models

import datetime


class Campus(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Building(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=5)

    class Meta:
        unique_together = ('campus', 'name')

    def __str__(self):
        return f"{self.campus}, {self.name}"


class Room(models.Model):
    building = models.ForeignKey(Building,  on_delete=models.CASCADE, default=None)
    number = models.CharField(max_length=10)

    class Meta:
        unique_together = ('building', 'number')

    def __str__(self):
        return f"{self.building.campus}, {self.building}, {self.number}"


class Instructor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class StartTime(models.Model):
    time = models.TimeField(unique=True)

    @property
    def stime(self):
        return self.time.isoformat(timespec='minutes')

    def __str__(self):
        return f"{self.time.isoformat(timespec='minutes')}"


class EndTime(models.Model):
    time = models.TimeField(unique=True)

    @property
    def stime(self):
        return self.time.isoformat(timespec='minutes')

    def __str__(self):
        return f"{self.time.isoformat(timespec='minutes')}"


class TimeBlock(models.Model):
    start_time = models.ForeignKey(StartTime, on_delete=models.CASCADE, default=None)
    end_time = models.ForeignKey(EndTime, on_delete=models.CASCADE, default=None)

    class Meta:
        unique_together = ('start_time', 'end_time')

    def __str__(self):
        return f"{self.start_time.stime} -> {self.end_time.stime}"


class Subject(models.Model):
    id = models.CharField(max_length=3, primary_key=True)

    def __str__(self):
        return self.id


class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=None)
    number = models.CharField(max_length=3, default=None)
    title = models.CharField(max_length=50)
    credits = models.IntegerField()
    semester = models.IntegerField(default=92023)

    @property
    def course_id(self):
        return f'{self.subject}:{self.number}'

    class Meta:
        unique_together = ('subject', 'number', 'title')

    def __str__(self):
        return f"{self.title} - ({self.subject}:{self.number})"


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections", default=None)
    section_number = models.CharField(max_length=10)

    instructors = models.ManyToManyField(Instructor, default=None, related_name="sections")

    class Meta:
        unique_together = ('course', 'section_number')

    def __str__(self):
        return f"{self.course}, Section {self.section_number}"


class MeetingTime(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, default=None, related_name="MeetingTime")
    time_block = models.ForeignKey(TimeBlock, on_delete=models.CASCADE, default=None)
    day = models.CharField(max_length=4)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None)
    # semester = models.IntegerField(default=92023)

    @property
    def location(self):
        return f"{self.room.building.campus.name}, {self.room.building.name}-{self.room.number}"

    class Meta:
        unique_together = ('time_block', 'day', 'room', 'section')

    def __str__(self):
        return f"{self.day}: ({self.room.building.campus.name} {self.room.building.name}-{self.room.number}) from " \
               f"{str(self.time_block)}"


