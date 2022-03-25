from django.conf import settings
from edc_model_wrapper import ModelWrapper


class DashboardViewModelWrapper(ModelWrapper):
    model = 'trainee_subject.subjectscreening'
    querystring_attrs = ['screening_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get('screening_listboard_url')
