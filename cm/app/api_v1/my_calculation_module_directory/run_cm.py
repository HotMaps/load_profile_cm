from .load_profile.excess_heat import load_profile_gen


def main(res_heating_share, industry_share, tertiary_share, nuts2_id, output_directory):
    industry_profile_monthly, residential_heating_profile_monthly, tertiary_profile_monthly, effective_profile_monthly =\
        load_profile_gen(res_heating_share, industry_share, tertiary_share, nuts2_id, output_directory)

    graphics = [{
            "type": "line",
            "xLabel": "Month",
            "yLabel": "Load",
            "data": {
                "labels": ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                           "October", "November", "December"],
                "datasets": [{
                    "label": "Industry",
                    "borderColor": "#3CA879",
                    "backgroundColor": "rgba(62, 149, 205, 0)",
                    "data": industry_profile_monthly
                    },
                    {
                    "label": "Residential heating",
                    "borderColor": "#3CAEA7",
                    "backgroundColor": "rgba(254, 124, 96, 0)",
                    "data": residential_heating_profile_monthly
                    },
                    {
                        "label": "Tertiary sector",
                        "borderColor": "##3C8EB4",
                        "backgroundColor": "rgba(254, 124, 96, 0)",
                        "data": tertiary_profile_monthly
                    },
                    {
                        "label": "Effective",
                        "borderColor": "#3C63BA",
                        "backgroundColor": "rgba(254, 124, 96, 0)",
                        "data": effective_profile_monthly
                    }
                    ]
            }
        }]
    return graphics
