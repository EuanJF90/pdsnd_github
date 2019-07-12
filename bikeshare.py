import time

import pandas as pd

import numpy as np

from datetime import datetime



CITY_DATA = { 'chicago': 'chicago.csv',

              'new york city': 'new_york_city.csv',

              'washington': 'washington.csv' }



def get_filters():

    """

    Asks user to specify a city, month, and day to analyze.



    Returns:

    (str) city - name of the city to analyze

    (str) month - name of the month to filter by, or "all" to apply no month filter

    (str) day - name of the day of week to filter by, or "all" to apply no day filter

    """

    print('\nHello! Let\'s explore some US bikeshare data! \n')

        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:

        city = input("Which city would you like to analyse (enter one of chicago, new york city or washington)?: \n")

        if city.lower() not in ('chicago', 'new york city', 'washington'):

            print("Please select another city. \n")

        else:

            print("\nYou have selected {}".format(city.title()))

            break

            # get user input for filter by month, day or not at all

    while True:

        selection = input("\nWould you like to filter by month, day or use all data (enter month, day or all)?: \n")

        if selection.lower() not in ('month', 'day', 'all'):

            print("\nPlease choose one of the options specified in the question \n")

        else:

            break

        # get user input for month (all, january, february, ... , june)

    if selection.lower() == 'month':

        while True:

            month = input("\nWhich month would you like to analyse (enter one of the first six months of the year?: \n")

            if month.lower() not in ('january', 'february', 'march', 'april', 'may', 'june'):

                print("\nNot in first six months of the year - please select another month. \n")

            else:

                day = 'all'

                print("\nYou have selected {} ....data loading\n".format(month.title()))

                print('-'*80)

                break

        # get user input for day of week (all, monday, tuesday, ... sunday)

    elif selection.lower() == 'day':

        while True:

            day = input("\nWhich day would you like to analyse (enter one of the days of the week) ?: \n")

            if day.lower() not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):

                print("\nNot a day of the week - please select another day. \n")

            else:

                month = 'all'

                print("\nYou have selected {} ....data loading\n ".format(day.title()))

                print('-'*80)

                break

    else:

        day = 'all'

        month = 'all'

        print("\nYou have selected all data, .... data loading\n")

        print('-'*80)

    return city.lower(), month.lower(), day.lower()



print('-'*80)



def load_data(city, month, day):

    """

    Loads data for the specified city and filters by month and day if applicable.



    Args:

        (str) city - name of the city to analyze

        (str) month - name of the month to filter by, or "all" to apply no month filter

        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Returns:

        df - Pandas DataFrame containing city data filtered by month and day

    """



    usefile = pd.read_csv(CITY_DATA[city])

    df = pd.DataFrame(usefile)



    # convert the Start Time column to datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])



    # extract month and day from the Start Time column to create month and day columns, in lowercase to match user input

    df['monthfilter'] = df['Start Time'].dt.strftime('%B').str.lower()

    df['dayfilter'] = df['Start Time'].dt.strftime('%A').str.lower()

    df['hourfilter'] = df['Start Time'].dt.strftime('%H').str.lower()

# filter the dataframe using the users choice of month, day, or all

    if month == 'all' and day != 'all':

        df = df[df['dayfilter'] == day]

    elif day == 'all' and month != 'all':

        df = df[df['monthfilter'] == month]

    else:

        print(".........Statistics below for City: {}, Month: {}, Day: {} ...........".format(city.title(), month.title(), day.title()))

    return df



def time_stats(df):

    """Displays statistics on the most frequent times of travel."""



    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    # display the most common month

    popular_month = df['monthfilter'].mode()[0]

    popmonth_count = (df['monthfilter']== popular_month).sum()

    print("- The most common month to ride in within the sample you selected is {} with {} trips \n".format(popular_month.title(), popmonth_count))

    # display the most common day of week

    popular_day = df['dayfilter'].mode()[0]

    popday_count = (df['dayfilter']== popular_day).sum()

    print("- The most common day to ride in the sample you selected is {} with {} trips \n".format(popular_day.title(), popday_count))



    # display the most common start hour

    popular_hour = df['hourfilter'].mode()[0]

    pophour_count = (df['hourfilter']== popular_hour).sum()

    print("- The most common start hour within the sample you selected is {}:00 with {} trips \n".format(popular_hour, pophour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*80)



def station_stats(df):

    """Displays statistics on the most popular stations and trip."""



    print('\nCalculating The Most Popular Stations and Trip...\n')

    start_time = time.time()



    # display most commonly used start station

    popular_sstation = df['Start Station'].mode()[0]

    sstation_count = (df['Start Station']== popular_sstation).sum()

    print("- The most commonly used start station within the sample you selected is {} with {} trips \n".format(popular_sstation, sstation_count))



    # display most commonly used end station

    popular_estation = df['End Station'].mode()[0]

    estation_count = (df['End Station']== popular_estation).sum()

    print("- The most common end station within the sample you selected is {} with {} trips \n".format(popular_estation, estation_count))



    # display most frequent combination of start station and end station trip

    popular_combo = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).index[0]

    popular_combo_count = max(df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False))



    print("- The most frequent combination of start station and end station trip is {} with {} trips \n".format(popular_combo, popular_combo_count))





    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*80)



def trip_duration_stats(df):

    """Displays statistics on the total and average trip duration."""



    print('\nCalculating Trip Duration...\n')

    start_time = time.time()



# displays total travel time



    seconds = sum(df['Trip Duration'])

    seconds_in_day = 86400

    seconds_in_hour = 3600

    seconds_in_minute = 60

    days = seconds // seconds_in_day

    day_remainder = seconds % seconds_in_day

    hours = day_remainder // seconds_in_hour

    hour_remainder = day_remainder % seconds_in_hour

    minutes =  hour_remainder // seconds_in_minute

    minutes_remainder = hour_remainder % seconds_in_minute

    seconds = minutes_remainder

    print("- The total travel time for your selected sample {} days, {} hours, {} minutes, and {} seconds \n".format(days, hours, minutes, seconds))



# displays mean travel time



    mean_seconds = np.mean(df['Trip Duration'])

    mean_days = mean_seconds // seconds_in_day

    mean_day_remainder = mean_seconds % seconds_in_day

    mean_hours = mean_day_remainder // seconds_in_hour

    mean_hour_remainder = mean_day_remainder % seconds_in_hour

    mean_minutes =  mean_hour_remainder // seconds_in_minute

    mean_minutes_remainder = mean_hour_remainder % seconds_in_minute

    mean_seconds = mean_minutes_remainder

    print("- The mean travel time for your selected sample {} days, {} hours, {} minutes, and {} seconds \n".format(mean_days, mean_hours,     mean_minutes, mean_seconds))



    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*80)





    print('\nCalculating User Stats...\n')





def user_stats(df):

    """Displays statistics on bikeshare users."""

    start_time = time.time()

# Display counts of user types

    user_types = df['User Type'].value_counts()

    print("\nUser type statistics below:\n\n{} \n".format(user_types))



# Display counts of gender

    user_gender = df['Gender'].value_counts()

    print("\nGender statistics below:\n\n{} \n".format(user_gender))



# Display earliest, most recent, and most common year of birth

    current_time = datetime.now().year

    youngest = int(np.min(df['Birth Year']))

    oldest = int(np.max(df['Birth Year']))

    most_common = int(df['Birth Year'].mode()[0])

    young_difference = current_time - youngest

    old_difference = current_time - oldest

    common_difference = current_time - most_common

    print("- The earliest year of birth is {}, which means this user is {} years old. The most recent year of birth is {}, which makes this cyclist {} years old. The most common year of birth is {}, which means the average age of users is {} years old. \n".format(youngest, young_difference, oldest, old_difference, most_common, common_difference))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*80)





def raw_data_loop(df):

    """This function asks the user if they want to see the raw data, and adds 5 rows to the output each incremental time they respond yes."""

    i = 5

    while True:

        raw_data = input('\nWould you like to see the raw data? Enter yes or no. \n')

        if raw_data.lower()=='yes':

            print(df.head(i))

            i = i + 5

            continue

        elif raw_data.lower()=='no':

            break

        else:

            print("Enter either yes or no \n")



def main():

    while True:

        city, month, day = get_filters()

        df = load_data(city, month, day)

        if city != 'washington':

            time_stats(df)

            station_stats(df)

            trip_duration_stats(df)

            user_stats(df)

            raw_data_loop(df)

        else:

             time_stats(df)

             station_stats(df)

             trip_duration_stats(df)

             print("Unfortunately there is no Birth Year or Gender data for Washington, so user stats analysis is excluded. \n")

             raw_data_loop(df)



        restart = input('\nWould you like to restart? Enter yes or no?.\n')

        if restart.lower() != 'yes':

            print("\nThank you, have a lovely day :)")

            break



if __name__ == "__main__":

                main()
