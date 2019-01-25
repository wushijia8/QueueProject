# _*_ encoding:utf-8 _*_

from django.http import HttpResponse
from rest_framework.views import APIView

from .tasks import add


class Receiver(APIView):
    def post(self, request):
        num1 = request.data[u"num1"]
        num2 = request.data[u"num2"]
        print add.delay(num1, num2)
        return HttpResponse('{"status":"success"}', content_type='application/json')
