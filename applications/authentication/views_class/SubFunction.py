from .commonImport import *


@api_view(["GET"])
def download_file(request, pk):
    # Retrieve the UploadedFile instance by its primary key (pk)
    # uploaded_file = get_object_or_404(UploadedFile, pk=pk)
    user = get_object_or_404(get_user_model(), pk=pk)
    # Use FileResponse to serve the file
    # The as_attachment=True parameter prompts the browser to download the file
    # return FileResponse(uploaded_file.file.open(), as_attachment=True)
    return Response({
        "file_link": user.profile_img.url
    })

def get_object(pk):
    user = get_user_model()
    try:
        return user.objects.get(pk=pk)
    except user.DoesNotExist:
        raise Http404



@api_view(["GET"])
def set_password(request, password):
    return Response({
        "password": make_password(password)
    })

