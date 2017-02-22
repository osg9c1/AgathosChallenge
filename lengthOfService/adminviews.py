import os
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from forms import UploadSeedFileForm, GenerateSeedFileForm
from models import ShopWorkFlowFact


class UploadCSVView(TemplateView):
    """
    View for uploading a csv file and the output is a table of the format:

    Name  repairtype  average time ratio of average

     Bob    A            1            1

     Rich   D            4            0.5

    """
    template_name = 'SeedForm.html'

    def get_context_data(self, **kwargs):
        context = super(UploadCSVView, self).get_context_data(**kwargs)
        context["form"] = UploadSeedFileForm(self.request.POST or None)
        return context

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(**kwargs)
        return super(UploadCSVView, self).render_to_response(context_data)

    def post(self, request, *args, **kwargs):
        from helper import handle_uploaded_file, compute_los
        context_data = self.get_context_data(**kwargs)
        seed_form = UploadSeedFileForm(request.POST, request.FILES)
        if seed_form.is_valid():
            ShopWorkFlowFact().delete_everything()
            err_msg = handle_uploaded_file(request.FILES['file'])
            if err_msg:
                messages.error(request, err_msg)
        output_data = compute_los()
        context_data["output_list"] = output_data
        return super(UploadCSVView, self).render_to_response(context_data)


class DownloadSeedFileView(TemplateView):
    """
    Download a seed file with records generated with random data.
    """

    template_name = 'DownloadSeedForm.html'

    def get_context_data(self, **kwargs):
        context = super(DownloadSeedFileView, self).get_context_data(**kwargs)
        context["form"] = GenerateSeedFileForm(self.request.POST or None)
        return context

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(**kwargs)
        return super(DownloadSeedFileView, self).render_to_response(context_data)

    def post(self, request, *args, **kwargs):
        from helper import generate_csv_file

        context_data = self.get_context_data(**kwargs)
        generate_seed_form = GenerateSeedFileForm(request.POST)
        if generate_seed_form.is_valid():
            start_date = generate_seed_form.cleaned_data.get("start_date")
            end_date = generate_seed_form.cleaned_data.get("end_date")
            no_of_records = int(generate_seed_form.cleaned_data.get("no_of_records"))
            generate_csv_file(start_date, end_date, no_of_records)
            file_out = ""
            with open("seed.csv", 'r') as fin:
                file_out = fin.read()
            response = HttpResponse(file_out, content_type='application/csv')
            response['Content-Disposition'] = 'attachment; filename="seed.csv"'
            return response
        return super(DownloadSeedFileView, self).render_to_response(context_data)
