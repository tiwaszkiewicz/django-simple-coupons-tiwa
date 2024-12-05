from django.contrib.admin import ModelAdmin
from django.utils import timezone


# Create your actions here
# ========================
def reset_coupon_usage(modeladmin, request, queryset):
    for coupon_user in queryset:
        coupon_user.times_used = 0
        coupon_user.save()

    ModelAdmin.message_user(modeladmin, request, "Coupons reseted!")


def delete_expired_coupons(modeladmin, request, queryset):
    count = 0
    for coupon in queryset:
        expiration_date = coupon.ruleset.validity.expiration_date
        if timezone.now() >= expiration_date:
            coupon.delete()
            count += 1

    ModelAdmin.message_user(modeladmin, request, "{0} Expired coupons deleted!".format(count))


# Actions short descriptions
# ==========================
reset_coupon_usage.short_description = "Reset coupon usage"
delete_expired_coupons.short_description = "Delete expired coupons"


from django.utils.crypto import get_random_string

def generate_coupons_action(modeladmin, request, queryset):
    """
    Action to generate multiple coupons with a specified prefix.
    """
    prefix = "JANEK_"  # Możesz ustawić prefiks na stałe lub dodać logikę pobierania go od użytkownika
    count = 5          # Liczba kuponów do wygenerowania
    generated_count = 0

    for _ in range(count):
        random_part = get_random_string(length=30 - len(prefix))
        code = f"{prefix}{random_part}"

        for coupon in queryset:
            coupon.ruleset.coupons.create(
                code=code,
                discount=coupon.discount,
                ruleset=coupon.ruleset,
                created=timezone.now()
            )
            generated_count += 1

    modeladmin.message_user(request, f"{generated_count} coupons generated with prefix {prefix}!")

generate_coupons_action.short_description = "Generate multiple coupons with prefix"