"""Campaign configuration (single source of truth). Values marked TODO are filled after user confirmation."""

AD_ACCOUNT = "act_1806647434085082"  # OrchidPros (confirmed by user)
PAGE_ID = None                        # TODO: confirm in step 1
INSTAGRAM_USER_ID = None              # TODO: confirm in step 1
PIXEL_ID = "2271987886986577"

CAMPAIGN_NAME = "ORCHID - Leads - Hire a VA - 2026-10"
ADSET_NAME = "ORCHID - US - 30-65 - Owners Legal RE Health - 2026-10"
AD_NAME = "ORCHID - C{n} - {angle} - 2026-10"

DAILY_BUDGET = 3289                   # USD cents = 32.89/day
START_TIME = "2026-10-01T00:00:00-0400"  # 00:00 America/New_York (EDT, UTC-4)
LINK = "https://go.orchidpros.com/hire"
URL_TAGS = ("utm_source={{site_source_name}}&utm_medium=paid_social&utm_campaign={{campaign.name}}"
            "&utm_term={{adset.name}}&utm_content={{ad.name}}&utm_id={{campaign.id}}&placement={{placement}}")
CTA = "BOOK_NOW"                      # approved by user 2026-10-08 (matches "Book a free call" on the landing)

# Detailed targeting signals; filled with real IDs from step2_audience.py after approval
INTEREST_QUERIES = {
    "General": ["Small business", "Entrepreneurship"],
    "Legal": ["Law firm", "Lawyer", "Legal services", "Paralegal"],
    "Real estate": ["Realtor", "Real estate broker", "Real estate investing"],
    "Health": ["Medical practice", "Private practice"],
}
BEHAVIOR_QUERIES = ["Small business owners", "Business page admins"]
APPROVED_INTERESTS = []               # TODO: [{"id": "...", "name": "..."}] after step 2 approval
APPROVED_BEHAVIORS = []               # TODO
EXCLUDED_CUSTOM_AUDIENCES = []        # TODO: [{"id": "..."}] only if the user approves
ENGLISH_LOCALES = []                  # TODO: filled from adlocale search in step 1


def targeting():
    t = {
        "geo_locations": {"countries": ["US"], "location_types": ["home"]},
        "age_min": 30,
        "age_max": 65,
        "genders": [1, 2],
        "targeting_automation": {"advantage_audience": 0},
        "publisher_platforms": ["facebook", "instagram"],
        "facebook_positions": ["feed", "profile_feed", "video_feeds", "story", "facebook_reels"],
        "instagram_positions": ["stream", "story", "reels", "explore", "explore_home", "profile_feed"],
        "device_platforms": ["mobile", "desktop"],
    }
    if ENGLISH_LOCALES:
        t["locales"] = ENGLISH_LOCALES
    flex = {}
    if APPROVED_INTERESTS:
        flex["interests"] = APPROVED_INTERESTS
    if APPROVED_BEHAVIORS:
        flex["behaviors"] = APPROVED_BEHAVIORS
    if flex:
        t["flexible_spec"] = [flex]  # OR across all signals: one audience, not split by vertical
    if EXCLUDED_CUSTOM_AUDIENCES:
        t["excluded_custom_audiences"] = EXCLUDED_CUSTOM_AUDIENCES
    return t


PROMOTED_OBJECT = {"pixel_id": PIXEL_ID, "custom_event_type": "LEAD"}
ATTRIBUTION_SPEC = [{"event_type": "CLICK_THROUGH", "window_days": 7},
                    {"event_type": "VIEW_THROUGH", "window_days": 1}]

# Advantage+ creative: every enhancement opted out. If the API rejects a key, the build stops and reports it.
CREATIVE_FEATURES_OPT_OUT = [
    "text_optimizations", "text_generation", "image_touchups", "image_brightness_and_contrast",
    "image_uncrop", "image_templates", "image_animation", "video_auto_crop", "video_filtering",
    "adapt_to_placement", "add_text_overlay", "enhance_cta", "inline_comment", "description_automation",
    "reveal_details_over_time", "site_extensions", "product_extensions", "profile_card", "show_summary",
    "audio", "music",
]

# Concepts: filled after inspect_creatives.py. angle = short label used in the ad name.
# {"n": 1, "angle": "Time Back", "vertical": "creatives/c1_9x16.mp4", "feed": "creatives/c1_4x5.mp4"}
CONCEPTS = []
