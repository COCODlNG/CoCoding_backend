import subprocess
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