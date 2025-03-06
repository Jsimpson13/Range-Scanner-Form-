#!/usr/bin/python3
import usb.core
import usb.util
import datetime
import csv
import os
import logging

# Set up logging
logging.basicConfig(filename='/home/cyberadmin/scanner_log.txt', level=logging.DEBUG)

def read_barcode(scanner):
    scanner.set_configuration()
    endpoint = scanner[0][(0, 0)][0]
    while True:
        try:
            data = scanner.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
            # Convert to readable format
            barcode = ''.join([chr(d) for d in data if d > 0]).strip()  # Filter and strip unwanted characters
            if barcode:
                print(f"Barcode Scanned: {barcode}")
                return barcode
        except usb.core.USBError as e:
            # Handle potential USB errors (e.g., timeout)
            if e.errno == 110:  # Timeout error
                continue
            else:
                print(f"USB Error: {e}")
                logging.error(f"USB Error: {e}")
                break


def main():
    save_folder = "/media/cyberadmin/55BC-B4F8/Scanner Data"
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
        #print(f"Current Hour: {current_hour}")  # Debugging info

        if current_hour > 19:
            print("It's after 7 PM. Exiting the program.")
            logging.info("It's after 7 PM. Exiting the program.")
            return  # Exit the function

        print("Ready to scan. Type 'c' to exit.")

        while True:
            # Find the scanner by its ID
            scanner = usb.core.find(idVendor=0x581, idProduct=0x011c)
            if scanner is None:
                print("Scanner not found!")
                logging.error("Scanner not found!")
                return
            print("Input barcode")
            idnum = read_barcode(scanner)  # Get barcode input

            if idnum.lower() == "c":  # Allow lowercase "c" to exit
                print("Exiting...")
                break

            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format date
            writer.writerow([idnum, date])  # Append to CSV
            print(f"✅ Saved: {idnum} at {date}")
            logging.info(f"Saved: {idnum} at {date}")

if __name__ == "__main__":
    main()



