# course/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Course, Lesson, Enrollment, Payment
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course/course_detail.html', {'course': course})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        # Create a Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(course.price * 100),  # Stripe uses cents
                    'product_data': {
                        'name': course.title,
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/courses/{course.id}/enroll/success/'),
            cancel_url=request.build_absolute_uri(f'/courses/{course.id}/'),
        )
        return redirect(session.url)
    return render(request, 'course/enroll_course.html', {'course': course})

@login_required
def enroll_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # Create Enrollment and Payment objects
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            stripe_charge_id='placeholder'  # You should update this with the actual Stripe charge ID
        )
        messages.success(request, f'You have successfully enrolled in {course.title}!')
    else:
        messages.info(request, f'You were already enrolled in {course.title}.')
    return redirect('my_courses')

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'course/my_courses.html', {'enrollments': enrollments})

@login_required
def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('course_detail', course_id=course.id)
    return render(request, 'course/lesson_detail.html', {'lesson': lesson})