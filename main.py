from datetime import datetime,timedelta
import sqlite3


def time_calculation():
    startTime = input("Enter a start time for activity:\n")
    endTime = input("Enter end time for activity:\n")

    # Formatting, we want our times to be 2:00PM 
    time_format = "%I:%M%p"

    startTime = datetime.strptime(startTime,time_format)
    endTime = datetime.strptime(endTime,time_format)

    total_time = endTime - startTime

    return time_conversion(total_time)

def time_conversion(total_time):
    hourlyTime = total_time.total_seconds() / 3600
    return hourlyTime


def time_logging_db(activity,recordedTime):
    # Getting today's date
    todayDate = datetime.today().strftime('%Y-%m-%d')
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute ("CREATE TABLE IF NOT EXISTS Activity_Log(date TEXT, activity TEXT, hours REAL) ")
    # Inserting our current value for the activity
    cur.execute("INSERT INTO Activity_Log(date, activity, hours) VALUES (?,?,?)", (todayDate,activity,recordedTime))
    con.commit()

    #Closing
    con.close()
    print("Logged into database")


def main():
    # Menu 
    print("Hello! Please enter which activity you'd like to enter a time for:")
    userChoice = int(input("1. Programming\n2. Working Out\n3. Working @ Job\n4. Practicing Math\n"))
    
    while userChoice not in range (1,5):
        userChoice = int(input("Please enter a valid number from 1-4:\n"))

    if userChoice == 1:
        timeSpent = time_calculation()
        time_logging_db("Programming",timeSpent)
    elif userChoice == 2:
        timeSpent = time_calculation()
        time_logging_db("Working Out",timeSpent)
    elif userChoice == 3:
        timeSpent = time_calculation()
        time_logging_db("Working @ Job",timeSpent)
    elif userChoice == 4:
        timeSpent = time_calculation()
        time_logging_db("Practicing Math",timeSpent)



if __name__ == "__main__":
    main()
