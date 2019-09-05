from .load_profile.load_profile import load_profile_gen


def main(res_heating_factor, ter_heating_factor, res_water_factor, ter_water_factor, heat_density_raster_res, heat_density_raster_nonres, gfa_res_curr_density, gfa_nonres_curr_density, nuts_id_number, output_directory):
    industry_profile_monthly,res_heating_profile_monthly, res_shw_profile_monthly, ter_heating_profile_monthly,\
    ter_shw_profile_monthly, effective_profile_monthly, total_industry, total_res_heating, total_res_shw, total_ter_heating,\
        total_ter_shw, total_heat =\
        load_profile_gen(res_heating_factor, ter_heating_factor, res_water_factor, ter_water_factor,
                         heat_density_raster_res, heat_density_raster_nonres, gfa_res_curr_density, gfa_nonres_curr_density, nuts_id_number, output_directory)

    graphics = [{
            "type": "line",
            "xLabel": "Month",
            "yLabel": "Power in MW",
            "data": {
                "labels": ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                           "October", "November", "December"],
                "datasets": [{
                    "label": "Industry",
                    "borderColor": "#57c635",
                    "backgroundColor": "rgba(62, 149, 205, 0)",
                    "data": industry_profile_monthly
                    },
                    {
                    "label": "Residential heating",
                    "borderColor": "#35c6a5",
                    "backgroundColor": "rgba(254, 124, 96, 0)",
                    "data": res_heating_profile_monthly
                    },
                    {
                    "label": "Residential warm water supply",
                    "borderColor": "#a535c6",
                    "backgroundColor": "rgba(254, 124, 96, 0)",
                    "data": res_shw_profile_monthly
                    },
                    {
                    "label": "Tertiary heating",
                    "borderColor": "#c63557",
                    "backgroundColor": "rgba(254, 124, 96, 0)",
                    "data": ter_heating_profile_monthly
                    },
                    {
                    "label": "Tertiary warm water supply",
                    "borderColor": "#c6a535",
                    "backgroundColor": "rgba(254, 124, 96, 0)",
                    "data": ter_shw_profile_monthly
                    },
                    {
                    "label": "Effective",
                    "borderColor": "#3557c6",
                    "backgroundColor": "rgba(254, 124, 96, 0)",
                    "data": effective_profile_monthly
                    }
                    ]
            }
        }]
    return graphics, total_industry, total_res_heating, total_res_shw, total_ter_heating, total_ter_shw, total_heat
