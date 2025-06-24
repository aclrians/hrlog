from datetime import datetime,timedelta
import sqlite3
import matplotlib.pyplot as plt


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
    hourlyTime = round(hourlyTime,2)
    return hourlyTime


def time_logging_db(activity,recordedTime):
    # Getting today's date
    todayDate = datetime.today().strftime('%Y-%m-%d')
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute ("CREATE TABLE IF NOT EXISTS Activity_Log(date TEXT, activity TEXT, hours REAL) ")

    # Checking to see if there is something logged in for today
    cur.execute("SELECT hours FROM Activity_Log WHERE date = ? AND activity = ?", (todayDate, activity))
    result = cur.fetchone()
    # Adding on to the existing value
    if result:
        existing_hours = result[0]
        newTotal = existing_hours + recordedTime
        cur.execute("UPDATE Activity_Log SET hours = ? WHERE date = ? AND activity = ?", (newTotal, todayDate, activity ))
        con.commit()
    # Inserting our current value for the activity
    else:
        cur.execute("INSERT INTO Activity_Log(date, activity, hours) VALUES (?,?,?)", (todayDate,activity,recordedTime))
        con.commit()

    #Closing
    con.close()
    print("Logged into database")

def pie_chart_load():
    todayDate = datetime.today().strftime('%Y-%m-%d')
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute ("SELECT activity, hours FROM Activity_Log")
    data = cur.fetchall()

    # Processing our data
    labels = [row[0] for row in data]
    sizes = [row[1] for row in data]

    # Fetching our date , this could have easily been used as todayDate but we have to think for future features
    cur.execute("SELECT date FROM Activity_Log WHERE date = ? " , (todayDate,))
    result = cur.fetchone()
    if result:
        title = result[0]

    # Creating our pie chart
    plt.pie(sizes, labels=labels, autopct = '%1.1f%%', startangle = 90)
    plt.axis('equal')
    plt.title(f'Activity Log for {title}') 
    plt.show()
    con.close()



def main():
    # Menu 
    print("Hello! Please enter which activity you'd like to enter a time for:")
    userChoice = int(input("1. Programming\n2. Working Out\n3. Working @ Job\n4. Practicing Math\n5. Show Pie Chart\n"))
    
    while userChoice not in range (1,6):
        userChoice = int(input("Please enter a valid number from 1-5:\n"))

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
    elif userChoice == 5:
        pie_chart_load()



if __name__ == "__main__":
    main()
