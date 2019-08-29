import os

from jinja2 import Environment, FileSystemLoader


class J2Env(object):
    _environment = None
    _base_folder = 'templates'

    def __init__(self):
        # Setup the environment
        self._environment = Environment(
            autoescape=False,
            loader=FileSystemLoader(self._get_template_folder()),
            trim_blocks=False)

    def _get_template_folder(self):
        return os.path.join(os.environ.get('GIT_REPO'), self._base_folder)

    def render_template(self, template_filename, context):
        return self._environment.get_template(template_filename).render(context)

    def create_file(self, j2_file, input_dict, out_file):
        with open(out_file, 'w') as f:
            out = self.render_template(j2_file, input_dict)
            f.write(out)
