from django.http import JsonResponse
from django.utils import timezone

from apps.codes.models import Code
from tasks.run_code import execute_code

language_map = {
    'Python': Code.PYTHON,
    'Java': Code.JAVA,
    'C': Code.C
}


def run_code(request, *args, **kwargs):
    code = request.POST.get('code')
    std_in = request.POST.get('std_in')
    language = language_map[request.POST.get('language')]
    try:
        std_out, err_out = execute_code(code, language, str(10))
    except Exception as e:
        return JsonResponse({
            'is_error': True,
            'std_out': "",
            'err_out': "컴파일 에러!!",
        })
    is_error = False
    if err_out:
        is_error = True
    return JsonResponse({
        'is_error': is_error,
        'std_out': std_out,
        'err_out': err_out,
    })
