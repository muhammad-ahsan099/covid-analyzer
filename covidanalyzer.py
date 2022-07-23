import csv


def total_country_cases_deaths(total_country,
                               total_cases,
                               total_deaths,
                               total_recovered_cases):
    with open('covid_cases_stats.csv') as file_obj:
        reader_obj = csv.DictReader(file_obj)
        for row in reader_obj:
            if row['country'] != 'Total:':
                if row['country']:
                    total_country += 1
                if row['total_deaths']:
                    total_deaths += int(row['total_deaths'])
                if row['total_cases']:
                    total_cases += int(row['total_cases'])
                if row['total_recovered']:
                    total_recovered_cases += int(row['total_recovered'])
            else:
                pass

        return total_country, total_cases, total_deaths, total_recovered_cases


def given_country_stats(country_name):
    with open('covid_cases_stats.csv') as file_obj:
        reader_obj = csv.DictReader(file_obj)
        for row in reader_obj:
            if str(country_name != 'Total'):
                if str(country_name) == "-a " + row['country']:
                    print("-a " + row['country'])
                    getting_ratio = int(row['total_recovered']) / int(row['total_cases'])
                    print('Recovered/total ratio: ', round(getting_ratio, 2))
                    break
                else:
                    print("Country Does Not Find")
                    break
            else:
                pass


def economic_measure(economic_measure_string, total_country, total_cases, total_deaths):
    if str(economic_measure_string) == '-b Economic measures':
        getting_final_ratio = (total_deaths * 100) / total_cases
        print(f'{round(getting_final_ratio, 2)}% death average found in {total_country} countries.')
    else:
        print("Does not matched")


def safety_measure(safety_param, total_recovered_cases, total_cases):
    count_economic_measures = 0
    limit_public_gatherings = 0
    quarantine_policies = 0
    public_health_system = 0
    flight_suspension = 0

    with open('covid_safety_measures.csv') as file_obj:
        reader_obj = csv.DictReader(file_obj)
        if str(safety_param) == '-c':
            for row in reader_obj:
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
            economic_measures = count_economic_measures / calculate_efficiency
            print('Economic measures: ', int(economic_measures))
            economic_measures = limit_public_gatherings / calculate_efficiency
            print('Limit public gatherings:', int(economic_measures))
            economic_measures = limit_public_gatherings / calculate_efficiency
            print('Introduction of quarantine policies:', int(economic_measures))
            economic_measures = public_health_system / calculate_efficiency
            print('Strengthening the public health system:', int(economic_measures))
            economic_measures = flight_suspension / calculate_efficiency
            print('International flights suspension:', int(economic_measures))
        else:
            print("Does not match")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    total_country = 0
    total_deaths = 0
    total_cases = 0
    total_recovered_cases = 0
    all_stats = total_country_cases_deaths(total_country,
                                           total_cases,
                                           total_deaths,
                                           total_recovered_cases)
    total_country = all_stats[0]
    total_cases = all_stats[1]
    total_deaths = all_stats[2]
    total_recovered_cases = all_stats[3]

    # Check Country Stats by Name

    country_name = input("")
    given_country_stats(country_name)
    print("=======================End Task 1=================================")

    # Searching for Econimical Measures
    economic_measure_string = input("")
    economic_measure(economic_measure_string,
                         total_country,
                         total_cases,
                         total_deaths)
    print("=======================End Task 2=================================")

    # Calculate Safety Measures
    safety_param = input("")
    safety_measure(safety_param, total_recovered_cases, total_cases)
    print("=======================End Task 3=================================")
