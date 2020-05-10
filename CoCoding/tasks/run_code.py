import subprocess
import conf.settings
from celery import Celery
from apps.codes.models import Code

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


def execute_code(code, language_type, pk):
    C, JAVA, PYTHON = 0, 1, 2
    code_dir = conf.settings.BASE_DIR + '/tasks/task_code/'
    if language_type == PYTHON:
        file_name = pk + '.py'
        full_path = code_dir + file_name
        f = open(full_path, 'w')
        f.write(code)
        f.close()
        proc = subprocess.Popen(['python', full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        return out.decode('utf-8'), err.decode('utf-8')
    elif language_type == JAVA:
        file_name = pk + '.java'
        full_path = code_dir + file_name
        f = open(full_path, 'w')
        f.write(code)
        f.close()
        proc = subprocess.Popen(['javac', '-d', code_dir, '-sourcepath', code_dir ,full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #TODO stop code and return compile error message right after compile is finished
        out, err = proc.communicate()
        #out.decode('utf-8')
        #err.decode('utf-8')
        proc = subprocess.Popen(['java', '-classpath', code_dir, pk], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        return out.decode('utf-8'), err.decode('utf-8')
    elif language_type == C:
        file_name = pk + '.c'
        full_path = code_dir + file_name
        execute_file_name = code_dir + pk
        print(execute_file_name)
        f = open(full_path, 'w')
        f.write(code)
        f.close()
        proc = subprocess.Popen(['gcc', full_path, '-o', execute_file_name], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        # TODO stop code and return compile error message right after compile is finished
        out, err = proc.communicate()
        #out.decode('utf-8')
        #err.decode('utf-8')
        proc = subprocess.Popen([execute_file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        return out.decode('utf-8'), err.decode('utf-8')
    else:
        return None, None

if __name__ == '__main__':
    pass