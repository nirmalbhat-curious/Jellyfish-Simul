import matplotlib.pyplot as plt


def plot_coverage(time_history, coverage_history):

    plt.figure(figsize=(9, 5))

    plt.plot(
        time_history,
        coverage_history,
        marker='o',
        label='Swarm Coverage'
    )

    plt.xlabel("Time (seconds)")
    plt.ylabel("Ocean Coverage (%)")

    plt.title("Swarm Coverage vs Time")

    plt.ylim(0, 100)

    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    plt.show()