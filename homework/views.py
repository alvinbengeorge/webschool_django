from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from .models import Work, Submission
from .forms import SubmissionForm, WorkForm
# Create your views here.

class SubmissionCreateView(CreateView):
    model = Submission
    form = SubmissionForm
    fields = ['file']
    template_name = 'homework/form.html'
    success_url = '/homework/'

    def form_valid(self, form):
        submission = form.save(commit=False)
        submission.student, submission.work = self.request.user, Work.objects.get(id=self.kwargs["pk"])
        submission.save()
        return super().form_valid(form)


class WorkCreateView(CreateView):
    model = Work
    form = WorkForm
    fields = ['title', 'description',  'upload_by', 'groups', 'work_type']
    template_name = 'homework/form.html'
    success_url = '/homework/'

    def form_valid(self, form):
        work = form.save(commit=False)
        work.created_by = self.request.user
        work.save()
        for grp in form.cleaned_data['groups']:
            work.groups.add(grp)
        work.save()
        return super().form_valid(form)

class WorkListView(ListView):
    model = Work
    template_name = 'homework/list.html'
    success_url = '/homework/'

    def get_queryset(self):
        if self.request.user.user_type == self.request.user.TEACHER:
            return Work.objects.filter(created_by=self.request.user.id).order_by('-updated_at')
        else:
            return Work.objects.filter(groups__in=self.request.user.groups.all()).order_by('-updated_at').distinct()

class SubmissionListView(ListView):
    model = Submission
    template_name = 'homework/list.html'
    success_url = '/homework/'

    def get_queryset(self):
        if self.request.user.user_type == self.request.user.TEACHER:
            return Submission.objects.filter(work=self.kwargs['pk']).order_by('-updated_at')
        # else:
        #     return Submission.objects.filter(student=self.request.user.id)

class WorkUpdateView(UpdateView):
    model = Work
    fields = ['title', 'description',  'upload_by', 'groups', 'work_type']
    template_name = 'homework/form.html'
    success_url = '/homework/'

class SubmissionUpdateView(UpdateView):
    model = Submission
    fields = ['file']
    template_name = 'homework/form.html'
    success_url = '/homework/'

