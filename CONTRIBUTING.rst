Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/xarray-contrib/xncml/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

xncml could always use more documentation, whether as part of the official xncml docs, in docstrings, or even on the web in blog posts, articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/xarray-contrib/xncml/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome. :)

Get Started!
------------

.. note::

    If you are new to using GitHub and `git`, please read `this guide <https://guides.github.com/activities/hello-world/>`_ first.

Ready to contribute? Here's how to set up ``xncml`` for local development.

#. Fork the ``xncml`` repo on GitHub.
#. Clone your fork locally::

    git clone git@github.com:your_name_here/xncml.git

#. Install your local copy into a development environment. Using ``virtualenv`` (``virtualenvwrapper``), you can create a new development environment with::

    python -m pip install flit virtualenvwrapper
    mkvirtualenv xncml
    cd xncml/
    flit install --symlink

  This installs ``xncml`` in an "editable" state, meaning that changes to the code are immediately seen by the environment.

#. To ensure a consistent coding style, install the ``pre-commit`` hooks to your local clone::

   pre-commit install

  On commit, ``pre-commit`` will check that ``flake8``, and ``ruff`` checks are passing, perform automatic fixes if possible, and warn of violations that require intervention. If your commit fails the checks initially, simply fix the errors, re-add the files, and re-commit.

  You can also run the hooks manually with::

   pre-commit run -a

  If you want to skip the ``pre-commit`` hooks temporarily, you can pass the ``--no-verify`` flag to `git commit`.

#. Create a branch for local development::

   git checkout -b name-of-your-bugfix-or-feature

  Now you can make your changes locally.

#. When you're done making changes, we **strongly** suggest running the tests in your environment or with the help of ``tox``::

   python -m pytest
    # Or, to run multiple build tests
   tox

#. Commit your changes and push your branch to GitHub::

   git add .
   git commit -m "Your detailed description of your changes."
   git push origin name-of-your-bugfix-or-feature

  If ``pre-commit`` hooks fail, try re-committing your changes (or, if need be, you can skip them with `git commit --no-verify`).

#. Submit a `Pull Request <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request>`_ through the GitHub website.

#. When pushing your changes to your branch on GitHub, the documentation will automatically be tested to reflect the changes in your Pull Request. This build process can take several minutes at times. If you are actively making changes that affect the documentation and wish to save time, you can compile and test your changes beforehand locally with::

    # To generate the html and open it in your browser
   make docs
    # To only generate the html
   make autodoc
   make -C docs html
    # To simply test that the docs pass build checks
   tox -e docs

#. Once your Pull Request has been accepted and merged to the ``main`` branch, several automated workflows will be triggered:

    - The ``bump-version.yml`` workflow will automatically bump the patch version when pull requests are pushed to the ``main`` branch on GitHub. **It is not recommended to manually bump the version in your branch when merging (non-release) pull requests (this will cause the version to be bumped twice).**
    - `ReadTheDocs` will automatically build the documentation and publish it to the `latest` branch of `xncml` documentation website.
    - If your branch is not a fork (ie: you are a maintainer), your branch will be automatically deleted.

  You will have contributed your first changes to ``xncml``!

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

#. The pull request should include tests and should aim to provide `code coverage <https://en.wikipedia.org/wiki/Code_coverage>`_ for all new lines of code. You can use the ``--cov-report html --cov xncml`` flags during the call to ``pytest`` to generate an HTML report and analyse the current test coverage.

#. If the pull request adds functionality, the docs should also be updated. Put your new functionality into a function with a docstring, and add the feature to the list in ``README.rst``.

#. The pull request should work for Python 3.8, 3.9, 3.10, 3.11, and 3.12. Check that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

pytest tests.test_xncml

To run specific code style checks::

   black --check xncml tests
   isort --check xncml tests
   blackdoc --check xncml docs
   ruff xncml tests
   flake8 xncml tests

To get ``black``, ``isort``, ``blackdoc``, ``ruff``, and ``flake8`` (with plugins ``flake8-alphabetize`` and ``flake8-rst-docstrings``) simply install them with `pip` into your environment.
