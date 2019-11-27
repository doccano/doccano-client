# Doccano API Client

A simple client wrapper for the doccano API.

**History**

doccano users have consistently been interested in a way to programmatically access a doccano instance.

- In [Issue #6](https://github.com/chakki-works/doccano/issues/6#issuecomment-489924577), Hironsan provided a sample class to illustrate interaction with the doccano API. 

- In [Issue #410](https://github.com/chakki-works/doccano/issues/410), louisguitton asked for assistance in using the API endpoints.

- In [Issue #299](https://github.com/chakki-works/doccano/issues/299#issuecomment-555692983), afparsons "figured out" how to upload files.

This project seeks to provide a temporary solution while the `chakki-works/doccano` team [creates an official package to call APIs.](https://github.com/chakki-works/doccano/issues/299#issuecomment-557037552)

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
git clone <THIS REPOSITORY>

cd <THIS REPOSITORY>

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
print(r_me.json())

# get the label text from project 1, label 3
label_text = doccano_client.get_label_detail(1, 3).json()['text']

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

## Credits

Thanks to [Hironsan](https://github.com/Hironsan) and [louisguitton](https://github.com/louisguitton).