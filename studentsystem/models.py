# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Course(models.Model):
    course_id = models.CharField(db_column='Course_id', primary_key=True, max_length=30)  # Field name made lowercase.
    course_name = models.CharField(db_column='Course_name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    course_credits = models.IntegerField(db_column='Course_credits', blank=True, null=True)  # Field name made lowercase.
    course_type = models.CharField(db_column='Course_type', max_length=2, blank=True, null=True)  # Field name made lowercase.
    lec = models.IntegerField(db_column='Lec', blank=True, null=True)  # Field name made lowercase.
    tut = models.IntegerField(db_column='Tut', blank=True, null=True)  # Field name made lowercase.
    lab = models.IntegerField(db_column='Lab', blank=True, null=True)  # Field name made lowercase.
    course_mode = models.CharField(db_column='Course_mode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    course_year = models.IntegerField(db_column='Course_year', blank=True, null=True)  # Field name made lowercase.
    course_sem = models.IntegerField(db_column='Course_sem', blank=True, null=True)  # Field name made lowercase.
    dept_name = models.ForeignKey('Department', models.DO_NOTHING, db_column='Dept_name', blank=True, null=True)  # Field name made lowercase.
    total_seats = models.IntegerField(db_column='Total_seats', blank=True, null=True)  # Field name made lowercase.
    total_enrolled = models.IntegerField(db_column='Total_enrolled', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Course'


class Department(models.Model):
    dept_name = models.CharField(db_column='Dept_name', primary_key=True, max_length=20)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hod = models.CharField(db_column='HOD', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Department'


class Enroll(models.Model):
    student = models.OneToOneField('Student', models.DO_NOTHING, db_column='Student_id', primary_key=True)  # Field name made lowercase.
    course = models.ForeignKey(Course, models.DO_NOTHING, db_column='Course_id')  # Field name made lowercase.
    course_grade = models.CharField(db_column='Course_grade', max_length=2, blank=True, null=True)  # Field name made lowercase.
    enroll_date = models.DateField(db_column='Enroll_date', blank=True, null=True)  # Field name made lowercase.
    course_status = models.CharField(db_column='Course_status', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Enroll'
        unique_together = (('student', 'course'),)


class Instructor(models.Model):
    inst_id = models.IntegerField(db_column='Inst_id', primary_key=True)  # Field name made lowercase.
    inst_name = models.CharField(db_column='Inst_name', max_length=70, blank=True, null=True)  # Field name made lowercase.
    inst_phone_no = models.CharField(db_column='Inst_phone_no', max_length=12, blank=True, null=True)  # Field name made lowercase.
    office = models.CharField(db_column='Office', max_length=20, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=70, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='Designation', max_length=20, blank=True, null=True)  # Field name made lowercase.
    instr_dob = models.DateField(db_column='Instr_DOB', blank=True, null=True)  # Field name made lowercase.
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='Dept_name', blank=True, null=True)  # Field name made lowercase.
    profile_link = models.CharField(db_column='Profile_link', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Instructor'


class Section(models.Model):
    section_type = models.CharField(db_column='Section_type', primary_key=True, max_length=3)  # Field name made lowercase.
    course = models.ForeignKey(Course, models.DO_NOTHING, db_column='Course_id')  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=20, blank=True, null=True)  # Field name made lowercase.
    section_hour = models.IntegerField(db_column='Section_hour', blank=True, null=True)  # Field name made lowercase.
    inst = models.ForeignKey(Instructor, models.DO_NOTHING, db_column='Inst_id', blank=True, null=True)  # Field name made lowercase.
    mon = models.IntegerField(db_column='Mon', blank=True, null=True)  # Field name made lowercase.
    tue = models.IntegerField(db_column='Tue', blank=True, null=True)  # Field name made lowercase.
    wed = models.IntegerField(db_column='Wed', blank=True, null=True)  # Field name made lowercase.
    thu = models.IntegerField(db_column='Thu', blank=True, null=True)  # Field name made lowercase.
    fri = models.IntegerField(db_column='Fri', blank=True, null=True)  # Field name made lowercase.
    sat = models.IntegerField(db_column='Sat', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Section'
        unique_together = (('section_type', 'course'),)


class Stream(models.Model):
    stream_id = models.IntegerField(db_column='Stream_id', primary_key=True)  # Field name made lowercase.
    degree_type = models.CharField(db_column='Degree_type', max_length=20, blank=True, null=True)  # Field name made lowercase.
    branch = models.CharField(db_column='Branch', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='Dept_name', blank=True, null=True)  # Field name made lowercase.
    duration = models.IntegerField(db_column='Duration', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Stream'


class Student(models.Model):
    student_id = models.CharField(db_column='Student_id', primary_key=True, max_length=20)  # Field name made lowercase.
    student_name = models.CharField(db_column='Student_name', max_length=70, blank=True, null=True)  # Field name made lowercase.
    enrollment_year = models.IntegerField(db_column='Enrollment_year', blank=True, null=True)  # Field name made lowercase.
    stream = models.ForeignKey(Stream, models.DO_NOTHING, db_column='Stream_id', blank=True, null=True)  # Field name made lowercase.
    student_address = models.CharField(db_column='Student_address', max_length=120, blank=True, null=True)  # Field name made lowercase.
    student_phone_no = models.CharField(db_column='Student_phone_no', max_length=20, blank=True, null=True)  # Field name made lowercase.
    student_dob = models.DateField(db_column='Student_DOB', blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(db_column='Sex', max_length=1, blank=True, null=True)  # Field name made lowercase.
    father_name = models.CharField(db_column='Father_name', max_length=70, blank=True, null=True)  # Field name made lowercase.
    current_sem = models.IntegerField(db_column='Current_sem', blank=True, null=True)  # Field name made lowercase.
    current_year = models.IntegerField(db_column='Current_year', blank=True, null=True)  # Field name made lowercase.
    degree_status = models.CharField(db_column='Degree_status', max_length=10, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Student'


