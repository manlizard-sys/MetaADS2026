"""Targeting definitions for the November 2026 campaigns (shared by launch and reports)."""
OWNERS = {"behaviors": [{"id": "6002714898572", "name": "Small business owners"},
                        {"id": "6020530281783", "name": "Business page admins"}]}
VERTICALS = {
    # "Lawyer" alone reaches ~55M people (mostly consumers); law-practice interests keep it on firms.
    "Legal": [{"interests": [{"id": "6003057724244", "name": "Law firm"}, {"id": "6003029225585", "name": "Bar association"}]}, OWNERS],
    "RealEstate": [{"interests": [{"id": "6003446239080", "name": "Real estate investing"},
                                  {"id": "6003365135251", "name": "Property management"},
                                  {"id": "6003332796032", "name": "Real estate development"}]}, OWNERS],
    "Accounting": [{"interests": [{"id": "6003138589139", "name": "Accounting"},
                                  {"id": "6002984410123", "name": "Certified Public Accountant"},
                                  {"id": "6003122830124", "name": "Tax preparation"}]}, OWNERS],
    "Finance": [{"interests": [{"id": "6003174867249", "name": "Financial services"},
                               {"id": "6003215620345", "name": "Financial adviser"},
                               {"id": "6003217093576", "name": "Insurance"}]}, OWNERS],
    "Entrepreneurs": [{"interests": [{"id": "6003371567474", "name": "Entrepreneurship"},
                                     {"id": "6002884511422", "name": "Small business"}]}, OWNERS],
    "Healthcare": [{"work_positions": [{"id": "108768179146852", "name": "Dentist"},
                                       {"id": "149072445110317", "name": "Chiropractor/Owner"},
                                       {"id": "148866958458716", "name": "Physical Therapist"},
                                       {"id": "911356208895948", "name": "Practice Manager"},
                                       {"id": "1569299249954237", "name": "Medical Practice Manager"},
                                       {"id": "1595394480678734", "name": "Dental Office Manager"}]}],
}
PLACEMENTS = {"publisher_platforms": ["facebook", "instagram"],
              "facebook_positions": ["feed", "story", "facebook_reels"],
              "instagram_positions": ["stream", "story", "reels"]}


def targeting(flex, age_min=25, age_max=65):
    return {"geo_locations": {"countries": ["US"], "location_types": ["home", "recent"]},
            "age_min": age_min, "age_max": age_max, "flexible_spec": flex,
            "targeting_automation": {"advantage_audience": 0}, **PLACEMENTS}

# Lead prospecting: law-practice interests (incl. "Lawyer") AND small-business owners / page admins -> solo & small firms.
ATTORNEYS = [{"interests": [{"id": "6003057724244", "name": "Law firm"}, {"id": "6003392101554", "name": "Lawyer"},
                            {"id": "6003029225585", "name": "Bar association"}]}, OWNERS]
