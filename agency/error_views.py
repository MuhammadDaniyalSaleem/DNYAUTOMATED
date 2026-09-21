from django.shortcuts import render
def error_404(r,e): return render(r,'agency/error.html',{'code':'404','message':'This page could not be found.'},status=404)
def error_500(r): return render(r,'agency/error.html',{'code':'500','message':'Something went wrong on our side.'},status=500)
