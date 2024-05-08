
from .views_class.ProductViewClass import *
from .views_class.TypeProductClass import *


# import os
# from pathlib import Path
# @api_view(["GET"])
# def list_media_files(request):
#     BASE_DIR = Path(__file__).resolve().parent.parent.parent
#     media_root = os.path.join(BASE_DIR, 'media') # Assuming BASE_DIR is defined in your settings
#     media_files = []
#     for root, dirs, files in os.walk(media_root):
#         for file in files:
#             file_path = os.path.join(root, file)
#             media_files.append(file_path)

#     return Response({'media_files': media_files})
