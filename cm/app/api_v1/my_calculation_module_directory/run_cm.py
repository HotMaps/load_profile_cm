from .load_profile.excess_heat import load_profile_gen


def main(res_heating_share, industry_share, tertiary_share, nuts2_id, output_directory):

    load_profile_gen(res_heating_share, industry_share, tertiary_share, nuts2_id, output_directory)



