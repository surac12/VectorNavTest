import serial
import time
#poopt test
# Open the serial port
try:
    ser = serial.Serial('COM3', 115200, timeout=1)
    ser.flushInput()  # Clear old data
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

def read_vn300():
    """Reads and processes ASCII data from VN-300."""
    try:
        line = ser.readline().decode('ascii', errors='ignore').strip()
        if line:
            print("Received:", line)  # Print raw message
            parse_vn300_data(line)
    except Exception as e:
        print(f"Error reading from serial: {e}")

def parse_vn300_data(line):
    """Parses VN-300 ASCII output and extracts Yaw, Pitch, Roll."""
    if line.startswith("$VNINS"):  # Only process INS data
        fields = line.split(',')
        try:
            yaw = float(fields[4])   # Yaw in degrees
            pitch = float(fields[5])  # Pitch in degrees
            roll = float(fields[6])   # Roll in degrees

            print(f"Yaw: {yaw:.2f}°, Pitch: {pitch:.2f}°, Roll: {roll:.2f}°")
        except (ValueError, IndexError):
            print("Error parsing VNINS data")

def main():
    """Continuously reads VN-300 data until interrupted."""
    try:
        print("Reading VN-300 Yaw, Pitch, Roll...")
        while True:
            read_vn300()
            time.sleep(0.1)  # Adjust delay for real-time data
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        ser.close()
        print("Serial connection closed.")

if __name__ == "__main__":
    main()