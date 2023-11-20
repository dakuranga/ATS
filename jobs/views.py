from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse  # Add this import statement
from .models import Job, Client
from .forms import JobForm, JobFilterForm
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test

def jobs(request):
    jobs = Job.objects.all().order_by('-date_added')
    form = JobFilterForm(request.GET)

    if form.is_valid():
        status_filter = form.cleaned_data['job_status']
        priority_filter = form.cleaned_data['job_priority']
        client_filter = form.cleaned_data['client']

        if status_filter:
            jobs = jobs.filter(job_status=status_filter)
        if priority_filter:
            jobs = jobs.filter(job_priority=priority_filter)
        if client_filter:
            jobs = jobs.filter(client=client_filter)
    else:
        form = JobFilterForm()
        jobs = Job.objects.all()
    
    
    # Paginate the jobs
    paginator = Paginator(jobs, 8)  # Show 10 jobs per page (you can change this number)
    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)

    context = {
        'jobs': jobs_page,  # Use the paginated jobs queryset
        'filter_form': form,
    }
    return render(request, 'jobs.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_edit_job(request, job_id=None):
    if job_id is not None:
        job = get_object_or_404(Job, pk=job_id)
        form = JobForm(request.POST or None, request.FILES or None, instance=job)
        mode = 'edit'
    else:
        form = JobForm(request.POST or None, request.FILES or None)
        mode = 'add'

    if request.method == 'POST':
        if form.is_valid():
            job_instance = form.save(commit=False)
            job_instance.save()
            return redirect('jobs')

    template = 'add_edit_job.html'
    context = {'form': form, 'mode': mode}
    return render(request, template, context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_job(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        job.delete()
        return redirect('jobs')
    else:
        return redirect('jobs')
    
def view_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'view_job.html', {'job': job})