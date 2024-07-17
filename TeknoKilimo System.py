import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import smtplib
from email.mime.text import MIMEText

# Sample data for rabbit management
data = {
    'rabbit_id': [1, 2, 3, 4, 5],
    'age_months': [10, 5, 3, 8, 2],
    'weight_kg': [2.5, 2.0, 1.8, 2.2, 1.5],
    'health_status': ['healthy', 'sick', 'healthy', 'healthy', 'sick'],
    'feeding_schedule': ['08:00, 16:00', '08:00, 16:00', '09:00, 17:00', '08:00, 16:00', '09:00, 17:00'],
    'breeding_cycle_days': [30, 30, 45, 30, 45]
}

df = pd.DataFrame(data)

# Data preprocessing
df['is_sick'] = df['health_status'].apply(lambda x: 1 if x == 'sick' else 0)

# Splitting the data
X = df[['age_months', 'weight_kg', 'breeding_cycle_days']]
y = df['is_sick']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training a simple classifier
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Evaluating the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Function to send email notifications
def send_email_notification(subject, body, to_email):
    from_email = "your_email@example.com"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(from_email, 'your_password')
        server.sendmail(from_email, to_email, msg.as_string())

# Sample notification
send_email_notification(
    subject="Rabbit Health Alert",
    body="Rabbit ID 2 is showing signs of sickness. Please check immediately.",
    to_email="farmer@example.com"
)

# Simple command-line interface
def main():
    while True:
        print("Sungura Bora Rabbit Management System")
        print("1. View Rabbit Data")
        print("2. Add Rabbit Data")
        print("3. Send Health Alert")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print(df)
        elif choice == '2':
            rabbit_id = int(input("Enter Rabbit ID: "))
            age = int(input("Enter Age (months): "))
            weight = float(input("Enter Weight (kg): "))
            health_status = input("Enter Health Status (healthy/sick): ")
            feeding_schedule = input("Enter Feeding Schedule (e.g., '08:00, 16:00'): ")
            breeding_cycle = int(input("Enter Breeding Cycle (days): "))
            
            new_data = {
                'rabbit_id': rabbit_id,
                'age_months': age,
                'weight_kg': weight,
                'health_status': health_status,
                'feeding_schedule': feeding_schedule,
                'breeding_cycle_days': breeding_cycle
            }
            df.loc[len(df)] = new_data
            print("Data added successfully!")
        elif choice == '3':
            rabbit_id = int(input("Enter Rabbit ID to send alert for: "))
            rabbit_data = df[df['rabbit_id'] == rabbit_id]
            if not rabbit_data.empty:
                send_email_notification(
                    subject="Rabbit Health Alert",
                    body=f"Rabbit ID {rabbit_id} is showing signs of sickness. Please check immediately.",
                    to_email="farmer@example.com"
                )
                print("Alert sent successfully!")
            else:
                print("Rabbit ID not found!")
        elif choice == '4':
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
