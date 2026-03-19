# WARNING: This is a legacy code sample for testing the Archaeology Engine.
# It contains intentional bad practices and mock sensitive data.

import os

DB_PASSWORD = "admin_password_2024!"  # Mock Secret
API_TOKEN = "sk-12345abcde-secret-token" # Mock API Key

def connect_to_old_db():
    print("Connecting to database using " + DB_PASSWORD)
    # Circular dependency and obsolete library simulation
    import legacy_connector
    return legacy_connector.connect()

def processData(d): # Bad naming convention
    for i in range(len(d)): # Inefficient loop
        for j in range(len(d)): # O(n^2) complexity
            print(d[i][j])

if __name__ == "__main__":
    data = [[1,2],[3,4]]
    processData(data)