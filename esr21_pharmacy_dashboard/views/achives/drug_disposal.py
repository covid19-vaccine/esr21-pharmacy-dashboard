import io
import mimetypes
import os
from wsgiref.util import FileWrapper

from django.conf import settings
from django.http.response import HttpResponse
from django.utils.encoding import smart_str


def DrugDisposal(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    filename = 'drug_disposal_form.pdf'

    media_dir = settings.MEDIA_ROOT

    filepath = media_dir + '/document/' + filename

    buffer.seek(0)

    file_wrapper = FileWrapper(open(filepath, 'rb'))
    file_mimetype = mimetypes.guess_type(filepath)
    response = HttpResponse(file_wrapper, content_type=file_mimetype)
    response['X-Sendfile'] = filepath
    response['Content-Length'] = os.stat(filepath).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filepath)

    return response
