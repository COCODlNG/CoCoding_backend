from django.http import JsonResponse
from django.utils import timezone

from apps.codes.models import Code
from misc import random_str
from tasks.run_code import execute_code

language_map = {
    'python': Code.PYTHON,
    'java': Code.JAVA,
    'c': Code.C
}


def run_code(request, *args, **kwargs):
    code = request.POST.get('code')
    std_in = request.POST.get('std_in')
    language = language_map[request.POST.get('language')]

    code_dict = {}
    if language == 'python':
        code_dict['main.py'] = code
    elif language == 'java':
        code_dict['Main.java'] = code
    elif language == 'c':
        code_dict['main.c'] = code
    try:
        end_msg, std_out, err_out = execute_code(code_dict, std_in, language, random_str())
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
        'std_out': std_out.replace('/home/ubuntu/CoCoding_backend/CoCoding/tasks/task_code/', ''),
        'err_out': err_out.replace('/home/ubuntu/CoCoding_backend/CoCoding/tasks/task_code/', ''),
    })
