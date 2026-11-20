"""Nov 20 (user order "Hazlo"): LPV ad sets drop low-intent placements (Facebook Reels overlay, Marketplace, search,
Audience Network) and cap age at 64. Kept: FB feed, FB stories, FB Reels, IG feed, IG stories, IG Reels.
Audience, ads and budget unchanged. Usage: python3 placements_nov20.py [--validate]"""
import json, sys
from meta import get, post

SETS = ["120257891824390196", "120257891833940196"]
EX = {"execution_options": ["validate_only"]} if "--validate" in sys.argv else {}
for s in SETS:
    t = get(s, fields="targeting")["targeting"]
    t.update(age_max=64, publisher_platforms=["facebook", "instagram"],
             facebook_positions=["feed", "story", "facebook_reels"], instagram_positions=["stream", "story", "reels"],
             device_platforms=["mobile", "desktop"])
    for k in ("audience_network_positions", "messenger_positions"):
        t.pop(k, None)
    print(s, post(s, targeting=t, **EX))
