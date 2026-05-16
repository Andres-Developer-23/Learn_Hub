from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from enrollment.models import Student, Course


@login_required(login_url='student_login')
def python_console(request, pk):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return redirect('student_login')

    course = get_object_or_404(Course, pk=pk, is_active=True)
    if course not in student.courses.all():
        messages.warning(request, 'Debes inscribirte al curso para acceder a su contenido.')
        return redirect('student_dashboard')

    return render(request, 'terminal/python_console.html', {
        'course': course,
        'student': student,
    })
