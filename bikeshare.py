import time
import pandas as pd
import numpy as np
import calendar as cal

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Now Let\'s explore some interesting US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_of_choice = input("Please Select one of the cities between Chicago, New York City or Washington to begin: ").lower()

    if city_of_choice in ['chicago', 'new york city', 'washington']:
        df = pd.read_csv(CITY_DATA[city_of_choice])
#########################################################################################################
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
        start_loc = 0
        stop_loc = 5
    while (view_data == "yes"):
        print(df.iloc[start_loc:stop_loc])
        start_loc += 5
        stop_loc += 5
        ##print('Here you have the 5 rows from',city_of_choice, ':\n', df.head(5))

        view_data = input("Do you wish to continue?: ").lower()


#########################################################################################################
    while city_of_choice not in ['chicago', 'new york city', 'washington']:
        print('Not Valid. Ensure you entered a valid city name')
        city_of_choice = input("Please Select one of the cities between Chicago, New York City or Washington again: ").lower()
        overview = pd.read_csv(CITY_DATA[city_of_choice])
        print('Here you have the first 5 rows from',city_of_choice, ':\n', overview.head(5))

    # get user input for month (all, january, february, ... , june)
    month = input("Please Select the month between January and June or all to begin: ").lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        print('Not Valid. Ensure your selection is between January and June')
        month = input("Please Select the month between January to June again: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please Select one day of the week to investigate or all: ").lower()
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        print('Not Valid')
        day = input("Please Select the day of the week again: ").lower()

    print('-'*40)
    return city_of_choice, month, day

def load_data(city_of_choice, month, day):
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city_of_choice])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month day and hour of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    most_common_month_name = cal.month_name[most_common_month]

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]

    print('Most common month of travel:', most_common_month_name)
    print('Most common day of travel:', most_common_day)
    print('Most common start hour of travel:', most_common_start_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['start end station'] = df['Start Station'] + ' and ' + df['End Station']
    popular_start_end_station = df['start end station'].mode()[0]

    print('Most commonly used start station:', popular_start_station)
    print('Most commonly used end station :', popular_end_station)
    print('Most frequent combination of start station and end station trip :', popular_start_end_station)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time : ', total_travel_time, 'seconds.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean of travel time : ', mean_travel_time, 'seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_user_types = df['User Type'].value_counts()

    print('Counts of user types:\n', counts_user_types, '\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        counts_gender = df['Gender'].value_counts()
        print('Counts of gender:\n', counts_gender, '\n')
    else:
        print('There is no record in Gender')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_yob = int(df['Birth Year'].min())
        most_recent_yob = int(df['Birth Year'].max())
        most_common_yob = int(df['Birth Year'].mode())
        print('Earliest year of birth: ', earliest_yob)
        print('Most recent year of birth: ', most_recent_yob)
        print('Most common year of birth: ', most_common_yob)
    else:
        print('There is no record in Birth Year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city_of_choice, month, day = get_filters()
        df = load_data(city_of_choice, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to explore more? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
