## Page loader

[![Actions Status](https://github.com/Andrka/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/Andrka/python-project-lvl3/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/0f10d4df5001658af2bd/maintainability)](https://codeclimate.com/github/Andrka/python-project-lvl3/maintainability) <a href="https://codeclimate.com/github/Andrka/python-project-lvl3/test_coverage"><img src="https://api.codeclimate.com/v1/badges/0f10d4df5001658af2bd/test_coverage" /></a> [![Build Status](https://travis-ci.org/Andrka/python-project-lvl3.svg?branch=main)](https://travis-ci.org/Andrka/python-project-lvl3) [![Github Actions Status](https://github.com/Andrka/python-project-lvl3/workflows/Python%20CI/badge.svg)](https://github.com/Andrka/python-project-lvl3/actions)

"Page loader" is a written in Python utility, which download requested web page with local resources.

#### Installation with pip:

Before you start, you will need Python and pip on your computer. To install "Page loader", run the following command in your terminal:

`pip install --user -i https://test.pypi.org/simple andrka-page-loader --extra-index-url https://pypi.org/simple`

[![asciicast](https://asciinema.org/a/Vh7BxxMSmT5bjEx6Kv7cE8kYT.svg)](https://asciinema.org/a/Vh7BxxMSmT5bjEx6Kv7cE8kYT)

#### Start utility:

To get help with utility after installation, print and run in the terminal:

`page-loader -h`

(or: page-loader --help)

To start this utility print and run in the terminal:

`page-loader [--output path] [--log {full,errors}] full_url`

By default, output path will be the current directory and logging will be full.

[![asciicast](https://asciinema.org/a/ziRHTTljmPZzF0O10QpJ1niWh.svg)](https://asciinema.org/a/ziRHTTljmPZzF0O10QpJ1niWh)