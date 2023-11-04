from django.shortcuts import render
from django import forms
from .models import Student, Course
from django.shortcuts import render, redirect


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'email', 'courses']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']

# 

def students(request):
    students = Student.objects.all()
    student_form = StudentForm(request.POST or None)

    if request.method == 'POST' and student_form.is_valid():
        student_form.save()
        return redirect('students')

    return render(request, 'student.html', {'students': students, 'student_form': student_form})

def courses(request):
    courses = Course.objects.all()
    course_form = CourseForm(request.POST or None)

    if request.method == 'POST' and course_form.is_valid():
        course_form.save()
        return redirect('courses')

    return render(request, 'courses.html', {'courses': courses, 'course_form': course_form})


def details(request, student_id):
    student = Student.objects.get(pk=student_id)
    registered_courses = student.courses.all()
    all_courses = Course.objects.all()
    not_registered_courses = all_courses.exclude(id__in=registered_courses.values_list('id', flat=True))
    
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = Course.objects.get(pk=course_id)
        student.courses.add(course)
        return redirect('details', student_id=student_id)

    return render(request, 'details.html', {'student': student, 'not_registered_courses': not_registered_courses})

