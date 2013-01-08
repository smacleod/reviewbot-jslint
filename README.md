reviewbot-jslint
================

reviewbot-jslint is a plugin to the [Review Bot](https://github.com/smacleod/ReviewBot) static analysis automation tool. It allows the JSLint code quality tool to be run on .js files uploaded in [Review Board](http://www.reviewboard.org/) review requests.

[JSLint](http://www.jslint.com/) is a tool written in JavaScript developed by [Doug Crockford](https://github.com/douglascrockford/JSLint) for inspecting JavaScript code.

Installation
============

reviewbot-jslint requires installation of Review Bot (see [instructions](https://github.com/smacleod/ReviewBot)), and of the [Spidermonkey](https://developer.mozilla.org/en-US/docs/SpiderMonkey/1.8.5) JavaScript engine.

Spidermonkey
------------

* **Installation:** For instructions on building and installing Spidermonkey, please consult the Mozilla Developer Network [documentation](https://developer.mozilla.org/en-US/docs/SpiderMonkey/Build_Documentation).

* **Running JSLint on Spidermonkey:** In order for reviewbot-jslint to be able to run jslint.js on your system, the path to the js executable (e.g. js-1.8.5/js/src) must be added to the system path.

Installing and Registering Tasks
--------------------------------

Review Bot workers are able to find installed tools using
[Entry Points](http://packages.python.org/distribute/pkg_resources.html#entry-points).

In order to register reviewbot-jslint as a tool, run the following from the top-level reviewbot-jslint directory:

    python setup.py install

After a tool has been installed on a worker, it must be registered
with the Review Bot extension, and configured in the admin panel.
Registering tools is accomplished in the following manner:

  1. Go to the extension list in the admin panel.
  2. Click the 'DATABASE' button for the 'Review-Bot-Extension'.
  3. Click the 'Review bot tools' link.
  4. Click 'REFRESH INSTALLED TOOLS' in the upper right of the page.

This will trigger tool registration for all of the currently running
workers, and refresh the page. reviewbot-jslint should appear in the tools list as "JSLint Code Quality Tool".
