"""Sunny Bliss account configuration (single source of truth for every script).

Values can also come from the environment (SUNNY_AD_ACCOUNT, SUNNY_PIXEL, ...), so a new ID
never needs a code change. None = not confirmed yet; scripts that need it stop and say so.
"""
import os, sys

env = lambda k: os.environ.get(k) or None

AD_ACCOUNT = env("SUNNY_AD_ACCOUNT") or "act_406803358900425"  # Sunny Bliss Plumbing & Air Ad Account
BUSINESS_ID = env("SUNNY_BUSINESS_ID")        # TODO
PAGE_ID = env("SUNNY_PAGE_ID") or "115885981512163"   # Sunny Bliss Plumbing & Air
INSTAGRAM_USER_ID = env("SUNNY_IG_ID") or "17841463167723871"  # @sunnybliss_plumbing_air
PIXEL_ID = env("SUNNY_PIXEL") or "1576525677606884"   # "Sunny Bliss Landing" (sunny-bliss.com); the other pixel, 1330015551637365, only sees PageView
PRIMARY_EVENT = env("SUNNY_EVENT") or "LEAD"  # TODO: LEAD / PURCHASE / SCHEDULE ...
LANDING = env("SUNNY_LANDING")                # TODO: "https://..."
TIMEZONE = env("SUNNY_TZ") or "America/New_York"
MAX_DAILY_BUDGET = None                       # TODO: USD/day ceiling; never exceeded without owner approval

# Campaigns whose name contains one of these are recruiting (job applicants), not customers.
HIRING_KEYWORDS = ("hiring",)

# Accounts of other clients: a Sunny Bliss script must never touch them.
FOREIGN_ACCOUNTS = {"act_1806647434085082"}   # OrchidPros

# Meta action types counted as the primary result, by event.
RESULT_TYPES = {
    # "lead" is Meta's total (pixel + instant form); the others are fallbacks when it is absent.
    "LEAD": ("lead", "offsite_conversion.fb_pixel_lead", "onsite_conversion.lead_grouped"),
    "PURCHASE": ("offsite_conversion.fb_pixel_purchase", "purchase", "omni_purchase"),
    "SCHEDULE": ("offsite_conversion.fb_pixel_schedule", "schedule"),
    "COMPLETE_REGISTRATION": ("offsite_conversion.fb_pixel_complete_registration", "complete_registration"),
}[PRIMARY_EVENT.upper()]


def require(*names):
    """Stop with a clear message if an ID the script needs is still unconfirmed."""
    missing = [n for n in names if not globals().get(n)]
    if missing:
        sys.exit(f"Falta confirmar en config.py o en el entorno: {', '.join(missing)}")
    if AD_ACCOUNT in FOREIGN_ACCOUNTS:
        sys.exit(f"{AD_ACCOUNT} es la cuenta de otro cliente, no de Sunny Bliss.")
