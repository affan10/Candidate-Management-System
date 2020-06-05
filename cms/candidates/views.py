from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
import PyPDF3
import mimetypes

from . import forms
from .models import CandidateModel
# Create your views here.


def home_view(request):
    if request.method == 'POST':
        form = forms.CreateCandidateForm(request.POST, request.FILES)
        if form.is_valid():
            print("HERE IN VALID Home_View....")
            form.save()
            return render(request, 'candidates/resume_success.html', {})
    else:
        print("HERE IN ELSE....")
        form = forms.CreateCandidateForm()
    context = {
        'form': form
    }
    return render(request, 'candidates/home.html', context)


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


def search_view(request):
    search_word        = request.GET['q']
    search_word        = search_word.lower()
    all_candidates     = CandidateModel.objects.all()
    matched_candidates = []
    print(search_word)
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
                        print('TYPE --> ', type(pdf_file.getPage(i).extractText()))
            # with open(candidate.resume.path, 'r') as file:
            #     resume_content = file.readlines()
            # print(resume_content)
            # if search_word in resume_content:
            #     matched_candidates.append(candidate)

    context = {
        'candidates': matched_candidates
    }
    return render(request, 'candidates/search_results.html', context)

#
# class SearchView(ListView):
#     model         = CandidateModel
#     template_name = 'candidates/search_results.html'
#
#     def get_queryset(self):
#         articles = []
#         query    = self.request.GET['q']
#         query    = query.split(' ')
#         for word in query:
#             filtered_articles = CandidateModel.objects.filter(
#                 Q(title__icontains=word) | Q(body__icontains=word) |
#                 Q(author__username__icontains=word) | Q(thumb__icontains=word)
#             ).order_by('-date')
#
#             # For removing duplicate articles fetched by the above filters
#             for article in filtered_articles:
#                 if article not in articles:
#                     articles.append(article)
#
#         return articles