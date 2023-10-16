from .models import Profile
from django.shortcuts import render

import pdfkit
from django.http import HttpResponse, response
from django.template import loader
import io

# Create your views here.


def make_resume(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        summary = request.POST.get("summary", "")
        degree = request.POST.get("degree", "")
        school = request.POST.get("school_name", "")
        university = request.POST.get("university", "")
        previous_work = request.POST.get("previous_work", "")
        skills = request.POST.get("skills", "")

        profile = Profile(
            name=name,
            email=email,
            phone_no=phone,
            summary=summary,
            degree=degree,
            school_name=school,
            university=university,
            previous_work=previous_work,
            skills=skills,
        )
        profile.save()

    return render(request, "pdf/accept.html", {})


def resume(request, id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template("pdf/resume.html")
    html = template.render({"user_profile": user_profile})

    options = {
        "page-size": "Letter",
        "encoding": "UTF-8",
    }
    # config = pdfkit.configuration(wkhtmltopdf="C:\wkhtmltox\\bin\wkhtmltopdf")
    config = pdfkit.configuration(wkhtmltopdf="C:\wkhtmltox\\bin\wkhtmltopdf.exe")
    pdf = pdfkit.from_string(html, False, options, configuration=config)

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = "attachment"
    filename = "resume.pdf"
    return response


def list(request):
    profiles = Profile.objects.all()
    return render(request, "pdf/list.html", {"profiles": profiles})
