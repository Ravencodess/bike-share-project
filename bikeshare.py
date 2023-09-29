import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'nyc': 'new_york_city.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv',
             'washington dc': 'washington.csv',
             'washington d.c': 'washington.csv'}


def get_filters():
    """
    Gathers user input to specify a city, month, and day for data analysis.

    Returns:
        str: The name of the city to analyze.
        str or None: The name of the month to filter by or None if not specified.
        str or None: The name of the day of the week to filter by or None if not specified.

    This function interactively collects user preferences for city, month, and day filtering options.
    Users can choose to filter by month, day, both, or none to view the entire dataset.
    """
    def get_month():
        """
        Prompt the user to input a month for filtering.

        Returns:
            str: The name of the month to filter by.

        This function interacts with the user to collect a month for filtering data.
        It ensures that the input month is valid (from January to June) and returns it in title case.
        """
        while True:
            print('-'*40)
            try:
                user_month = input(
                    'Enter a Month you would like to filter by from January to June: ').strip().title()
                months = ["January", "February",
                          "March", "April", "May", "June"]
                if user_month in months:
                    month = user_month
                    return month
                else:
                    print('Please Enter a valid Month')
            except KeyboardInterrupt:
                print(' \n Closing......')
                break
        return

    def get_day():
        """
        Prompt the user to input a day of the week for filtering.

        Returns:
            str: The name of the day of the week to filter by.

        This function interacts with the user to collect a day of the week for filtering data.
        It validates the input against a list of valid day names and returns the selected day in title case.
        """
        while True:
            print('-'*40)
            try:
                user_day = input(
                    'Enter a Day you would like to filter by: ').strip().title()
                days_of_week = ["Monday", "Tuesday", "Wednesday",
                                "Thursday", "Friday", "Saturday", "Sunday", "all"]
                if user_day in days_of_week:
                    day = user_day
                    return day
                else:
                    print('Please Enter a valid Day')
            except KeyboardInterrupt:
                print(' \n Closing......')
                break
        return

    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        # get user input for city (chicago, new york city, washington)
        try:
            user_city = input(
                'Please enter the City you would like to see data from (Chicago, New york city, Washington): ').strip().lower()
            # Validate if user input exists in my Dictionary
            if user_city in CITY_DATA:
                print('-'*40)
                print(f"Loading {user_city}'s Data......")
                city = CITY_DATA[user_city]
                break
            else:
                print('We currently do not have data for this City\nKindly inidcate a city from (Chicago, New york city, Washington)\n')
        except KeyboardInterrupt:
            print(' \n Closing......')
            return

    # Get user preference on filtering criteria
    while True:
        print('-'*40)
        try:
            user_preference = input(
                'Do you want to filter by "Month", "Day" or "Both" Enter "None" if you would prefer the entire dataset: ').strip().title()
            preferences = ["Month", "Day", "Both", "None"]
            if user_preference in preferences:
                preference = user_preference
                break
            else:
                print('Please Enter a valid Preference Criteria')
        except KeyboardInterrupt:
            print(' \n Closing......')
            return

    if preference == 'Month':
        month = get_month()
        return city, month, None
    elif preference == 'Day':
        day = get_day()
        return city, None, day
    elif preference == 'Both':
        month, day = get_month(), get_day()
        return city, month, day
    else:
        return city, None, None


def load_data(city, month=None, day=None):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or defaults to None to apply no month filter
        (str) day - name of the day of week to filter by, or defaults to None to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month or day or both if applicable
    """
    df = pd.read_csv(city)

    # Convert the 'Start Time' column to a datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Access the month names using dt.month_name
    df['month'] = df['Start Time'].dt.month_name()

    # Access the weekday names using dt.day_name
    df['weekday'] = df['Start Time'].dt.day_name()

    # Access the hour integers using dt.hour
    df['hour'] = df['Start Time'].dt.hour

    if month is None and day is None:
        return df
    elif month is None:
        df = df[df['weekday'] == day]
        return df
    elif day is None:
        df = df[df['month'] == month]
        return df
    else:
        df = df[(df['weekday'] == day) & (df['month'] == month)]
        return df


def time_stats(df):
    """
    Displays statistics related to the most frequent times of travel within a given dataset.

    Args:
        df (DataFrame): A Pandas DataFrame containing city data, possibly filtered by month and day.

    Returns:
        None: This function prints statistical information based on the provided criteria.

    Note:
        This function converts 24-hour time integers to local time format (AM/PM).
    """

    def convert_to_local_time(hour_24):
        """
        Converts a 24-hour time integer to local time format (AM/PM).

        Args:
            hour_24 (int): The input hour in 24-hour format.

        Returns:
            str: The time in local time format (e.g., "1AM" or "1PM").
        """
        if 1 <= hour_24 <= 12:
            return f"{hour_24}AM"
        elif 13 <= hour_24 <= 24:
            return f"{hour_24 - 12}PM"

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()
    print(f'The most common month for travel was: {common_month[0]}')
    # display the most common day of week
    common_day = df['weekday'].mode()
    print(f'The most common day for travel was: {common_day[0]}')
    # display the most common start hour
    common_hour = df['hour'].mode()
    print(
        f'The most common hour for travel was: {convert_to_local_time(common_hour[0])}')

    print(f"\nThis took {time.time() - start_time} seconds to compute")
    print('-'*40)


def station_stats(df):
    """
    Display statistics about the most popular stations and trips within a given dataset.

    Args:
        df (DataFrame): A Pandas DataFrame containing city data, possibly filtered by month and day.

    Returns:
        None: This function prints statistical information based on the specified criteria.

    This function calculates and prints the most common starting station, the most common ending station,
    and the most frequent combination of start and end stations for trips within the provided dataset.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()
    print(f'The most common start sation was: {common_start_station[0]}')

    # display most commonly used end station
    common_end_station = df['End Station'].mode()
    print(f'The most common end station was: {common_end_station[0]}')
    print()

    # display most frequent combination of start station and end station trip
    groupby = df.groupby(['Start Station', 'End Station'])

    # Iterate through the groups and compare each group's length with the previous until we get the largest group (combination of start and end stations)
    highest_frequency = 0
    for key, group in groupby:
        if len(group) >= highest_frequency:
            highest_frequency = len(group)
            start_station, end_station = key
    print(
        f"The most frequent combination of start station and end station trip was\nStart Station: {start_station}\nEnd station: {end_station}\nWith a total of {highest_frequency} trips")
    print(f"\nThis took {time.time() - start_time} seconds to compute")
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics related to trip durations for a given dataset.

    Args:
        df (DataFrame): A Pandas DataFrame containing city data, possibly filtered by month and day.

    Returns:
        None: This function prints statistical information based on the provided criteria.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    def int_to_hms(seconds):
        """
        Converts seconds to hours, minutes, and seconds.

        Args:
            seconds (int): The input duration in seconds.

        Returns:
            tuple: A tuple containing hours, minutes, and seconds.
        """
        hours = seconds // 3600  # 3600 seconds in an hour
        remaining_minutes = seconds % 3600
        minutes = remaining_minutes // 60  # 60 seconds in a minute
        seconds = seconds % 60
        return int(hours), int(minutes), round(seconds, 2)

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    hours, minutes, seconds = int_to_hms(total_travel_time)
    print(
        f"The total travel time was {hours} Hours, {minutes} Minutes and {seconds} Seconds")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    hours, minutes, seconds = int_to_hms(mean_travel_time)
    print(
        f"The Mean travel time was {hours} Hours, {minutes} Minutes and {seconds} Seconds")

    print(f"\nThis took {time.time() - start_time} seconds to compute")
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        df (pandas.DataFrame): Pandas DataFrame containing city data.

    Returns:
        None

    This function calculates and displays the following statistics based on the provided DataFrame:
    - Counts of user types (e.g., Subscriber, Customer)
    - Counts of gender (if available in the DataFrame)
    - Earliest, most recent, and most common birth years of customers (if available in the DataFrame).

    If gender or birth year information is not available in the DataFrame, it handles the KeyError gracefully
    and informs the user accordingly.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    for type, count in user_types.items():
        print(f"{type}: {count}")
    print()

    try:
        # Display counts of gender
        gender_types = df['Gender'].value_counts()
        for gender, count in gender_types.items():
            print(f"{gender}: {count}")
        print()

    except KeyError as e:
        print(f"KeyError: info on {e} Doesn't exist ")
    try:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year, most_recent_birth_year, most_common_birth_year = df['Birth Year'].min(
        ), df['Birth Year'].max(), df['Birth Year'].mode()[0]

        print(
            f"Our oldest customer was born in: {int(earliest_birth_year)}\nOur youngest customer was born in: {int(most_recent_birth_year)}\nThe most common birthday year of our customers is: {int(most_common_birth_year)}")
    except KeyError as e:
        print(f"KeyError: info on {e} Doesn't exist ")

    print()
    print(f"\nThis took {time.time() - start_time} seconds to compute")
    print('-'*40)


def yes_no(prompt):
    """
    Prompts the user for a Yes or No response and returns the validated choice.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: Either 'Yes' or 'No' based on the user's input.
    """
    while True:
        try:
            raw_data_choice = input(prompt).strip().title()
            valid_choices = ['Yes', 'No']
            if raw_data_choice in valid_choices:
                return raw_data_choice
            else:
                print('Please enter either Yes or No')
        except KeyboardInterrupt:
            print('\n Closing......')
            return


def chunker(iterable, size):
    """
    Splits an iterable into chunks of a specified size and yields each chunk.

    Args:
        iterable (iterable): The iterable to be split into chunks.
        size (int): The size of each chunk.

    Yields:
        object: A chunk of the iterable of the specified size.
    """
    for i in range(0, len(iterable), size):
        yield iterable.iloc[i:i+5]


def raw_data(dataframe):
    """
    Displays 5 lines of raw data from a given DataFrame in chunks of 5 lines at a time.

    Args:
        dataframe (pandas.DataFrame): The DataFrame containing the raw data.

    Returns:
        None
    """
    for chunk in chunker(dataframe, 5):
        # Prompt the user to see raw data
        user_choice = yes_no(
            '\nWould you like to see 5 lines of the raw data? Enter Yes or No: ')

        if user_choice == 'No':
            break
        else:
            print(chunk)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        # Prompt the user to restart the program
        restart = yes_no('\nWould you like to restart? Enter yes or no: ')
        if restart == 'No':
            break


if __name__ == "__main__":
    main()
