Student Management System

A Django-based comprehensive student management system designed for educational institutions to efficiently manage student data, academic records, and administrative processes.

🌟 Features

Core Management Features

Student Information Management: Complete student profiles with personal, academic, and contact information
Course & Class Management: Organize courses, classes, and academic schedules
Attendance Tracking: Daily attendance recording and monitoring
Grade Management: Academic performance tracking and report card generation
Teacher Management: Faculty information and assignment tracking
Academic Calendar: Schedule management for exams, holidays, and events
Administrative Features

User Role Management: Different access levels for admin, teachers, students, and parents
Report Generation: Automated reports for attendance, grades, and performance
Notification System: Alerts for important dates and announcements
Fee Management: Track student fees and payments
Library Integration: Book issuance and return tracking
Transport Management: Bus routes and transportation details
🛠️ Technology Stack

Backend

Python 3.8+
Django 4.x - High-level Python web framework
Django REST Framework - For API development
PostgreSQL/MySQL - Production database
SQLite - Development database (default)
Frontend

HTML5 - Primary markup language (97.4% of codebase)
CSS3 - Styling and layout (1.3% of codebase)
JavaScript - Client-side interactivity
Bootstrap 5 - Responsive design framework
jQuery - Enhanced JavaScript functionality
Additional Components

Pillow - Image processing for student photos
ReportLab - PDF report generation
Django Crispy Forms - Form styling and layout
Django Filter - Advanced filtering capabilities
Celery - Background task processing (optional)
📋 Prerequisites

Before installation, ensure you have:

Python 3.8 or higher installed
pip (Python package manager)
Virtual environment tool (venv, virtualenv, or conda)
Git for version control
Database system (SQLite for development, PostgreSQL for production)
🚀 Installation & Setup

1. Clone the Repository

bash
git clone https://github.com/sksagor/student-management-system-main.git
cd student-management-system-main
2. Set Up Virtual Environment

bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
3. Install Dependencies

bash
pip install -r requirements.txt
If requirements.txt is not provided, install essential packages:

bash
pip install django pillow django-crispy-forms django-filter reportlab
4. Configure Environment

bash
# Copy environment template
cp .env.example .env
# Edit .env with your settings
Sample .env configuration:

env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
5. Database Setup

bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
6. Load Sample Data (Optional)

bash
python manage.py loaddata fixtures/sample_data.json
7. Run Development Server

bash
python manage.py runserver
Visit http://localhost:8000 in your browser.

📁 Project Structure

Based on the repository structure:

text
student-management-system-main/
├── SAMandSAM/               # Main Django project directory
├── Home/                    # Main application directory
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   ├── static/              # CSS, JS, images
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── urls.py             # URL routing
│   └── admin.py            # Admin configuration
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
🔧 Key Components

Database Models

python
# Sample models for the student management system
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    enrollment_date = models.DateField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='students/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    credit_hours = models.IntegerField()
    department = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)
    
    class Meta:
        unique_together = ['student', 'course', 'semester', 'academic_year']
    
    def __str__(self):
        return f"{self.student.student_id} - {self.course.code}"

class Grade(models.Model):
    GRADE_CHOICES = [
        ('A', 'A (90-100)'),
        ('B', 'B (80-89)'),
        ('C', 'C (70-79)'),
        ('D', 'D (60-69)'),
        ('F', 'F (Below 60)'),
    ]
    
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='grade')
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f"Grade {self.grade} for {self.enrollment}"
View Examples

python
# Sample views for student management
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Student, Course, Enrollment
from .forms import StudentForm, EnrollmentForm

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'Home/student_list.html'
    context_object_name = 'students'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Student.objects.all().order_by('last_name', 'first_name')
        
        # Filter by search query
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                models.Q(first_name__icontains=search_query) |
                models.Q(last_name__icontains=search_query) |
                models.Q(student_id__icontains=search_query) |
                models.Q(email__icontains=search_query)
            )
        
        return queryset

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'Home/student_detail.html'
    context_object_name = 'student'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = self.object.enrollments.all()
        context['grades'] = Grade.objects.filter(enrollment__student=self.object)
        return context

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'Home/student_form.html'
    success_url = '/students/'
    
    def form_valid(self, form):
        # Generate unique student ID
        year = datetime.now().year
        last_student = Student.objects.filter(
            student_id__startswith=f"STU{year}"
        ).order_by('-student_id').first()
        
        if last_student:
            last_number = int(last_student.student_id[7:])
            new_number = last_number + 1
        else:
            new_number = 1
        
        form.instance.student_id = f"STU{year}{new_number:04d}"
        return super().form_valid(form)
🎓 Core Features Implementation

Attendance Management

python
# Attendance tracking system
from django.db import models
from django.utils import timezone

class Attendance(models.Model):
    ATTENDANCE_STATUS = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('E', 'Excused'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=1, choices=ATTENDANCE_STATUS, default='P')
    remarks = models.CharField(max_length=200, blank=True)
    
    class Meta:
        unique_together = ['student', 'course', 'date']
    
    def __str__(self):
        return f"{self.student} - {self.course} - {self.date} - {self.get_status_display()}"
    
    @classmethod
    def mark_attendance(cls, course_id, date, attendance_data):
        """
        Bulk mark attendance for a course
        attendance_data: list of tuples (student_id, status, remarks)
        """
        course = get_object_or_404(Course, id=course_id)
        
        for student_id, status, remarks in attendance_data:
            student = get_object_or_404(Student, id=student_id)
            
            attendance, created = cls.objects.update_or_create(
                student=student,
                course=course,
                date=date,
                defaults={'status': status, 'remarks': remarks}
            )
        
        return True
Grade Calculation

python
# Grade calculation utilities
def calculate_grade(marks):
    """Calculate letter grade based on marks"""
    if marks >= 90:
        return 'A'
    elif marks >= 80:
        return 'B'
    elif marks >= 70:
        return 'C'
    elif marks >= 60:
        return 'D'
    else:
        return 'F'

def generate_report_card(student_id, semester, academic_year):
    """Generate comprehensive report card for a student"""
    student = get_object_or_404(Student, id=student_id)
    
    enrollments = Enrollment.objects.filter(
        student=student,
        semester=semester,
        academic_year=academic_year
    ).select_related('course', 'grade')
    
    total_credits = 0
    total_points = 0
    
    report_data = []
    for enrollment in enrollments:
        if hasattr(enrollment, 'grade'):
            grade_obj = enrollment.grade
            course = enrollment.course
            
            # Calculate grade points (A=4, B=3, C=2, D=1, F=0)
            grade_points = {
                'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0
            }.get(grade_obj.grade, 0)
            
            total_credits += course.credit_hours
            total_points += grade_points * course.credit_hours
            
            report_data.append({
                'course_code': course.code,
                'course_name': course.name,
                'credit_hours': course.credit_hours,
                'marks': grade_obj.marks,
                'grade': grade_obj.grade,
                'remarks': grade_obj.remarks,
            })
    
    # Calculate GPA
    gpa = total_points / total_credits if total_credits > 0 else 0
    
    return {
        'student': student,
        'semester': semester,
        'academic_year': academic_year,
        'courses': report_data,
        'total_credits': total_credits,
        'gpa': round(gpa, 2),
        'generated_date': timezone.now().date(),
    }
🌐 URL Routing

python
# Home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Home and dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Student management
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/add/', views.StudentCreateView.as_view(), name='student_add'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_edit'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),
    
    # Course management
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/add/', views.CourseCreateView.as_view(), name='course_add'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    
    # Enrollment management
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/add/', views.EnrollmentCreateView.as_view(), name='enrollment_add'),
    
    # Attendance management
    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),
    
    # Grade management
    path('grades/', views.GradeListView.as_view(), name='grade_list'),
    path('grades/add/', views.GradeCreateView.as_view(), name='grade_add'),
    path('grades/report-card/', views.generate_report_card_view, name='report_card'),
    
    # User authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
🎨 Frontend Templates Structure

html
<!-- Sample student list template -->
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Student List</h3>
                    <div class="card-tools">
                        <a href="{% url 'student_add' %}" class="btn btn-primary">
                            <i class="fas fa-plus"></i> Add New Student
                        </a>
                    </div>
                </div>
                
                <div class="card-body">
                    <!-- Search form -->
                    <form method="get" class="mb-3">
                        <div class="input-group">
                            <input type="text" 
                                   name="search" 
                                   class="form-control" 
                                   placeholder="Search students..." 
                                   value="{{ request.GET.search }}">
                            <div class="input-group-append">
                                <button class="btn btn-outline-secondary" type="submit">
                                    <i class="fas fa-search"></i>
                                </button>
                            </div>
                        </div>
                    </form>
                    
                    <!-- Student table -->
                    <div class="table-responsive">
                        <table class="table table-bordered table-hover">
                            <thead>
                                <tr>
                                    <th>Student ID</th>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Phone</th>
                                    <th>Enrollment Date</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for student in students %}
                                <tr>
                                    <td>{{ student.student_id }}</td>
                                    <td>
                                        <a href="{% url 'student_detail' student.pk %}">
                                            {{ student.first_name }} {{ student.last_name }}
                                        </a>
                                    </td>
                                    <td>{{ student.email }}</td>
                                    <td>{{ student.phone }}</td>
                                    <td>{{ student.enrollment_date|date:"M d, Y" }}</td>
                                    <td>
                                        <a href="{% url 'student_detail' student.pk %}" 
                                           class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                        <a href="{% url 'student_edit' student.pk %}" 
                                           class="btn btn-sm btn-warning">
                                            <i class="fas fa-edit"></i>
                                        </a>
                                    </td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="6" class="text-center">
                                        No students found.
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    
                    <!-- Pagination -->
                    {% if is_paginated %}
                    <nav aria-label="Page navigation">
                        <ul class="pagination justify-content-center">
                            {% if page_obj.has_previous %}
                            <li class="page-item">
                                <a class="page-link" 
                                   href="?page={{ page_obj.previous_page_number }}{% if request.GET.search %}&search={{ request.GET.search }}{% endif %}">
                                    Previous
                                </a>
                            </li>
                            {% endif %}
                            
                            {% for num in page_obj.paginator.page_range %}
                            {% if page_obj.number == num %}
                            <li class="page-item active">
                                <span class="page-link">{{ num }}</span>
                            </li>
                            {% else %}
                            <li class="page-item">
                                <a class="page-link" 
                                   href="?page={{ num }}{% if request.GET.search %}&search={{ request.GET.search }}{% endif %}">
                                    {{ num }}
                                </a>
                            </li>
                            {% endif %}
                            {% endfor %}
                            
                            {% if page_obj.has_next %}
                            <li class="page-item">
                                <a class="page-link" 
                                   href="?page={{ page_obj.next_page_number }}{% if request.GET.search %}&search={{ request.GET.search }}{% endif %}">
                                    Next
                                </a>
                            </li>
                            {% endif %}
                        </ul>
                    </nav>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
⚙️ Django Admin Configuration

python
# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Student, Course, Enrollment, Attendance, Grade

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Student Details'

class CustomUserAdmin(UserAdmin):
    inlines = (StudentInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'phone', 'enrollment_date']
    list_filter = ['gender', 'enrollment_date']
    search_fields = ['student_id', 'first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['student_id']
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'student_id', 'first_name', 'last_name', 'date_of_birth', 'gender')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Academic Information', {
            'fields': ('enrollment_date', 'profile_picture')
        }),
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'credit_hours']
    list_filter = ['department']
    search_fields = ['code', 'name', 'description']
    prepopulated_fields = {'code': ('name',)}

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'semester', 'academic_year', 'enrollment_date']
    list_filter = ['semester', 'academic_year', 'enrollment_date']
    search_fields = ['student__student_id', 'student__first_name', 'course__code']

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'marks', 'grade', 'get_student_name', 'get_course_code']
    list_filter = ['grade']
    search_fields = ['enrollment__student__first_name', 'enrollment__course__code']
    
    def get_student_name(self, obj):
        return obj.enrollment.student.get_full_name()
    get_student_name.short_description = 'Student'
    
    def get_course_code(self, obj):
        return obj.enrollment.course.code
    get_course_code.short_description = 'Course'
🔒 Security & Authentication

Role-Based Access Control

python
# permissions.py
from django.contrib.auth.mixins import UserPassesTestMixin

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Teachers').exists() or self.request.user.is_superuser

class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'student') or self.request.user.is_superuser

# Usage in views
class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'Home/admin_dashboard.html'

class TeacherDashboardView(TeacherRequiredMixin, TemplateView):
    template_name = 'Home/teacher_dashboard.html'

class StudentDashboardView(StudentRequiredMixin, TemplateView):
    template_name = 'Home/student_dashboard.html'
Secure File Uploads

python
# utils/file_validation.py
import os
from django.core.exceptions import ValidationError
from PIL import Image

def validate_image_file(value):
    """
    Validate uploaded image files
    """
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(value.name)[1].lower()
    
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file extension. Allowed: {", ".join(valid_extensions)}')
    
    # Check file size (max 5MB)
    max_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_size:
        raise ValidationError(f'File size too large. Maximum size is {max_size/1024/1024}MB')
    
    # Validate image content
    try:
        img = Image.open(value)
        img.verify()
    except Exception as e:
        raise ValidationError(f'Invalid image file: {str(e)}')
📊 Report Generation

python
# reports/generators.py
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from django.http import HttpResponse

def generate_attendance_pdf(student_id, start_date, end_date):
    """Generate PDF attendance report for a student"""
    student = get_object_or_404(Student, id=student_id)
    attendances = Attendance.objects.filter(
        student=student,
        date__range=[start_date, end_date]
    ).select_related('course').order_by('date')
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    elements.append(Paragraph(f"Attendance Report - {student.get_full_name()}", title_style))
    elements.append(Paragraph(f"Period: {start_date} to {end_date}", styles['Normal']))
    
    # Prepare table data
    table_data = [['Date', 'Course', 'Status', 'Remarks']]
    
    for attendance in attendances:
        table_data.append([
            attendance.date.strftime('%Y-%m-%d'),
            attendance.course.code,
            attendance.get_status_display(),
            attendance.remarks or '-'
        ])
    
    # Calculate statistics
    total_classes = len(attendances)
    present_count = sum(1 for a in attendances if a.status == 'P')
    attendance_percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
    
    # Create and style table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    
    # Add summary
    elements.append(Paragraph(f"Summary:", styles['Heading2']))
    elements.append(Paragraph(f"Total Classes: {total_classes}", styles['Normal']))
    elements.append(Paragraph(f"Present: {present_count}", styles['Normal']))
    elements.append(Paragraph(f"Attendance Percentage: {attendance_percentage:.2f}%", styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer
🧪 Testing

bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test Home

# Run with coverage
coverage run manage.py test
coverage report
coverage html
Sample Test Cases

python
# tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from .models import Student, Course, Enrollment

class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            password='testpass123'
        )
        self.student = Student.objects.create(
            user=self.user,
            student_id='STU20230001',
            first_name='John',
            last_name='Doe',
            date_of_birth=date(2000, 1, 1),
            gender='M',
            phone='+1234567890',
            email='john.doe@example.com',
            address='123 Main St, City, Country'
        )
    
    def test_student_creation(self):
        self.assertEqual(self.student.student_id, 'STU20230001')
        self.assertEqual(self.student.get_full_name(), 'John Doe')
        self.assertTrue(self.student.user.check_password('testpass123'))
    
    def test_student_str_method(self):
        expected_str = 'John Doe (STU20230001)'
        self.assertEqual(str(self.student), expected_str)
    
    def test_student_age_calculation(self):
        # Assuming current date is 2023-01-01 for this test
        self.assertEqual(self.student.calculate_age(date(2023, 1, 1)), 23)

class EnrollmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent2',
            password='testpass123'
        )
        self.student = Student.objects.create(
            user=self.user,
            student_id='STU20230002',
            first_name='Jane',
            last_name='Smith',
            date_of_birth=date(2001, 2, 2),
            gender='F',
            phone='+0987654321',
            email='jane.smith@example.com',
            address='456 Oak St, City, Country'
        )
        
        self.course = Course.objects.create(
            code='CS101',
            name='Introduction to Computer Science',
            description='Basic computer science concepts',
            credit_hours=3,
            department='Computer Science'
        )
        
        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            semester='Fall',
            academic_year='2023-2024'
        )
    
    def test_enrollment_creation(self):
        self.assertEqual(self.enrollment.student, self.student)
        self.assertEqual(self.enrollment.course, self.course)
        self.assertEqual(self.enrollment.semester, 'Fall')
    
    def test_unique_enrollment_constraint(self):
        # Attempt to create duplicate enrollment should raise error
        with self.assertRaises(Exception):
            Enrollment.objects.create(
                student=self.student,
                course=self.course,
                semester='Fall',
                academic_year='2023-2024'
            )
🐳 Docker Deployment

Dockerfile

dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p staticfiles media

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run migrations and collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "SAMandSAM.wsgi:application", "--bind", "0.0.0.0:8000"]
Docker Compose

yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn SAMandSAM.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/student_management
      - SECRET_KEY=your-production-secret-key
      - DEBUG=False
    depends_on:
      - db
  
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=student_management
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
  
  nginx:
    image: nginx:1.21-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./ssl:/etc/ssl
    depends_on:
      - web

volumes:
  static_volume:
  media_volume:
  postgres_data:
📈 Production Deployment

Nginx Configuration

nginx
# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream django {
        server web:8000;
    }
    
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }
    
    server {
        listen 443 ssl;
        server_name yourdomain.com www.yourdomain.com;
        
        ssl_certificate /etc/ssl/yourdomain.crt;
        ssl_certificate_key /etc/ssl/yourdomain.key;
        
        location /static/ {
            alias /app/staticfiles/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
        
        location /media/ {
            alias /app/media/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
        
        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
        }
    }
}
Production Settings

python
# production.py
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'student_management',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Contributing

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request
Development Guidelines

Follow PEP 8 for Python code style
Write tests for new features
Update documentation as needed
Use meaningful commit messages
📞 Support

For support and questions:

Check the GitHub Issues page
Create a new issue with detailed description of your problem
Email: Check repository for contact information
🙏 Acknowledgments

Django framework and its amazing community
Bootstrap for frontend components
ReportLab for PDF generation capabilities
All contributors who have helped improve this project
