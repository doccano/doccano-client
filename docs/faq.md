# FAQ

> Why doesn't this package's source code use f-strings (PEP 498)?

F-strings are available for Python 3.6+. I wanted to be able to support slightly older versions of Python.

> What kind of code formatting/style does this package use?

I've not yet prescribed a style guide. However:
- I generally like [Python Black](https://github.com/psf/black).
- I've provided [Google-style docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) throughout the source code.

> Does this API client support <some_feature> in doccano (deleting, etc.)?

Probably not (yet). A few things to note:
- everything I know about the endpoints is listed in the [README.md](https://github.com/doccano/doccano_api_client/blob/master/README.md#history) file.
- this was only supposed to be a temporary solution! I guess the doccano team hasn't yet [made their own client](https://github.com/doccano/doccano/issues/299#issuecomment-557037552)?
- I based the API client code off of what I could find in [doccano's source code](https://github.com/doccano/doccano/blob/master/app/api/urls.py), but I wasn't able to find much documentation to begin with.
- I originally created this API client to quickly solve a problem I had at work; the [supported endpoints](https://github.com/doccano/doccano_api_client/blob/master/README.md#completion) came in order of my own personal requirement!
