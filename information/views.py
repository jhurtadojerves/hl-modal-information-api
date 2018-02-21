from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from bs4 import BeautifulSoup
import requests
import re


class InformationView(View):
    def get(self, request, *arg, **kwargs):
        response = requests.get('http://www.harrylatino.org/user/'+self.kwargs['url']+'/')
        status_code = response.status_code
        if status_code == 200:
            html = BeautifulSoup(response.text)
            li = html.select('#custom_fields_personaje > .ipsList_data > li')
            output = list()
            for span in li:
                try:
                    title = span.select('.row_title').pop().string
                    data = span.select('.row_data').pop().string
                    if data is None:
                        data = span.select('.row_data > a').pop().string
                    output.append((title.strip(), data.strip()))
                except:
                    pass

            return JsonResponse(output, safe=False)

        return JsonResponse("Ocurrió un error extraño (?)")
