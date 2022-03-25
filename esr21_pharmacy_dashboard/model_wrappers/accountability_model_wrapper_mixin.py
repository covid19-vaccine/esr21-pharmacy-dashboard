from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from esr21_pharmacy_dashboard.model_wrappers import AccountabilityModelWrapper


class AccountabilityModelWrapperMixin:
    accountability_model_wrapper_cls = AccountabilityModelWrapper

    @property
    def accountability_model_obj(self):
        try:
            return self.accountability_cls.objects.get(
                **self.accountability_options)
        except ObjectDoesNotExist:
            return None

    @property
    def accountability(self):
        model_obj = self.accountability_model_obj or self.accountability_cls(
            **self.create_accountability_options)
        return self.accountability_model_wrapper_cls(model_obj=model_obj)

    @property
    def accountability_cls(self):
        return django_apps.get_model('esr21_pharmacy.drugaccountabilitylog')

    @property
    def create_accountability_options(self):
        options = dict(
            tracking_identifier=self.tracking_identifier,
            injection_site=self.injection_site,
            quantity_order=self.quantity_order,
        )
        return options

    @property
    def accountability_options(self):
        options = dict(
            tracking_identifier=self.tracking_identifier,
            injection_site=self.injection_site,
            quantity_order=self.quantity_order,
        )
        return options
