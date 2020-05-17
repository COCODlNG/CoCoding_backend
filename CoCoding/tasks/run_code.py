from celery import Celery
from apps.codes.models import Code
import subprocess
from subprocess import Popen, PIPE
import conf.settings
import os
import shutil

app = Celery('run_code')


@app.task
def run_code(code_id):
    code = Code.objects.filter(id=code_id).fisrt()
    code.status = Code.ONGOING
    code.save(update_fields=['status'])
    try:
        code.code = CodeExecutor(code).run_code()
        code.status = Code.COMPLETED
        code.save(update_fields=['status', 'code'])

    except Exception:
        code.status = Code.FAILED
        code.save(update_fields=['status'])


class CodeExecutor:
    code = None
    file_name = None

    def __init__(self, code_id):
        self.code = Code.objects.filter(id=code_id).fisrt()

    def get_file_extension(self):
        extensions = {
            Code.PYTHON: '.py',
            Code.JAVA: '.java',
            Code.C: '.c',
        }
        return extensions.get(self.code.language)

    def save_code(self):
        self.file_name = '{}'.format(self.code.id)
        f = open(self.file_name + self.get_file_extension(), 'w')
        f.write(self.code.code)
        f.close()

    def compile(self):
        compilers = {
            Code.PYTHON: 'echo',
            Code.JAVA: 'javac',
            Code.C: 'gcc',
        }
        return subprocess.call(compilers.get(self.code.language))

    def run_code(self):
        runners = {
            Code.PYTHON: 'python',
            Code.JAVA: 'java',
            Code.C: 'source',
        }
        output_file = {
            Code.PYTHON: self.file_name + self.get_file_extension(),
            Code.JAVA: self.file_name + '.class',
            Code.C: 'a.out',
        }
        return subprocess.check_output(
            [
                runners.get(self.code.language),
                output_file.get(self.code.language)
            ]
        )


def construct_code_tree(code_dict, language_type, code_dir):
    cmp_dict = {}
    for key in code_dict.keys():
        if type(code_dict[key]) == type(cmp_dict):
            new_dir = code_dir + key
            os.mkdir(new_dir)
            new_dir = new_dir + '/'
            construct_code_tree(code_dict[key], language_type, new_dir)
        else:
            file_name = key
            full_path = code_dir + file_name
            f = open(full_path, 'w')
            f.write(code_dict[key])
            f.close()


def execute_code(code_dict, input, language_type, pk):
    C, JAVA, PYTHON = 'c', 'java', 'python'
    EXECUTE_COMPLETE, COMPILE_ERROR, RUNTIME_ERROR = 0, 1, 2
    end_msg = -1
    output = ''
    error = ''
    code_dir_name = conf.settings.BASE_DIR + '/tasks/task_code/' + pk
    os.mkdir(code_dir_name)
    code_dir = code_dir_name + '/'
    construct_code_tree(code_dict, language_type, code_dir)
    if language_type == PYTHON:
        file_name = 'main.py'
        full_path = code_dir + file_name
        proc = Popen(['python', full_path], stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate(input= input.encode())
        if err:
            end_msg = RUNTIME_ERROR
        else:
            end_msg = EXECUTE_COMPLETE
        output = out.decode('utf-8')
        error = err.decode('utf-8')
    elif language_type == JAVA:
        file_name = 'Main.java'
        full_path = code_dir + file_name
        proc = Popen(['javac', '-d', code_dir, '-sourcepath', code_dir ,full_path], stdout=PIPE,
                     stdin=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        if err:
            end_msg = COMPILE_ERROR
            output = out.decode('utf-8')
            error = err.decode('utf-8')
        else:
            full_path = code_dir + ':' + 'Main'
            proc = Popen(['java', '-classpath', code_dir, 'Main'], stdout=PIPE,
                         stdin=PIPE, stderr=PIPE)
            out, err = proc.communicate(input= input.encode())
            if err:
                end_msg = RUNTIME_ERROR
            else:
                end_msg = EXECUTE_COMPLETE
            output = out.decode('utf-8')
            error = err.decode('utf-8')
    elif language_type == C:
        file_name = 'main.c'
        full_path = code_dir + file_name
        execute_file_name = code_dir + pk
        print(execute_file_name)
        proc = Popen(['gcc', full_path, '-o', execute_file_name], stdout=PIPE,
                                stdin=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        if err:
            end_msg = COMPILE_ERROR
            output = out.decode('utf-8')
            error = err.decode('utf-8')
        else:
            proc = Popen([execute_file_name], stdout=PIPE,
                         stdin=PIPE, stderr=PIPE)
            out, err = proc.communicate(input = input.encode())
            if err:
                end_msg = RUNTIME_ERROR
            else:
                end_msg = EXECUTE_COMPLETE
            output = out.decode('utf-8')
            error = err.decode('utf-8')

    shutil.rmtree(code_dir_name)
    return end_msg, output, error


if __name__ == '__main__':
    pass