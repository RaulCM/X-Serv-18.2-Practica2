from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from acorta.models import Urls

# Create your views here.


@csrf_exempt
def barra(request):
    lista = Urls.objects.all()
    if request.method == "GET":
        response = ("<form method = 'POST'>" +
                    "Introduce la URL que quieres acortar: " +
                    "<input type='text' name='url'><br>" +
                    "<input type='submit' value='Enviar'></form>")
        if len(lista) == 0:
            response += "<br>La lista de URLs está vacia"
        else:
            for url in lista:
                url_corta = "http://localhost:1234/" + str(url.id)
                response += ("<br>URL: " + url.url_larga + " --> URL corta: " +
                             "<a href=" + url_corta + ">" + url_corta + "</a>")
    elif request.method == "POST":
        url_larga = request.POST['url']
        if (url_larga[0:7] != "http://" and url_larga[0:8] != "https://"):
            url_larga = "http://" + url_larga
            try:
                url_corta = Urls.objects.get(url_larga=url_larga)
            except Urls.DoesNotExist:
                url = Urls(url_larga=url_larga)
                url.save()
                url_corta = Urls.objects.get(url_larga=url_larga)
            url_corta = "http://localhost:1234/" + str(url_corta.id)
            response = ("La url acortada de " + url_larga + " es " +
                        "<a href=" + url_corta + ">" + url_corta + "</a>")
    else:
        return HttpResponse("Method not allowed", status=405)
    return HttpResponse(response, status=200)


def redirect(request, resource):
    try:
        url_larga = Urls.objects.get(id=resource).url_larga
        return HttpResponseRedirect(url_larga)
    except Urls.DoesNotExist:
        response = "Recurso no disponible"
        return HttpResponse(response, status=404)
