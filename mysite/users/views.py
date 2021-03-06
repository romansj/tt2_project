# Create your views here.
import json
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.views import generic
from django.views.decorators.cache import never_cache

from recipes.models import Post
from .forms import SignUpForm
from .models import Question, Choice, User_report, Profile
from .tokens import account_activation_token


def activation_sent_view(request):
    return render(request, 'users/activation_sent.html')


def report_profile(request, pk):
    response_data = {}
    model = User_report
    if request.method == 'POST':
        report_text = request.POST.get('the_report')
        response_data['author'] = request.user.username
        response_data['text'] = report_text
        response_data['postpk'] = pk
        # print(request.user.username)
        # šī daļa ir tur kur strādā liekot datu
        reporting = User_report(reported_user=request.user, reported_text=report_text)
        reporting.save()
        text = request.user.username + report_text + str(pk)
        send_mail('Report', text, settings.EMAIL_HOST_USER, ['amachefDF@gmail.com'], fail_silently=False)
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('users:index')
    else:
        return render(request, 'users/activation_invalid.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            # user.profile.picture=form.cleaned_data.get('profile_picture')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account'
            # load a template like get_template()
            # and calls its render() method immediately.
            message = render_to_string('users/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            # return HttpResponse('Please confirm your email address to complete the registration')
            # todo what does this do, Elvis?
            # user.email_user(subject, message)
            return redirect('users:activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


class IndexView(generic.ListView):
    template_name = 'users/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        # Question.objects.filter(pub_date__lte=timezone.now()) returns a queryset containing Questions whose pub_date is less than or equal to - that is, earlier than or equal to - timezone.now.
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class ProfileDetailView(generic.DetailView):
    model = Profile


def report_issue(request):
    response_data = {}
    if request.method == 'POST':
        report_text = request.POST.get('the_message')
        response_data['text'] = report_text
        send_mail('Report', report_text, settings.EMAIL_HOST_USER, ['amachefDF@gmail.com'], fail_silently=False)
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return render(request, 'users/report-issue.html')


class ProfileView(generic.ListView):
    @never_cache
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    template_name = 'users/profile_list.html'
    model = Post
    context_object_name = 'posts'

    # def get_context_data(self, **kwargs):
    #     context = super(ProfileView, self).get_context_data(**kwargs)
    #     context['author'] = User.objects.get(self.kwargs['pk'])
    #     return context
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        # print(self.kwargs['pk'])
        return Post.objects.filter(author_id=self.kwargs['pk'])


class DetailView(generic.DetailView):
    model = Question
    template_name = 'users/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'users/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'users/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('users:results', args=(question.id,)))


@user_passes_test(lambda user: user.is_authenticated and (user.profile.is_moderator or user.is_superuser), login_url='/users/login/')

def user_promotion(request, pkkk):
    new_mod = get_object_or_404(Profile, id=pkkk)
    new_mod.is_moderator = True
    new_mod.save()
    return redirect('users:profile-view', pk=pkkk)


@user_passes_test(lambda user: user.is_authenticated and (user.profile.is_moderator or user.is_superuser), login_url='/users/login/')
def user_demotion(request, pkkk):
    new_mod = get_object_or_404(Profile, id=pkkk)
    new_mod.is_moderator = False
    new_mod.save()
    return redirect('users:profile-view', pk=pkkk)
