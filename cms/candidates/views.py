from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
import mimetypes

from . import forms
from .models import CandidateModel
# Create your views here.


def candidates_list_view(request):
    candidates = CandidateModel.objects.all().order_by('-date')
    context = {
        'candidates': candidates
    }
    return render(request, 'candidates/candidate_list.html', context)


def candidate_detail_view(request, candId):
    candidate = get_object_or_404(CandidateModel, id=candId)
    context = {
        'candidate': candidate
    }
    return render(request, 'candidates/candidate_detail.html', context)


def candidate_create_view(request):
    if request.method == 'POST':
        #form = forms.CreateCandidateForm(request.POST)
        form = forms.CreateCandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('candidates:candidate-list-view')
    else:
        form = forms.CreateCandidateForm()
    context = {
        'form':form
    }
    return render(request, 'candidates/candidate_create.html', context)

# def candidate_update_view(request, candId):
#     if request.method == 'POST':
#         # Check if POST request is from Update Candidate Button on candidate_detail page
#         if 'from update candidate btn' in request.POST:
#             candidate = get_object_or_404(CandidateModel, id=candId)
#             form      = forms.CreateCandidateForm(request.GET or None, request.FILES, instance=candidate)
#         else:
#             # If POST request is from the form to itself to save updated data
#             candidate = get_object_or_404(CandidateModel, id=candId)
#             form      = forms.CreateCandidateForm(request.POST or None, request.FILES, instance=candidate)
#             if form.is_valid():
#                 form.save()
#                 return redirect('candidates:candidate-detail-view', candId=candId)
#     else:
#         candidate = get_object_or_404(CandidateModel, id=candId)
#         form = forms.CreateCandidateForm(request.GET or None, instance=candidate)
#     context = {
#         'form': form,
#     }
#     return render(request, 'candidates/candidate_update.html', context)


def candidate_update_view(request, candId):
    if request.method == 'POST':
        # Check if POST request is from Update Candidate Button on candidate_detail page
        # If POST request is from the form to itself to save updated data
        candidate = get_object_or_404(CandidateModel, id=candId)
        form      = forms.CreateCandidateForm(request.POST or None, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            return redirect('candidates:candidate-detail-view', candId=candId)
    else:
        candidate = get_object_or_404(CandidateModel, id=candId)
        form = forms.CreateCandidateForm(request.GET or None, instance=candidate)
    context = {
        'form': form,
    }
    return render(request, 'candidates/candidate_update.html', context)

    # if request.method == 'POST':
    #     # Check if POST request is from update candidate button
    #     if 'from update candidate btn' in request.POST:
    #
    #     candidate = get_object_or_404(CandidateModel, id=candId)
    #     form      = forms.CreateCandidateForm(request.POST or None, instance=candidate)
    #     if form.is_valid():
    #         # instance      = form.save(commit=False)
    #         # instance.slug = instance.author.username + '-' + form.cleaned_data['slug']
    #         # instance.save()
    #         form.save()
    #         return redirect('candidates:candidate-detail-view', candId=candId)
    # else:
    #     candidate = get_object_or_404(CandidateModel, id=candId)
    #     form      = forms.CreateCandidateForm(request.GET or None, instance=candidate)
    # context = {
    #     'form': form,
    # }
    # return render(request, 'candidates/candidate_update.html', context)


def candidate_delete_view(request, candId):
    candidate = get_object_or_404(CandidateModel, id=candId)
    context = {}
    if request.method == 'POST':
        if 'confirm delete' in request.POST:
            # if condition checks if POST request is coming from candidate_delete.html
            # by clicking the Confirm Delete button
            candidate.delete()
            return redirect('candidates:candidate-list-view')
    else:
        context = {
            'candidate': candidate
        }

    return render(request, 'candidates/candidate_delete.html', context)


def resume_download_view(request, candId):
    if request.method == 'GET':
        candidate = CandidateModel.objects.get(id=candId)
        #print('filepath -->', filepath)
        print('request', request)
        filepath = candidate.resume.path
        filename = filepath.split('/')[-1]
        print('fl_path -->', filepath)
        print('filename -->', filename)
        fl = open(filepath, 'rb')
        mime_type = mimetypes.guess_type(filepath)[0]
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        fl.close()
        return response
    else:
        HttpResponse("POST REQUEST")
