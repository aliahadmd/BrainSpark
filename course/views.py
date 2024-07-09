# course/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from .models import Course, Lesson, Enrollment, Payment
import stripe
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from allauth.account.adapter import DefaultAccountAdapter
from allauth_2fa.adapter import OTPAdapter
from allauth_2fa.utils import user_has_valid_totp_device


stripe.api_key = settings.STRIPE_SECRET_KEY

def course_list(request):
    courses = Course.objects.all()
    query = request.GET.get('q')
    if query:
        courses = courses.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(instructor__username__icontains=query)
        )
    return render(request, 'course/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    lessons = course.lessons.all().order_by('order')
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'lessons': lessons
    }
    return render(request, 'course/course_detail.html', context)

@login_required
def enroll_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except ObjectDoesNotExist:
        messages.error(request, "The requested course does not exist.")
        return redirect('course_list')

    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, "You are already enrolled in this course.")
        return redirect('course_detail', course_id=course.id)

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
            success_url=request.build_absolute_uri(reverse('enroll_success', args=[course.id])),
            cancel_url=request.build_absolute_uri(reverse('course_detail', args=[course.id])),
        )
        return redirect(session.url)
    
    return render(request, 'course/enroll_course.html', {'course': course})

@login_required
def enroll_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)
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
        return HttpResponseForbidden("You are not enrolled in this course.")
    
    lessons = course.lessons.order_by('order')
    current_lesson_index = list(lessons).index(lesson)
    previous_lesson = lessons[current_lesson_index - 1] if current_lesson_index > 0 else None
    next_lesson = lessons[current_lesson_index + 1] if current_lesson_index < len(lessons) - 1 else None
    
    context = {
        'course': course,
        'lesson': lesson,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
    }
    return render(request, 'course/course_video_player.html', context)



@login_required
@require_GET
def get_lesson_video_url(request):
    lesson_id = request.GET.get('lesson_id')
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if not Enrollment.objects.filter(user=request.user, course=lesson.course).exists():
        return JsonResponse({'error': 'You are not enrolled in this course.'}, status=403)
    
    return JsonResponse({'video_url': lesson.video.url})



class Custom2FAAdapter(OTPAdapter, DefaultAccountAdapter):
    def pre_login(self, request, user, **kwargs):
        if user_has_valid_totp_device(user):
            request.session['allauth_2fa_user_id'] = user.id
            return HttpResponseRedirect(reverse('two-factor-authenticate'))
        return super().pre_login(request, user, **kwargs)

    def login(self, request, user):
        if user_has_valid_totp_device(user):
            request.session['allauth_2fa_user_id'] = user.id
            return HttpResponseRedirect(reverse('two-factor-authenticate'))
        return super().login(request, user)