from .models import Student, Grade, Subject
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm, GradeForm
from django.db.models import Avg

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
        
        # Вычисляем средний балл студента
        average_grade = Grade.objects.filter(student=student).aggregate(Avg('grade'))['grade__avg']
        average_grade = round(average_grade, 2) if average_grade else '-'  # Округляем до двух знаков после запятой
        
        student_statistics.append({
            'student': student,
            'scores': scores,
            'average_grade': average_grade  # Добавляем средний балл в словарь для передачи в шаблон
        })

    return render(request, 'core/dashboard.html', {
        'student_statistics': student_statistics, 
        'subjects': [subject.name for subject in subjects], 
        'selected_subject': selected_subject
    })

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StudentForm()
    
    return render(request, 'core/add_student.html', {'form': form})

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('dashboard')
    return render(request, 'core/delete_student.html', {'student': student})

def add_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = GradeForm()
    
    return render(request, 'core/add_grade.html', {'form': form})