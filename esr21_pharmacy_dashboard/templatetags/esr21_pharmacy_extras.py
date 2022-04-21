from django import template

register = template.Library()


@register.inclusion_tag('esr21_pharmacy/buttons/issue_button.html')
def issue_button(model_wrapper):
    title = ['Issue Drugs']
    return dict(
        add_accountability_href=model_wrapper.accountability.href,
        tracking_identifier=model_wrapper.accountability.id,
        title=' '.join(title)
    )


@register.inclusion_tag('esr21_pharmacy/buttons/status_button.html')
def status_button(model_wrapper):
    title = model_wrapper.status
    statuses = ['Active', 'Quarantined']
    return dict(
        statuses=statuses,
        href_url='dropdown_menu_form/',
        model_wrapper=model_wrapper,
        title=' '.join(title)
    )


@register.inclusion_tag('esr21_pharmacy/buttons/order_button.html')
def order_button(model_wrapper):
    title = 'Oder Drugs'
    return dict(
        href=model_wrapper.href,
        title=' '.join(title)
    )
