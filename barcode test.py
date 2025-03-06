import datetime
import csv
import os

def main():
    save_folder = "D:/Scanner Data"
    os.makedirs(save_folder, exist_ok=True)  # Ensure folder exists

    # Format filename correctly
    filename = os.path.join(save_folder, "Scanner_Data_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".csv")
    header = ["ID", "Date"]

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write header only if file is empty
        if file.tell() == 0:
            writer.writerow(header)

        # Check the current hour
        current_hour = datetime.datetime.now().hour
        print(f"Current Hour: {current_hour}")  # Debugging info

        if current_hour > 19:
            print("It's before 7 PM. Exiting the program.")
            return  # Exit the function

        print("Ready to scan. Type 'c' to exit.")

        while True:
            idnum = input("Scan barcode: ")  # Get barcode input
            #909441982 2025/03/05 06:40:46
            # idnum=idnum[3:]
            if idnum.lower() == "c":  # Allow lowercase "c" to exit
                print("Exiting...")
                break

            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format date
            writer.writerow([idnum, date])  # Append to CSV
            print(f"✅ Saved: {idnum} at {date}")

main()



