
from django.shortcuts import render
from django.http import Http404


# Sample course information
COURSES_DATA = [
    {
        'id': 101,
        'code': 'DTI412',
        'title': 'Special Topic in Application Development',
        'credits': 3,
        'instructor': 'Dr. Sirisuda Buathongkeow',
        'description': (
            'Comprehensive backend application engineering '
            'focusing on Django, DRF, RESTful APIs, JWT security, '
            'and cloud deployment.'
        )
    },
    {
        'id': 102,
        'code': 'DTI201',
        'title': 'Database Systems & Data Modeling',
        'credits': 3,
        'instructor': 'Department Faculty',
        'description': (
            'Relational database design, ER diagrams, SQL query '
            'optimization, normalization, and transaction management.'
        )
    },
    {
        'id': 103,
        'code': 'DTI305',
        'title': 'Frontend Web Technologies & React',
        'credits': 3,
        'instructor': 'Department Faculty',
        'description': (
            'Modern user interface development using JavaScript ES6+, '
            'React components, state management, and API integration.'
        )
    }
]


# Homepage
def home_view(request):
    context = {
        'total_courses': len(COURSES_DATA),
        'featured_course': COURSES_DATA[0],
    }

    return render(request, 'catalog/home.html', context)


# Course list

def course_list_view(request):

    # Get the search word from the URL
    search_query = request.GET.get('q', '').strip()

    # Start with all courses
    courses = COURSES_DATA

    # Filter courses when a search word is entered
    if search_query:
        courses = [
            course for course in COURSES_DATA
            if search_query.lower() in course['title'].lower()
            or search_query.lower() in course['code'].lower()
        ]

    context = {
        'courses': courses,
        'search_query': search_query,
    }

    return render(request, 'catalog/course_list.html', context)


# Course details
def course_detail_view(request, course_id):
    course = next(
        (c for c in COURSES_DATA if c['id'] == course_id),
        None
    )

    if not course:
        raise Http404("Course with specified ID was not found.")

    context = {
        'course': course,
    }

    return render(request, 'catalog/course_detail.html', context)


# Student inquiry form
def inquiry_view(request):
    submitted_data = None
    errors = []

    if request.method == 'POST':

        student_name = request.POST.get(
            'student_name', ''
        ).strip()

        email = request.POST.get(
            'email', ''
        ).strip()

        course_code = request.POST.get(
            'course_code', ''
        ).strip()

        message = request.POST.get(
            'message', ''
        ).strip()

        # Check student name
        if not student_name:
            errors.append("Student Name is required.")

        # Check email
        if not email or '@' not in email:
            errors.append("A valid Email address is required.")

        # Check message
        if not message:
            errors.append("Inquiry message cannot be empty.")

        # Process successful submission
        if not errors:
            submitted_data = {
                'student_name': student_name,
                'email': email,
                'course_code': course_code,
                'message': message,
            }

    context = {
        'courses': COURSES_DATA,
        'submitted_data': submitted_data,
        'errors': errors,
    }

    return render(request, 'catalog/inquiry.html', context)
