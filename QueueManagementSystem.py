import pandas as pd
import matplotlib.pyplot as plt
import os
import simpy
import numpy as np

def perform_data_analysis():
    """
    Loads data, performs exploratory data analysis, and generates visualizations.
    """
    print("--- Starting Data Analysis ---")
    if not os.path.exists('visualizations'):
        os.makedirs('visualizations')
    df = pd.read_csv('Dataset.csv')
    df['Arrival Time'] = pd.to_datetime(df['Arrival Time'])
    df['Service Start Time'] = pd.to_datetime(df['Service Start Time'])

    print("Generating visualizations...")
    plt.figure(figsize=(10, 6))
    plt.hist(df['Waiting Time (min)'], bins=15, color='skyblue', edgecolor='black')
    plt.title('Distribution of Patient Waiting Times')
    plt.xlabel('Waiting Time (minutes)')
    plt.ylabel('Number of Patients')
    plt.grid(True)
    plt.savefig('visualizations/waiting_time_histogram.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.hist(df['Service Duration (min)'], bins=15, color='lightgreen', edgecolor='black')
    plt.title('Distribution of Service Durations')
    plt.xlabel('Service Duration (minutes)')
    plt.ylabel('Number of Patients')
    plt.grid(True)
    plt.savefig('visualizations/service_duration_histogram.png')
    plt.close()

    plt.figure(figsize=(12, 6))
    df['Arrival Time'].dt.floor('15min').value_counts().sort_index().plot(kind='bar', color='coral')
    plt.title('Patient Arrivals in 15-Minute Intervals')
    plt.xlabel('Time of Arrival')
    plt.ylabel('Number of Patients')
    plt.grid(axis='y')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('visualizations/arrivals_over_time.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.scatter(df['Queue Length'], df['Waiting Time (min)'], alpha=0.7)
    plt.title('Queue Length vs. Waiting Time')
    plt.xlabel('Queue Length at Arrival')
    plt.ylabel('Waiting Time (minutes)')
    plt.grid(True)
    plt.savefig('visualizations/queue_length_vs_waiting_time.png')
    plt.close()
    print("Visualizations saved in 'visualizations' directory.")

    print("\n--- Summary Statistics from Dataset ---")
    def print_stats(series, title):
        desc = series.describe()
        print(f"\n{title}:")
        print(f"  Count: {int(desc['count'])}")
        print(f"  Mean: {desc['mean']:.2f} mins")
        print(f"  Standard Deviation: {desc['std']:.2f} mins")
        print(f"  Minimum: {desc['min']:.2f} mins")
        print(f"  25th Percentile: {desc['25%']:.2f} mins")
        print(f"  Median (50th Percentile): {desc['50%']:.2f} mins")
        print(f"  75th Percentile: {desc['75%']:.2f} mins")
        print(f"  Maximum: {desc['max']:.2f} mins")

    print_stats(df['Waiting Time (min)'], "Waiting Time")
    print_stats(df['Service Duration (min)'], "Service Duration")
    df_sorted = df.sort_values(by='Arrival Time').reset_index()
    inter_arrival_times = (df_sorted['Arrival Time'].diff().dt.total_seconds() / 60).dropna()
    print_stats(inter_arrival_times, "Inter-Arrival Time")
    print("\n--- Data Analysis Finished ---")


def run_opd_simulation():
    """
    Runs a detailed, trace-driven simulation based on the Dataset.csv file.
    """
    print("\n--- Doctor Comparison Results (Trace-Driven Simulation) ---")

    trace_df = pd.read_csv('Dataset.csv')
    trace_df['Arrival Time'] = pd.to_datetime(trace_df['Arrival Time'])
    trace_df = trace_df.sort_values(by='Arrival Time').reset_index(drop=True)
    
    trace_df['Inter-Arrival'] = (trace_df['Arrival Time'].diff()).dt.total_seconds() / 60
    trace_df.loc[0, 'Inter-Arrival'] = (trace_df.loc[0, 'Arrival Time'] - trace_df.loc[0, 'Arrival Time'].normalize()).total_seconds() / 60


    class SimStats:
        def __init__(self):
            self.wait_times = []
            self.consultation_times = []
            self.total_system_times = []

    class OPD:
        def __init__(self, env, num_doctors):
            self.env = env
            self.doctor = simpy.Resource(env, num_doctors)

        def serve_patient(self, service_duration):
            yield self.env.timeout(service_duration)

    def patient_generator(env, opd, stats):
        for index, p_data in trace_df.iterrows():
            yield env.timeout(p_data['Inter-Arrival'])
            
            arrival_time = env.now
            service_duration = p_data['Service Duration (min)']
            env.process(patient(env, opd, arrival_time, service_duration, stats))

    def patient(env, opd, arrival_time, service_duration, stats):
        with opd.doctor.request() as request:
            yield request
            
            service_start_time = env.now
            wait_time = service_start_time - arrival_time
            stats.wait_times.append(wait_time)
            stats.consultation_times.append(service_duration)

            yield env.process(opd.serve_patient(service_duration))
            
            total_time = env.now - arrival_time
            stats.total_system_times.append(total_time)

    def run_single_simulation(num_doctors):
        stats = SimStats()
        env = simpy.Environment()
        opd = OPD(env, num_doctors)
        env.process(patient_generator(env, opd, stats))
        env.run() 

        patients_served = len(stats.wait_times)
        avg_wait = np.mean(stats.wait_times) if stats.wait_times else 0
        avg_consult = np.mean(stats.consultation_times) if stats.consultation_times else 0
        avg_total = np.mean(stats.total_system_times) if stats.total_system_times else 0

        return patients_served, avg_wait, avg_consult, avg_total

    for num_docs in range(3, 7):
        served, avg_w, avg_c, avg_t = run_single_simulation(num_docs)
        
        print(f"\nDoctors: {num_docs}")
        print(f"Patients Served: {served}")
        print(f"Average Waiting Time: {avg_w:.2f} mins")
        print(f"Average Consultation Time: {avg_c:.2f} mins")
        print(f"Average Total Time in System: {avg_t:.2f} mins")

    print("\n--- Simulation Finished ---")


if __name__ == '__main__':
    perform_data_analysis()
    run_opd_simulation()