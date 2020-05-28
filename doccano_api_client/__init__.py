"""
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import os
import requests
from urllib.parse import urljoin

# ------------------------------------------------------------------------
# ROUTER
# ------------------------------------------------------------------------
class _Router:
    """
    Provides generic `get` and `post` methods. Implemented by DoccanoClient.
    """

    def get(
        self,
        endpoint: str,
    ) -> requests.models.Response:
        """
        Args:
            endpoint (str): An API endpoint to query.

        Returns:
            requests.models.Response: The request response.
        """
        request_url = urljoin(self.baseurl, endpoint)
        return self.session.get(request_url)

    def post(
        self,
        endpoint: str,
        data: dict = {},
        files: dict = {}
    ) -> requests.models.Response:
        """
        """
        request_url = urljoin(self.baseurl, endpoint)
        return self.session.post(request_url, data=data, files=files)

    def build_url_parameter(
        self,
        url_parameter: dict
    ) -> str:
        """
        Format url_parameters.

        Args:
            url_parameter (dict): Every value must be a list.

        Returns:
            A URL parameter string. Ex: `?key1=u1&key1=u2&key2=v1&...`
        """
        return ''.join(['?', '&'.join(['&'.join(['='.join([tup[0], str(value)]) for value in tup[1]]) for tup in url_parameter.items()])])

# ------------------------------------------------------------------------
# CLIENT
# ------------------------------------------------------------------------
class DoccanoClient(_Router):
    """
    TODO: investigate alternatives to plaintext login

    Args:
        baseurl (str): The baseurl of a Doccano instance.
        username (str): The Doccano username to use for the client session.
        password (str): The respective username's password.

    Returns:
        An authorized client instance.
    """
    def __init__(self, baseurl: str, username: str, password: str):
        self.baseurl = baseurl if baseurl[-1] == '/' else baseurl+'/'
        self.session = requests.Session()
        self._login(username, password)

    def _login(
        self,
        username: str,
        password: str
    ) -> requests.models.Response:
        """
        Authorizes the DoccanoClient instance.

        Args:


        Returns:
            requests.models.Response: The authorization request response.
        """
        url = 'v1/auth-token'
        auth = {'username': username, 'password': password}
        response = self.post(url, auth)
        print(response)
        token = response.json()['token']
        self.session.headers.update(
            {
                'Authorization': 'Token {token}'.format(token=token),
                'Accept': 'application/json'
            }
        )
        return response

    def get_me(self) -> requests.models.Response:
        """
        Gets this account information.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/me')

    def get_features(self) -> requests.models.Response:
        """
        Gets features.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/features')

    def get_project_list(self) -> requests.models.Response:
        """
        Gets projects list.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/projects')

    def get_user_list(self) -> requests.models.Response:
        """
        Gets user list.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/users')

    def get_roles(self) -> requests.models.Response:
        """
        Gets available Doccano user roles.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/roles')

    def get_project_detail(
        self,
        project_id: int
    ) -> requests.models.Response:
        """
        Gets details of a specific project.

        Args:
            project_id (int): A project ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}'.format(
                project_id=project_id
            )
        )

    def get_project_statistics(
        self,
        project_id: int
    ) -> requests.models.Response:
        """
        Gets project statistics.

        Args:
            project_id (int): A project ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/statistics'.format(
                project_id=project_id
            )
        )

    def get_label_list(
        self,
        project_id: int
    ) -> requests.models.Response:
        """
        Gets a list of labels in a given project.

        Args:
            project_id (int): A project ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/labels'.format(
                project_id=project_id
            )
        )

    def get_label_detail(
        self,
        project_id: int,
        label_id: int
    ) -> requests.models.Response:
        """
        Gets details of a specific label.

        Args:
            project_id (int): A project ID to query.
            label_id (int): A label ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/labels/{label_id}'.format(
                project_id=project_id,
                label_id=label_id
            )
        )

    def get_document_list(
        self,
        project_id: int,
        url_parameters: dict = {}
    ) -> requests.models.Response:
        """
        Gets a list of documents in a project.

        Args:
            project_id (int):
            url_parameters (dict): `limit` and `offset`

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/docs{url_parameters}'.format(
                project_id=project_id,
                url_parameters=self.build_url_parameter(url_parameters)
            )
        )

    def get_document_detail(
        self,
        project_id: int,
        doc_id: int
    ) -> requests.models.Response:
        """
        Gets details of a given document.

        Args:
            project_id (int): A project ID to query.
            doc_id (int): A document ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/docs/{doc_id}'.format(
                project_id=project_id,
                doc_id=doc_id
            )
        )

    def get_annotation_list(
        self,
        project_id: int,
        doc_id: int
    ) -> requests.models.Response:
        """
        Gets a list of annotations in a given project and document.

        Args:
            project_id (int): A project ID to query.
            doc_id (int): A document ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/docs/{doc_id}/annotations'.format(
                project_id=project_id,
                doc_id=doc_id
            )
        )

    def get_annotation_detail(
        self,
        project_id: int,
        doc_id: int,
        annotation_id: int
    ) -> requests.models.Response:
        """
        """
        return self.get(
            'v1/projects/{project_id}/docs/{doc_id}/annotations/{annotation_id}'.format(
                project_id=project_id,
                doc_id=doc_id,
                annotation_id=annotation_id
            )
        )

    def get_doc_download(
        self,
        project_id: int,
        file_format: str = 'json'
    ) -> requests.models.Response:
        """
        """
        return self.get(
            'v1/projects/{project_id}/docs/download?q={file_format}'.format(
                project_id=project_id,
                file_format=file_format
            )
        )

    def get_rolemapping_list(
        self,
        project_id: int,
    ) -> requests.models.Response:
        """
        """
        return self.get(
            'v1/projects/{project_id}/roles'.format(
                project_id=project_id
            )
        )

    def get_rolemapping_detail(
        self,
        project_id: int,
        rolemapping_id: int,
    ) -> requests.models.Response:
        """
        Currently broken!
        """
        return self.get(
            'v1/projets/{project_id}/roles/{rolemapping_id}'.format(
                project_id=project_id,
                rolemapping_id=rolemapping_id
            )
        )

    def post_doc_upload(
        self,
        project_id: int,
        file_format: str,
        file_name: str,
        file_path: str = './',
    ) -> requests.models.Response:
        """
        Uploads a file to a Doccano project.

        Args:
            project_id (int): The project id number.
            file_format (str): The file format, ex: `plain`, `json`, or `conll`.
            file_name (str): The name of the file.
            file_path (str): The parent path of the file. Defaults to `./`.

        Returns:
            requests.models.Response: The request response.
        """
        files = {
            'file': (
                file_name,
                open(os.path.join(file_path, file_name), 'rb')
            )
        }
        data = {
            'file': (
                file_name,
                open(os.path.join(file_path, file_name), 'rb')
            ),
            'format': file_format
        }
        return self.post(
            'v1/projects/{project_id}/docs/upload'.format(
                project_id=project_id
            ),
            files=files,
            data=data
        )

    def post_approve_labels(
        self,
        project_id: int,
        doc_id: int
    ) -> requests.models.Response:
        """
        """
        return self.post(
            'v1/projects/{project_id}/docs/{doc_id}/approve-labels'.format(
                project_id=project_id,
                doc_id=doc_id
            )
        )

    def _get_any_endpoint(
        self,
        endpoint: str
    ) -> requests.models.Response:
        """
        """
        # project_id: int,
        # limit: int,
        # offset: int
        return self.get(endpoint)

    def exp_get_doc_list(
        self,
        project_id: int,
        limit: int,
        offset: int
    ) -> requests.models.Response:
        """
        """
        return self.get(
            'v1/projects/{project_id}/docs?limit={limit}&offset={offset}'.format(
                project_id=project_id,
                limit=limit,
                offset=offset
            )
        )
