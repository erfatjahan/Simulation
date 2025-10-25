import random
import pandas as pd
from tabulate import tabulate


def get_inter_arrival(rand_iat: int) -> int:
    if rand_iat < 126:
        return 1
    elif rand_iat < 251:
        return 2
    elif rand_iat < 376:
        return 3
    elif rand_iat < 501:
        return 4
    elif rand_iat < 626:
        return 5
    elif rand_iat < 751:
        return 6
    elif rand_iat < 876:
        return 7
    elif rand_iat <= 1000:
        return 8


def get_service_time(rand_service: int) -> int:
    if rand_service < 11:
        return 1
    elif rand_service < 31:
        return 2
    elif rand_service < 61:
        return 3
    elif rand_service < 86:
        return 4
    elif rand_service < 96:
        return 5
    elif rand_service <= 100:
        return 6


def simulate_queue(num_customers: int):
    data = []
    arrival_time = 0
    last_end_time = 0

    for i in range(num_customers):
        rand_iat = random.randint(1, 1000)
        rand_service = random.randint(1, 100)

        if i == 0:
            inter_arrival = 0
            arrival_time = 0
            rand_iat = 0
        else:
            inter_arrival = get_inter_arrival(rand_iat)
            arrival_time += inter_arrival

        service_time = get_service_time(rand_service)
        start_service = max(arrival_time, last_end_time)
        waiting_time = start_service - arrival_time
        idle_time = max(0, arrival_time - last_end_time)
        end_service = start_service + service_time
        time_in_system = waiting_time + service_time

        data.append({
            'Customer ID': i + 1,
            'Random No (IAT)': rand_iat,
            'Inter-Arrival Time': inter_arrival,
            'Arrival Time': arrival_time,
            'Random No (Service)': rand_service,
            'Service Time': service_time,
            'Time Service Begins': start_service,
            'Waiting Time': waiting_time,
            'Time Service Ends': end_service,
            'Time Spent in System': time_in_system,
            'Idle Time of Server': idle_time
        })
        last_end_time = end_service
    return pd.DataFrame(data)
def performance_summary(df: pd.DataFrame):
    total_customers = len(df)
    total_service = df['Service Time'].sum()
    total_idle = df['Idle Time of Server'].sum()
    total_time = df['Time Service Ends'].iloc[-1]

    avg_service = df['Service Time'].mean()
    avg_wait_all = df['Waiting Time'].mean()
    waiting_customers = df[df['Waiting Time'] > 0]
    avg_wait_for_waiting = waiting_customers['Waiting Time'].mean() if not waiting_customers.empty else 0
    avg_system = df['Time Spent in System'].mean()
    avg_time_between_arrival = df['Inter-Arrival Time'][1:].mean() if total_customers > 1 else 0

    prob_wait = (len(waiting_customers) / total_customers) * 100
    prob_idle = (total_idle / total_time) * 100

    print("\nPerformance Summary:")
    print(f"Probability that a customer has to wait: {prob_wait:.2f}%")
    print(f"Probability of idle time (server idle): {prob_idle:.2f}%")
    print(f"Average time between arrivals: {avg_time_between_arrival:.2f} mins")
    print(f"Average waiting time (for those who wait): {avg_wait_for_waiting:.2f} mins")
    print(f"Average waiting time (all customers): {avg_wait_all:.2f} mins")
    print(f"Average service time: {avg_service:.2f} mins")
    print(f"Average time customer spent in system: {avg_system:.2f} mins")
    print(f"Total Service Time : {total_service:.2f} mins")
    print(f"Total Idle Time of Server : {total_idle:.2f} mins")
    print(f"Total Simulation Time : {total_time:.2f} mins")


def main():
    num_customers = int(input("Enter number of customers: "))
    df = simulate_queue(num_customers)
    print("\nSimulation Table:")
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))

    performance_summary(df)


if __name__ == "__main__":
    main()
