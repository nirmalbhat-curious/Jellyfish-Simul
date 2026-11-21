import matplotlib.pyplot as plt


def plot_coverage(time_history, coverage_history,
                  detection_time_history, detection_history):

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Graph 1: Swarm Coverage
    ax1.plot(time_history, coverage_history,
             marker='o', label='Swarm Coverage')

    ax1.set_xlabel("Time (seconds)")
    ax1.set_ylabel("Ocean Coverage (%)")
    ax1.set_title("Swarm Coverage vs Time")
    ax1.set_ylim(0, 100)
    ax1.grid(True)
    ax1.legend()

    # Graph 2: Pollution Detection
    ax2.plot(detection_time_history, detection_history,
             marker='o', label='Hotspots Detected')

    ax2.set_xlabel("Time (seconds)")
    ax2.set_ylabel("Hotspots Detected")
    ax2.set_title("Pollution Detection vs Time")
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.show()