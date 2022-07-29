import csv


def calculate_recovery_death_cases_count():
    countries_count = 0
    total_cases = 0
    total_deaths = 0
    total_recovered_cases = 0
    seen_countries = []

    with open('covid_cases_stats.csv') as covid_data:
        covid_reader = csv.DictReader(covid_data)
        for row in covid_reader:
            if row['country'] not in (single_country['country'] for single_country in seen_countries):
                seen_countries.append(row)

    for country in seen_countries:
        if country['country'] != '':
            countries_count += 1
        if country['total_deaths'] != '':
            total_deaths += int(country['total_deaths'])
        if country['total_cases'] != '':
            total_cases += int(country['total_cases'])
        if country['total_recovered'] != '':
            total_recovered_cases += int(country['total_recovered'])

    return dict(total_countries=countries_count,
                total_cases=total_cases,
                total_deaths=total_deaths,
                total_recovered_cases=total_recovered_cases,
                covid_data=seen_countries)


def given_country_stats(country_name, covid_data):
    for row in covid_data:
        if str(country_name) == row['country']:
            ratio_value = int(row['total_recovered']) / int(row['total_cases'])
            return round(ratio_value, 2)


def economic_measure(economic_measure_param, total_cases, total_deaths):
    if str(economic_measure_param).lower() == str('Economic measures').lower():
        getting_total_ratios = (total_deaths * 100) / total_cases

        return round(getting_total_ratios, 2)


def safety_measure(safety_measure_param, total_recovered_cases, total_cases):
    count_economic_measures = 0
    limit_public_gatherings = 0
    quarantine_policies = 0
    public_health_system = 0
    flight_suspension = 0

    with open('covid_safety_measures.csv') as covid_safety_measure:
        reader_covid_measures = csv.DictReader(covid_safety_measure)
        if str(safety_measure_param) == '-c':
            for row in reader_covid_measures:
                if row['measure'] == 'Economic measures':
                    count_economic_measures += 1
                if row['measure'] == 'Limit public gatherings':
                    limit_public_gatherings += 1
                if row['measure'] == 'Introduction of quarantine policies':
                    quarantine_policies += 1
                if row['measure'] == 'Strengthening the public health system':
                    public_health_system += 1
                if row['measure'] == 'International flights suspension':
                    flight_suspension += 1

            calculate_efficiency = total_recovered_cases / total_cases
            count_economic_measures = count_economic_measures / calculate_efficiency
            limit_public_gatherings = limit_public_gatherings / calculate_efficiency
            quarantine_policies = quarantine_policies / calculate_efficiency
            public_health_system = public_health_system / calculate_efficiency
            flight_suspension = flight_suspension / calculate_efficiency

    return dict(economic_measures=int(count_economic_measures),
                public_gatherings=int(limit_public_gatherings),
                quarantine_policies=int(quarantine_policies),
                public_health_system=int(public_health_system),
                flight_suspension=int(flight_suspension))


if __name__ == '__main__':
    all_stats = calculate_recovery_death_cases_count()

    # Check Country Stats by Name

    country_name = input("")
    getting_ratio = given_country_stats(country_name.lstrip('-a '),
                                        all_stats['covid_data'])
    if getting_ratio != None:
        print('Recovered/total ratio: ', getting_ratio)

    print("=================================End Task 1=================================")

    # Searching for Econimical Measures

    economic_measure_param = input("")
    getting_total_ratios = economic_measure(economic_measure_param.lstrip('-b '),
                                            all_stats['total_cases'],
                                            all_stats['total_deaths'])
    if getting_total_ratios != None:
        print(getting_total_ratios, '% death average found in', all_stats["total_countries"], 'countries.')

    print("=================================End Task 2=================================")

    # Calculate Safety Measures

    safety_measure_param = input("")
    safety_measure_data = safety_measure(safety_measure_param,
                                         all_stats['total_recovered_cases'],
                                         all_stats['total_cases'])
    print('Economic measures: ', safety_measure_data['economic_measures'])
    print('Limit public gatherings:', safety_measure_data['public_gatherings'])
    print('Introduction of quarantine policies:', safety_measure_data['quarantine_policies'])
    print('Strengthening the public health system:', safety_measure_data['public_health_system'])
    print('International flights suspension:', safety_measure_data['flight_suspension'])

    print("=================================End Task 3=================================")
