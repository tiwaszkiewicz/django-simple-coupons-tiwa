from django_simple_coupons.models import Coupon, CouponUser
from django.utils import timezone


INVALID_TEMPLATE = {
    "valid": False,
    "message": ""
}

VALID_TEMPLATE = {
    "valid": True
}


def assemble_invalid_message(message=""):
    response = INVALID_TEMPLATE
    response['message'] = message
    return response


def validate_allowed_users_rule(coupon_object, user):
    allowed_users_rule = coupon_object.ruleset.allowed_users
    if not user in allowed_users_rule.users.all():
        return False if not allowed_users_rule.all_users else True

    return True


def validate_max_uses_rule(coupon_object, user):
    max_uses_rule = coupon_object.ruleset.max_uses
    #if coupon_object.times_used >= max_uses_rule.max_uses and not max_uses_rule.is_infinite:
    #    return False

    try:
        #coupon_user = CouponUser.objects.get(user=user)
        coupon_user = coupon_object
        if coupon_user.times_used >= max_uses_rule.uses_per_user:
            return False
    except CouponUser.DoesNotExist:
        pass

    return True


def validate_validity_rule(coupon_object):
    validity_rule = coupon_object.ruleset.validity
    if timezone.now() > validity_rule.expiration_date:
        return False

    return validity_rule.is_active


def validate_coupon(coupon_code, user):
    if not coupon_code:
        return assemble_invalid_message(message="Nie podano kodu kuponu!")

    if not user:
        return assemble_invalid_message(message="Nie podano użytkownika!")

    try:
        coupon_object = Coupon.objects.get(code=coupon_code)
    except Coupon.DoesNotExist:
        return assemble_invalid_message(message="Kupon nie istnieje!")

    valid_allowed_users_rule = validate_allowed_users_rule(coupon_object=coupon_object, user=user)
    if not valid_allowed_users_rule:
        return assemble_invalid_message(message="Kupon jest nieważny dla tego użytkownika!")

    valid_max_uses_rule = validate_max_uses_rule(coupon_object=coupon_object, user=user)
    if not valid_max_uses_rule:
        return assemble_invalid_message(message="Przekroczono limit użyć kuponu dla tego użytkownika!")

    valid_validity_rule = validate_validity_rule(coupon_object=coupon_object)
    if not valid_validity_rule:
        return assemble_invalid_message(message="Kupon jest nieważny!")

    return VALID_TEMPLATE
