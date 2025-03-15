from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PayerViewSet, PayerDetailViewSet, manual_mapping,upload_payer_file, manage_payer_groups,edit_payer_group,delete_payer_group, payer_hierarchy, edit_payer,delete_payer, unmap_payer

router = DefaultRouter()
router.register(r'payers', PayerViewSet)
router.register(r'payer_details', PayerDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('manual_mapping/', manual_mapping, name='manual_mapping'),
    path('upload/', upload_payer_file, name='upload_payer_file'),
    path("manage_payer_groups/", manage_payer_groups, name="manage_payer_groups"),
    path("edit_payer_group/<int:group_id>/", edit_payer_group, name="edit_payer_group"),
    path("delete_payer_group/<int:group_id>/", delete_payer_group, name="delete_payer_group"),
    path("payer_hierarchy/", payer_hierarchy, name="payer_hierarchy"),
    path("edit_payer/<int:payer_id>/", edit_payer, name="edit_payer"),  
    path("delete_payer/<int:payer_id>/", delete_payer, name="delete_payer"),
    path('unmap_payer/', unmap_payer, name='unmap_payer'),
]
