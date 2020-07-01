# Doccano API Client

A simple client wrapper for the doccano API.

- [Doccano API Client](#doccano-api-client)
  - [History](#history)
  - [To-Do](#to-do)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Completion](#completion)
  - [Preemptive FAQ](#preemptive-faq)
  - [Contributing](#contributing)
  - [Credits](#credits)


## History

doccano users have consistently been interested in a way to programmatically access a doccano instance.

- In [Issue #6](https://github.com/doccano/doccano/issues/6#issuecomment-489924577), Hironsan provided a sample class to illustrate interaction with the doccano API.

- In [Issue #410](https://github.com/doccano/doccano/issues/410), louisguitton asked for assistance in using the API endpoints.

- In [Issue #299](https://github.com/doccano/doccano/issues/299#issuecomment-555692983), afparsons "figured out" how to upload files.

This project seeks to provide a temporary solution while the `doccano/doccano` team [creates an official package to call APIs.](https://github.com/doccano/doccano/issues/299#issuecomment-557037552)

---

## To-Do

- investigate more secure alternatives to plaintext login
- improve docstrings

---

## Prerequisites
- a doccano instance to which you may connect
- Python 3
- Python requests library

## Installation

```bash
cd <DESTINATION DIRECTORY>

git clone https://github.com/doccano/doccano_api_client.git

cd doccano_api_client

# to install normally
pip install ./

# to install with edit mode
pip install -e ./
```

## Usage

- Object instantiation takes care of session authorization.
- All methods return a `requests.models.Response` object.

```python
from doccano_api_client import DoccanoClient

# instantiate a client and log in to a Doccano instance
doccano_client = DoccanoClient(
    'http://doccano.example.com',
    'username',
    'password'
)

# get basic information about the authorized user
r_me = doccano_client.get_me()

# print the details from the above query
print(r_me())

# get the label text from project 1, label 3
label_text = doccano_client.get_label_detail(1, 3)()['text']

# upload a json file to project 1. If file is in current directory, file_path is omittable
r_json_upload = doccano_client.post_doc_upload(1, 'json', 'file.json', '/path/to/file/without/filename/')
```

## Completion

This wrapper's methods are based on doccano url [paths](https://github.com/chakki-works/doccano/blob/master/app/api/urls.py).

Key:

- ✔️ implemented
- ❌ not implemented
- ⚠️ currently broken or improperly implemented

Endpoint Names:

- ✔️ `auth-token`
- ✔️ `me`
- ✔️ `user_list`
- ✔️ `roles`
- ✔️ `features`
- ✔️ `project_list`
- ✔️ `project_detail`
- ✔️ `statistics`
- ✔️ `label_list`
- ✔️ `label_detail`
- ❌ `label_upload`
- ✔️ `doc_list`
- ✔️ `doc_detail`
- ✔️ `doc_uploader`
- ❌ `cloud_uploader`
- ✔️ `approve_labels`
- ✔️ `annotation_list`
- ⚠️ `annotation_detail`
- ✔️ `doc_downloader`
- ✔️ `rolemapping_list`
- ⚠️ `rolemapping_detail`

## Preemptive FAQ
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

> Can I contribute?

Please do! See _[Contributing]()_

## Contributing

1. Fork the main project.
2. Create an issue on [doccano/doccano_api_client](https://github.com/doccano/doccano_api_client/issues).
3. Make a feature or bugfix branch *on your fork* referencing the newly-created issue.
4. Commit to that branch.
5. Submit a pull request when ready.

## Development

Once you've cloned the repository and created a virtual environement, just run the following command

```sh
make develop
```

## Credits

Thanks to [Hironsan](https://github.com/Hironsan) and [louisguitton](https://github.com/louisguitton).
