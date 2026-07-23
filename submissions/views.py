from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from .models import Submission
from django.utils import timezone
from django.contrib import messages
from users.models import ProjectManager
from django.contrib.auth.decorators import login_required

# submission
class PageOnlySubmissionForm(forms.Form):
    title = forms.CharField(max_length=200)
    category = forms.ChoiceField(
        choices=[
            # change them to match the SDG11 concepts
            ("general", "General"),
            ("safety", "Safety"),
            ("infrastructure", "Infrastructure"),
            ("event", "Event"),
        ]
    )
    location = forms.CharField(max_length=255, required=True)
    description = forms.CharField(widget=forms.Textarea)
    photo = forms.ImageField(required=False)

def submission_list(request):
    submissions = Submission.objects.all().order_by("-pub_date")
    return render(request, "list.html", {"submissions": submissions})

def create_submission(request):
    if request.method == "POST":
        form = PageOnlySubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            Submission.objects.create(
                submission_title = form.cleaned_data["title"],
                submission_category = form.cleaned_data["category"],
                submission_location = form.cleaned_data["location"],
                submission_description = form.cleaned_data["description"],
                pub_date = timezone.now(),
            )
            return render(request, "submit.html", {
                "form": form,
                "submissionSuccessMsg": True
                }
            )
    else:
        form = PageOnlySubmissionForm()

    return render(request, "submit.html", {"form": form})

@login_required
def delete_submission(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    if ProjectManager.objects.filter(pk=request.user.pk).exists() or request.user.is_superuser:
        submission.delete()
        #messages.success(request, "Submission deleted successfully.")
    return redirect('submissions:submission_list')
