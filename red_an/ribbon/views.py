from django.shortcuts import render


def ribbonView(request):

    return render(request, 'ribbon/base.html')
