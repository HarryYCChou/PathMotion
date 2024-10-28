from loader import load_data
from analyzer import get_description, get_sensor_data
from simulator import simulate
from ui import start_ui

#
#   main
#       load_data->get_description->simulate->plot_result
#
def main():
    start_ui()

if __name__ == "__main__":
    main()