from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
import PyPDF3
import mimetypes
import docx2txt
import os

from . import forms
from .models import CandidateModel


def home_view(request):
    if request.method == 'POST':
        form = forms.CreateCandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'candidates/resume_success.html', {})
    else:
        form = forms.CreateCandidateForm()
    context = {
        'form': form
    }
    return render(request, 'candidates/home.html', context)


def candidates_list_view(request):
    candidates = CandidateModel.objects.all().order_by('name')
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
        form = forms.CreateCandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('candidates:candidate-list-view')
    else:
        form = forms.CreateCandidateForm()
    context = {
        'form': form
    }
    return render(request, 'candidates/candidate_create.html', context)


def candidate_update_view(request, candId):
    if request.method == 'POST':
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


def candidate_delete_view(request, candId):
    candidate = get_object_or_404(CandidateModel, id=candId)
    context = {}
    if request.method == 'POST':
        if os.path.isfile(candidate.resume.path):
            os.remove(candidate.resume.path)
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
        filepath  = candidate.resume.path
        filename  = filepath.split('/')[-1]
        fl = open(filepath, 'rb')
        mime_type = mimetypes.guess_type(filepath)[0]
        response  = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        fl.close()
        return response


def search_view(request):
    search_word        = request.GET['q']
    search_word        = search_word.lower()
    all_candidates     = CandidateModel.objects.all()
    matched_candidates = []

    for candidate in all_candidates:
        if candidate.resume.path.endswith('.pdf'):
            pdf_file_object = open(candidate.resume.path, 'rb')
            pdf_file        = PyPDF3.PdfFileReader(pdf_file_object)
            for i in range(0, pdf_file.numPages):
                pdf_file_text = pdf_file.getPage(i).extractText()
                pdf_file_text = pdf_file_text.lower()
                if search_word in pdf_file_text:
                    if candidate not in matched_candidates:
                        matched_candidates.append(candidate)
            pdf_file_object.close()
        else:
            docx_file = docx2txt.process(candidate.resume.path)
            docx_file = docx_file.lower()

            if search_word in docx_file:
                if candidate not in matched_candidates:
                    matched_candidates.append(candidate)
    context = {
        'candidates': matched_candidates
    }
    return render(request, 'candidates/search_results.html', context)
