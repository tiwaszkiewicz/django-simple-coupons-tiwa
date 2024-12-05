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
from django.utils.crypto import get_random_string
from django.contrib import admin
from .models import Coupon, Discount, Ruleset

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'ruleset', 'times_used', 'created', )
    actions = [delete_expired_coupons, generate_coupons_action]  # Dodajemy nową akcję

    @admin.action(description='Generate new coupons')
    def generate_coupons_action(self, request, queryset):
        """
        Tworzy nowe kupony w bazie danych niezależnie od zaznaczonych.
        """
        prefix = "NEW_"  # Możesz wprowadzić logikę do ustawiania tego dynamicznie
        count = 5        # Liczba kuponów do wygenerowania
        discount = Discount.objects.first()  # Pobierz istniejącą zniżkę
        ruleset = Ruleset.objects.first()    # Pobierz istniejący zestaw zasad

        if not discount or not ruleset:
            self.message_user(request, "Error: Missing Discount or Ruleset", level="error")
            return

        created_coupons = []
        for _ in range(count):
            random_part = get_random_string(length=30 - len(prefix))
            code = f"{prefix}{random_part}"
            coupon = Coupon.objects.create(
                code=code,
                discount=discount,
                ruleset=ruleset
            )
            created_coupons.append(coupon)

        self.message_user(request, f"Successfully created {len(created_coupons)} new coupons.")    


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
    
    



