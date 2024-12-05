from django.contrib import admin # type: ignore

from django_simple_coupons.models import (Coupon,
                                          Discount,
                                          Ruleset,
                                          CouponUser,
                                          AllowedUsersRule,
                                          MaxUsesRule,
                                          ValidityRule)

from django_simple_coupons.actions import (reset_coupon_usage, delete_expired_coupons, generate_coupons_action)


# Register your models here.
# ==========================
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'times_used', 'created')

    def changelist_view(self, request, extra_context=None):
        """
        Przekazanie dodatkowego kontekstu do widoku listy obiektów.
        """
        extra_context = extra_context or {}
        # Dodaj link do swojej akcji lub widoku
        extra_context['additional_button'] = format_html(
            '<a class="button" href="/">Generate Coupons</a>',
            reverse('admin:generate-coupons')  # Zamień na odpowiednią nazwę widoku
        )
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(Ruleset)
class RulesetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'allowed_users', 'max_uses', 'validity', )


@admin.register(CouponUser)
class CouponUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'times_used', )
    actions = [reset_coupon_usage]


@admin.register(AllowedUsersRule)
class AllowedUsersRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(MaxUsesRule)
class MaxUsesRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(ValidityRule)
class ValidityRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}
    
    



