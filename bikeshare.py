import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    lowercases = ['chicago', 'new york city', 'washington', 'january', 'february', 'march', 'april', 'may', 'june', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    
    city = input('Pick a city: Chicago, New York City, Washington:  ').lower()
    while city not in lowercases:
        print('Not a valid city name!')
        city = input('Try again, pick a city: Chicago, New York City, Washington:  ').lower()
        
    month = input('Pick a month from January to June, or type All to show all of them:  ').lower()
    while month not in lowercases:
        print('Not a valid month name!')
        month = input('Try again, pick a month: January, February, March, April, May, June or All:  ').lower()
        
    day = input('Pick a day of the week from Monday to Sunday, or type All to show all of them:  ').lower()
    while day not in lowercases:
        print('Not a valid day name!')
        day = input('Try again, pick a day of the week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All:  ').lower

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month     #months are numbered 
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
        
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # check if there's a month or day filter. if there is, skip most popular month and day
    if month == 'all':
        popular_month = df['month'].mode()[0]
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        print('The most common month was: ', months[(popular_month - 1)].title())
     
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print('The most common day of the week was: ', popular_day)
        

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour was: {}:00'.format(popular_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('The most common start station was was: ', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('The most common end station was was: ', popular_end)

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df ['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('The most common trip was from: ', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in hours
    total_time = df['Trip Duration'].sum()
    tt_hours = round((total_time / 360), 2)
    print('Total travel time was {} hours.'.format(tt_hours))

    # display mean travel time in hours
    mean_time = df['Trip Duration'].mean()
    mt_hours = round((mean_time / 360), 2)
    print('Mean travel time was {} hours.'.format(mt_hours))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
          
    # Display counts of user types
    ut_count = df['User Type'].value_counts()
    print('The breakdown of user types is the following:\n', ut_count, '\n')

    # check if city applies. if True, display counts of gender and stats on birth year
    if city == 'chicago' or city == 'new york city':
        gender = df['Gender'].value_counts()
        print('The breakdown of user genders is the following:\n', gender, '\n')
        
        min_byear = df['Birth Year'].min()
        max_byear = df['Birth Year'].max()
        mode_byear = df['Birth Year'].mode()
        print('The earliest user birth year is {}, the most recent is {} and the most common is {}'.format(int(min_byear), int(max_byear), int(mode_byear)))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    # ask user if they want to see 5 rows of data starting from the top. keep asking until answer is 'no' to close the loop
    
    raw_option = input("Would you like you see the first 5 rows for the data you selected? Answer 'yes' or 'no':  ").lower()
    start_loc = 0
    
    while raw_option == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        raw_option = input("Would you like to see the next 5 rows? Answer 'yes' or 'no':  ").lower()
              
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
