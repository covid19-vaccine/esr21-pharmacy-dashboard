from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .requisitions_model_wrapper import RequisitionsModelWrapper


class RequisitionModelWrapperMixin:
    requisition_model_wrapper_cls = RequisitionsModelWrapper

    @property
    def requisition_model_obj(self):
        try:
            return self.requisition_cls.objects.get(
                **self.requisition_options)
        except ObjectDoesNotExist:
            return None

    @property
    def requisition(self):
        model_obj = self.requisition_model_obj or self.requisition_cls(
            **self.create_requisition_options)
        return self.requisition_model_wrapper_cls(model_obj=model_obj)

    @property
    def requisition_cls(self):
        return django_apps.get_model('esr21_pharmacy.drugrequisition')

    @property
    def create_requisition_options(self):
        options = dict(
            tracking_identifier=self.tracking_identifier,
            injection_site=self.injection_site,
            quantity_order=self.quantity_order,
            )
        return options

    def requisition_options(self):
        options = dict(
            tracking_identifier=self.tracking_identifier,
            injection_site=self.injection_site,
            quantity_order=self.quantity_order,
            )
        return options
