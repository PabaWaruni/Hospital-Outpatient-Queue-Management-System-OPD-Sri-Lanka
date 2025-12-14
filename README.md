# Hospital Outpatient Queue Management System

This project analyzes and simulates a hospital's outpatient department (OPD) queueing system based on a provided dataset. It performs data analysis to uncover insights into patient flow and runs a simulation to model the impact of resource allocation (number of doctors) on patient waiting times.

## Features

*   **Data Analysis**: Calculates and visualizes key metrics from the patient dataset (`Dataset.csv`), including:
    *   Distribution of patient waiting times.
    *   Distribution of service (consultation) durations.
    *   Patient arrival patterns over time.
    *   Relationship between queue length and waiting time.
*   **Trace-Driven Simulation**: Uses the `simpy` discrete-event simulation library to model the OPD.
    *   Compares system performance with a variable number of doctors (from 3 to 6).
    *   Outputs metrics such as average wait time, average consultation time, and total time spent in the system.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/Hospital-Outpatient-Queue-Management-System-OPD-Sri-Lanka.git
    cd Hospital-Outpatient-Queue-Management-System-OPD-Sri-Lanka
    ```

2.  Install the required Python libraries:
    ```bash
    pip install pandas matplotlib simpy numpy
    ```

## Usage

To run the analysis and simulation, execute the main script:

```bash
python QueueManagementSystem.py
```

The script will first perform the data analysis and then run the queueing simulation.

## Output

*   **Console Output**:
    *   Summary statistics for waiting time, service duration, and inter-arrival times.
    *   Simulation results for different numbers of doctors, showing the average waiting time, consultation time, and total time in the system.

*   **Visualizations**:
    The script generates and saves several plots in the `visualizations/` directory:
    *   `waiting_time_histogram.png`: Distribution of patient waiting times.
    *   `service_duration_histogram.png`: Distribution of consultation durations.
    *   `arrivals_over_time.png`: Patient arrival counts in 15-minute intervals.
    *   `queue_length_vs_waiting_time.png`: Scatter plot showing the relationship between queue length and waiting time.

## Project Structure

```
.
├── Dataset.csv                   # The input data for analysis and simulation
├── QueueManagementSystem.py      # The main Python script
└── visualizations/               # Directory for output plots
    ├── arrivals_over_time.png
    ├── queue_length_vs_waiting_time.png
    ├── service_duration_histogram.png
    └── waiting_time_histogram.png
```
