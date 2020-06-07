from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
import PyPDF3
import mimetypes
import docx2txt
import os

from . import forms
from .models import CandidateModel


def home_view(request):
    """
        - This view is called when a user visits the landing page.
        - It handles both GET Requests when the user visits this page to add details to it to
          apply for a job as well as POST requests when a user submits his / her information.

        :param request: standard request object that contains details about the request received.
        :return: redirected to resume_success.html on successful upload of information.
    """
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
    """
        This view GETs a list of all candidates, orders them by the name of the candidates
        and displays them for viewing.

        :param request: standard request object that contains details about the request received.
        :return: list of candidates displayed on the candidate_list.html page.
    """
    candidates = CandidateModel.objects.all().order_by('name')
    context = {
        'candidates': candidates
    }
    return render(request, 'candidates/candidate_list.html', context)


def candidate_detail_view(request, candId):
    """
        This view GETs a candidate based on the id present in the URL.

        :param request: standard request object that contains details about the request received.
        :param candId: candidate id in the URL.
        :return: candidate object displayed on the candidate_detail.html page.
    """
    candidate = get_object_or_404(CandidateModel, id=candId)
    context = {
        'candidate': candidate
    }
    return render(request, 'candidates/candidate_detail.html', context)


def candidate_create_view(request):
    """
        - This view handles both GET and POST requests to create a new candidate.
        - GET request is handled when a user requests the candidate_create.html page to create
          a new candidate.
        - POST request is handled when a user submits the information added to the form on
          the candidate_create.html page to create a new candidate.

        :param request: standard request object that contains details about the request received.
        :return: redirected to the candidate_list.html page on successful candidate creation.
    """
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
    """
        - This view handles both GET and POST requests to update a candidate.
        - GET request is handled when a user requests the candidate_update.html page to update
          a candidate. The page is returned with the candidate's current information.
        - POST request is handled when a user submits the information added to the form on
          the candidate_update.html page to update a candidate.

        :param request: standard request object that contains details about the request received.
        :param candId: candidate id in the URL.
        :return: redirected to the candidate_detail.html page on successful update.
    """
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
    """
        - This view handles both GET and POST requests to delete a candidate.
        - GET request is handled when a user clicks the delete button on the
          candidate_detail.html and is redirected to the candidate_delete.html page
          to seek confirmation of the deletion.
        - POST request is handled when a user confirms deletion on the the candidate_delete.html
          page to delete a candidate.
        - The view also performs clean-up of the deleted candidate's resume just before deletion.

        :param request: standard request object that contains details about the request received.
        :param candId: candidate id in the URL.
        :return: redirected first to candidate_delete.html and then to candidate_list.html
                 on successful deletion.
    """
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
    """
        - This view allows users to download a candidate's resume.
        - The view checks if the resume exists, reads it, checks its mime type and alters
          the response headers to inform the browser that the file is an attachment and thus
          should be allowed to download.

        :param request: standard request object that contains details about the request received.
        :param candId: candidate id in the URL.
        :return: HTTP Response prompting download option on the UI.
    """
    if request.method == 'GET':
        candidate = CandidateModel.objects.get(id=candId)
        filepath  = candidate.resume.path
        if filepath:
            filename  = filepath.split('/')[-1]
            resume    = open(filepath, 'rb')
            mime_type = mimetypes.guess_type(filepath)[0]
            response  = HttpResponse(resume, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            resume.close()
            return response


def search_view(request):
    """
        - This view handles the search bar's functionality.
        - The view retrieves all candidates and checks for the search word entered in the
          search bar in the all resumes, be it in docx or pdf format.

        :param request: standard request object that contains details about the request received.
        :return: redirection to the search_results.html page and displays list of candidates
                 whose resumes contained the search word.
    """
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
