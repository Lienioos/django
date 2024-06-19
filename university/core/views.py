from .models import Student, Grade, Subject
from django.shortcuts import render



def dashboard(request):
    subjects = Subject.objects.all()
    selected_subject = request.GET.get('subject')
    
    if selected_subject:
        selected_subject_instance = Subject.objects.get(name=selected_subject)
        grades = Grade.objects.filter(subject=selected_subject_instance)
        students = Student.objects.filter(id__in=grades.values('student'))
    else:
        students = Student.objects.all()
    
    student_statistics = []

    for student in students:
        grades = Grade.objects.filter(student=student)
        subject_grades = {grade.subject.name: grade.grade for grade in grades}
        scores = [subject_grades.get(subject.name, '-') for subject in subjects]
        student_statistics.append({
            'student': student,
            'scores': scores
        })

    return render(request, 'core/dashboard.html', {
        'student_statistics': student_statistics, 
        'subjects': [subject.name for subject in subjects], 
        'selected_subject': selected_subject
    })

