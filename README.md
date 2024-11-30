# BatterySense

**BatterySense** is a lightweight, real-time battery health monitoring app that helps you track your device's battery health, charge status, and runtime. It provides an intuitive interface to check battery health trends and displays useful information to help you optimize battery performance.

## Features

- **Real-Time Battery Information:** Displays current battery percentage, charge status (plugged in or not), and remaining time.
- **Battery Health Monitoring:** Shows the current battery health and calculates the average health over time.
- **Automatic Updates:** Data refreshes every 5 seconds to provide up-to-date battery information.
- **User-Friendly Interface:** Clean and simple interface for easy tracking of battery health.
- **Average Battery Health:** Tracks battery health trends and displays the average over the last several readings.
  
## Requirements

- Python 3.x
- `psutil` library for battery information
- `wmic` command (Windows-only) for detailed battery health info

### Install dependencies

To install the necessary dependencies, use the following command:

```bash
pip install psutil
