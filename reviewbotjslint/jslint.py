import os
import json

from reviewbot.tools import Tool
from reviewbot.tools.process import execute
from reviewbot.utils import is_exe_in_path


class JSLintTool(Tool):
    name = 'JSLint Code Quality Tool'
    version = '0.2'
    description = ("Checks syntax errors and validates JavaScript using the "
                   "JSLint tool.")
    options = [
        {
            'name': 'debug',
            'field_type': 'django.forms.BooleanField',
            'default': False,
            'field_options': {
                'label': 'Debug Enabled',
                'help_text': 'Allow debugger statements',
                'required': False,
            },
        },
        {
            'name': 'devel',
            'field_type': 'django.forms.BooleanField',
            'default': False,
            'field_options': {
                'label': 'Logging Enabled',
                'help_text': 'Allow logging (console, alert, etc.)',
                'required': False,
            },
        },
        {
            'name': 'es5',
            'field_type': 'django.forms.BooleanField',
            'default': False,
            'field_options': {
                'label': 'ECMAScript 5th ed.',
                'help_text': 'Allow ES5 syntax',
                'required': False,
            },
        },
        {
            'name': 'evil',
            'field_type': 'django.forms.BooleanField',
            'default': False,
            'field_options': {
                'label': 'eval() Tolerance',
                'help_text': 'Allow use of eval() statements',
                'required': False,
            },
        },
        {
            'name': 'indent',
            'field_type': 'django.forms.IntegerField',
            'default': 4,
            'field_options': {
                'label': 'Indent',
                'help_text': 'Indent size',
                'required': True,
            },
        },
        {
            'name': 'maxerr',
            'field_type': 'django.forms.IntegerField',
            'default': 1000,
            'field_options': {
                'label': 'Maximum Errors',
                'help_text': 'Maximum number of errors allowed',
                'required': True,
            },
        },
        {
            'name': 'maxlen',
            'field_type': 'django.forms.IntegerField',
            'default': 80,
            'field_options': {
                'label': 'Maximum Line Length',
                'help_text': 'Maximum source line length allowed',
                'required': True,
            },
        },
        {
            'name': 'passfail',
            'field_type': 'django.forms.BooleanField',
            'default': False,
            'field_options': {
                'label': 'Pass/Fail',
                'help_text': 'Stop scan after first error',
                'required': False,
            },
        },
        {
            'name': 'sloppy',
            'field_type': 'django.forms.BooleanField',
            'default': False,
            'field_options': {
                'label': 'Sloppy',
                'help_text': 'Allow "use strict" pragma to be optional',
                'required': False,
            },
        },
        {
            'name': 'white',
            'field_type': 'django.forms.BooleanField',
            'default': False,
            'field_options': {
                'label': 'Whitespace',
                'help_text': 'Tolerate sloppy whitespace',
                'required': False,
            },
        },
    ]

    def check_dependencies(self):
        # TODO: Add extra checking which ensures the 'js' command
        # we are hitting supports the command line arguments we use
        # when running jslint. Some of the options we use may be
        # spidermonkey specific, and we should ensure they will work
        # as expected.
        return is_exe_in_path('js')

    def handle_files(self, files):
        # Get path to js script relative to current package.
        package_root = os.path.abspath(os.path.dirname(__file__))
        lib_path = os.path.join(package_root, 'lib')
        self.runjslint_path = os.path.join(lib_path, 'runJSLint.js')
        self.jslint_path = os.path.join(lib_path, 'jslint.js')

        jslint_option_keys = [
                'debug',
                'devel',
                'es5',
                'evil',
                'passfail',
                'sloppy',
                'white',
                'indent',
                'maxerr',
                'maxlen',
            ]

        self.jslint_options = dict((s, self.settings[s])
                                   for s in jslint_option_keys)

        super(JSLintTool, self).handle_files(files)

    def handle_file(self, f):
        if not f.dest_file.lower().endswith('.js'):
            # Ignore the file.
            return False

        path = f.get_patched_file_path()
        if not path:
            return False

        output = execute(
            [
                'js',
                '-e',
                "load('%s'); runJSLint('%s', read('%s'), %s);" % (
                    self.runjslint_path,
                    self.jslint_path,
                    path,
                    json.dumps(self.jslint_options), )
            ],
            split_lines=True,
            ignore_errors=True)

        for line in output:
            try:
                parsed = line.split(':')
                lnum = int(parsed[0])
                col = int(parsed[1])
                msg = parsed[2]
                f.comment('Col: %s\n%s' % (col, msg), lnum)
            except ValueError:
                # A non-numeral was given in the output; don't use it.
                # There was likely an error in processing the .js file.
                # TODO : properly display an error message to the user saying
                #  there was an error processing the file. Also display success
                #  message if there were no errors found by this tool at all
                #  (ie no comments on the review).
                return False

        return True
