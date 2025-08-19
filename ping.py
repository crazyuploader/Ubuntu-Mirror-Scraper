import subprocess
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys # Import sys for OS detection

# Define the file path where the hostnames are stored
input_file = "data/mirrors/archive/servers.txt"


# Define the function to ping a hostname and get the ping time
def ping_host(hostname):
    try:
        # Determine the correct ping command based on the operating system
        if sys.platform.startswith('win'):
            ping_cmd = ["ping", "-n", "1", hostname]
        else: # Linux, macOS, etc.
            ping_cmd = ["ping", "-c", "1", hostname]

        result = subprocess.run(
            ping_cmd, # Use the determined ping command
            capture_output=True,
            text=True,
            timeout=1,  # Set the timeout to 1 second
        )
        # Extract the ping time from the output
        output = result.stdout
        # Extract the time value from the output
        if "time=" in output:
            time_str = output.split("time=")[1].split(" ms")[0]
            return hostname, float(time_str)
        else:
            return hostname, float("inf")  # Return infinity if ping fails
    except subprocess.TimeoutExpired:
        # print(f"Timeout expired for {hostname}")
        return hostname, float("inf")
    except Exception as e:
        print(f"Error pinging {hostname}: {e}")
        return hostname, float("inf")


# Main execution logic
if __name__ == "__main__":
    # Read hostnames from the input file
    with open(input_file, "r") as file:
        hostnames = [line.strip() for line in file if line.strip()]

    # Create a list to store ping results
    ping_results = []

    # Use ThreadPoolExecutor to parallelize the ping process
    # max_workers is set to 128, which can be high depending on system resources and network conditions.
    # Adjust as needed for optimal performance and to avoid resource exhaustion or rate limiting.
    with ThreadPoolExecutor(max_workers=128) as executor:
        # Create a dictionary to hold the future to hostname mapping
        future_to_hostname = {
            executor.submit(ping_host, hostname): hostname for hostname in hostnames
        }

        # Process results as they complete
        for future in as_completed(future_to_hostname):
            hostname, ping_time = future.result()
            ping_results.append({"Hostname": hostname, "Ping Time (ms)": ping_time})

    # Create a DataFrame from the ping results
    df = pd.DataFrame(ping_results)

    # Sort the DataFrame by ping time
    df_sorted = df.sort_values(by="Ping Time (ms)")

    # Print the results in a tabular format
    print(df_sorted.to_string(index=False))
