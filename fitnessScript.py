# FitnessTrackerAdvanced.py

import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from plyer import notification
from datetime import datetime

# File to store fitness data
DATA_FILE = "fitness_data.csv"
GOALS_FILE = "fitness_goals.csv"
SLEEP_FILE = "sleep_data.csv"
FOOD_FILE = "food_data.csv"
BADGES_FILE = "badges.csv"
CHALLENGES_FILE = "challenges.csv"

# Initialize files with headers if they don't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as file:
        file.write("Date,Steps,Calories Burned,Distance (km)\n")

if not os.path.exists(GOALS_FILE):
    with open(GOALS_FILE, 'w') as file:
        file.write("Steps Goal,Calories Goal,Distance Goal\n")

if not os.path.exists(SLEEP_FILE):
    with open(SLEEP_FILE, 'w') as file:
        file.write("Date,Sleep Duration (hours)\n")

if not os.path.exists(FOOD_FILE):
    with open(FOOD_FILE, 'w') as file:
        file.write("Date,Food Item,Calories Consumed\n")

if not os.path.exists(BADGES_FILE):
    with open(BADGES_FILE, 'w') as file:
        file.write("Badge Name\n")

if not os.path.exists(CHALLENGES_FILE):
    with open(CHALLENGES_FILE, 'w') as file:
        file.write("Challenge Name,Target Steps\n")

def log_fitness_data():
    """Log daily fitness data."""
    print("\n--- Log Your Fitness Data ---")
    date = input("Enter the date (YYYY-MM-DD): ")
    steps = int(input("Enter the number of steps: "))
    calories = float(input("Enter the calories burned: "))
    distance = float(input("Enter the distance covered (in km): "))

    # Append data to the CSV file
    with open(DATA_FILE, 'a') as file:
        file.write(f"{date},{steps},{calories},{distance}\n")
    print("Fitness data logged successfully!\n")

def set_fitness_goals():
    """Set fitness goals."""
    print("\n--- Set Fitness Goals ---")
    steps_goal = int(input("Enter your daily steps goal: "))
    calories_goal = float(input("Enter your daily calories burned goal: "))
    distance_goal = float(input("Enter your daily distance goal (in km): "))

    # Save goals to a file
    with open(GOALS_FILE, 'w') as file:
        file.write(f"{steps_goal},{calories_goal},{distance_goal}\n")
    print("Fitness goals set successfully!\n")

def track_progress():
    """Track progress towards fitness goals."""
    if not os.path.exists(DATA_FILE) or not os.path.exists(GOALS_FILE):
        print("No fitness data or goals found. Please log data and set goals first.")
        return

    # Load fitness data and goals
    data = pd.read_csv(DATA_FILE)
    goals = pd.read_csv(GOALS_FILE)

    # Check if DataFrames are empty
    if data.empty or goals.empty:
        print("No fitness data or goals found. Please log data and set goals first.")
        return

    # Check if the required columns exist in the DataFrames
    required_columns_data = ['Steps', 'Calories Burned', 'Distance (km)']
    required_columns_goals = ['Steps Goal', 'Calories Goal', 'Distance Goal']

    if not all(column in data.columns for column in required_columns_data):
        print("Fitness data file is missing required columns. Please check the file.")
        return

    if not all(column in goals.columns for column in required_columns_goals):
        print("Goals file is missing required columns. Please check the file.")
        return

    # Calculate progress
    try:
        latest_data = data.iloc[-1]  # Get the latest logged data
        progress = {
            "Steps": latest_data['Steps'] / goals.iloc[0]['Steps Goal'],
            "Calories Burned": latest_data['Calories Burned'] / goals.iloc[0]['Calories Goal'],
            "Distance (km)": latest_data['Distance (km)'] / goals.iloc[0]['Distance Goal']
        }

        print("\n--- Your Progress ---")
        for metric, value in progress.items():
            print(f"{metric}: {value * 100:.2f}% of goal")

    except IndexError:
        print("Error: No data found in the files. Please log data and set goals first.")
    except KeyError as e:
        print(f"Error: Missing required column in the data. {e}")

def analyze_fitness_data():
    """Analyze fitness data and generate insights."""
    if not os.path.exists(DATA_FILE):
        print("No fitness data found. Please log some data first.")
        return

    # Load fitness data
    data = pd.read_csv(DATA_FILE)

    # Check if the DataFrame is empty
    if data.empty:
        print("No fitness data found. Please log some data first.")
        return

    # Check if required columns exist
    required_columns = ['Date', 'Steps', 'Calories Burned', 'Distance (km)']
    if not all(column in data.columns for column in required_columns):
        print("Fitness data file is missing required columns. Please check the file.")
        return

    # Convert 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Remove rows with missing data
    data = data.dropna()

    # Check if there is any data left after dropping NaN values
    if data.empty:
        print("No valid fitness data found. Please log some data first.")
        return

    # Set 'Date' as the index for resampling
    data.set_index('Date', inplace=True)

    # Calculate weekly averages
    weekly_avg = data.resample('W').mean()

    # Drop weeks with all NaN values
    weekly_avg = weekly_avg.dropna(how='all')

    # Check if there is any weekly data
    if weekly_avg.empty:
        print("No weekly data found. Please log more data.")
        return

    print("\n--- Weekly Averages ---")
    print(weekly_avg)

    # Plot trends
    weekly_avg.plot(y=['Steps', 'Calories Burned', 'Distance (km)'])
    plt.title('Weekly Fitness Trends')
    plt.xlabel('Date')
    plt.ylabel('Average Value')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def create_challenge():
    """Create a fitness challenge."""
    print("\n--- Create a Fitness Challenge ---")
    challenge_name = input("Enter the challenge name: ")
    target_steps = int(input("Enter the target steps for the challenge: "))

    # Save challenge to a file
    with open(CHALLENGES_FILE, 'a') as file:
        file.write(f"{challenge_name},{target_steps}\n")
    print(f"Challenge '{challenge_name}' created successfully!\n")

def join_challenge():
    """Join a fitness challenge."""
    if not os.path.exists(CHALLENGES_FILE):
        print("No challenges found. Please create a challenge first.")
        return

    challenges = pd.read_csv(CHALLENGES_FILE)
    print("\n--- Available Challenges ---")
    print(challenges)

    challenge_name = input("Enter the challenge name you want to join: ")
    if challenge_name in challenges['Challenge Name'].values:
        print(f"You have joined the challenge '{challenge_name}'!\n")
    else:
        print("Invalid challenge name. Please try again.\n")

def send_reminder():
    """Send a reminder to log fitness data."""
    notification.notify(
        title="Fitness Reminder",
        message="Don't forget to log your fitness data today!",
        timeout=10
    )
    print("Reminder sent successfully!\n")

def export_data(format='csv'):
    """Export fitness data to a file."""
    if not os.path.exists(DATA_FILE):
        print("No fitness data found. Please log some data first.")
        return

    data = pd.read_csv(DATA_FILE)
    if format == 'csv':
        data.to_csv("fitness_export.csv", index=False)
    elif format == 'excel':
        data.to_excel("fitness_export.xlsx", index=False)
    print(f"Data exported successfully as {format}!\n")

def assign_badge(badge_name):
    """Assign a badge to the user."""
    with open(BADGES_FILE, 'a') as file:
        file.write(f"{badge_name}\n")
    print(f"Congratulations! You earned the '{badge_name}' badge!\n")

def log_sleep_data():
    """Log sleep data."""
    print("\n--- Log Sleep Data ---")
    date = input("Enter the date (YYYY-MM-DD): ")
    sleep_duration = float(input("Enter sleep duration (in hours): "))

    # Save sleep data to a file
    with open(SLEEP_FILE, 'a') as file:
        file.write(f"{date},{sleep_duration}\n")
    print("Sleep data logged successfully!\n")

def log_food_intake():
    """Log food intake."""
    print("\n--- Log Food Intake ---")
    date = input("Enter the date (YYYY-MM-DD): ")
    food_item = input("Enter food item: ")
    calories = float(input("Enter calories consumed: "))

    # Save food intake data to a file
    with open(FOOD_FILE, 'a') as file:
        file.write(f"{date},{food_item},{calories}\n")
    print("Food intake logged successfully!\n")

def main():
    """Main function to run the fitness tracker."""
    while True:
        print("\n--- Personal Fitness Tracker ---")
        print("1. Log Fitness Data")
        print("2. Set Fitness Goals")
        print("3. Track Progress")
        print("4. Analyze Fitness Data")
        print("5. Create a Fitness Challenge")
        print("6. Join a Fitness Challenge")
        print("7. Send Reminder")
        print("8. Export Data")
        print("9. Assign Badge")
        print("10. Log Sleep Data")
        print("11. Log Food Intake")
        print("12. Exit")
        choice = input("Enter your choice (1-12): ")

        if choice == '1':
            log_fitness_data()
        elif choice == '2':
            set_fitness_goals()
        elif choice == '3':
            track_progress()
        elif choice == '4':
            analyze_fitness_data()
        elif choice == '5':
            create_challenge()
        elif choice == '6':
            join_challenge()
        elif choice == '7':
            send_reminder()
        elif choice == '8':
            format = input("Enter export format (csv/excel): ").lower()
            export_data(format)
        elif choice == '9':
            badge_name = input("Enter the badge name: ")
            assign_badge(badge_name)
        elif choice == '10':
            log_sleep_data()
        elif choice == '11':
            log_food_intake()
        elif choice == '12':
            print("Exiting the Fitness Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()