import PySimpleGUI as sg
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from psu import PSU
from sensor import  Sensor

TARGET_TEMPERATURE = 30.0

PSU_PORT = "COM2"
ARDUINO_PORT = "COM15"
TARGET_VOLTAGE = 8.0

MAX_WT = 16.0

fig, ax = plt.subplots()
ax.set_ylim([20, 45])  # Set y-axis limits

line = ax.plot([],[])[0]
xdata, ydata = [], []

def update_plot(data):
    time_point, temp = data
    xdata.append(time_point)
    ydata.append(temp)
    line.set_data(xdata[-50:], ydata[-50:])
    ax.relim()  # Recalculate limits
    ax.autoscale_view(True,True,True)  # Autoscale the view
    return line,

layout = [
    [sg.Canvas(size=(640, 480), key='canvas')],
    [sg.Button('Exit')]
]

window = sg.Window('Graph with controls', layout, finalize=True)
canvas = FigureCanvasTkAgg(fig, master=window['canvas'].TKCanvas)
canvas.draw()
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)


def run_loop():
    start_time = time.time()

    with PSU(PSU_PORT) as psu, Sensor(ARDUINO_PORT) as sensor:
        psu.set_voltage(TARGET_VOLTAGE)
        psu.set_current(0.0)
        psu.set_output(True)

        while True:
            temp = sensor.read()
            print(f'Got temperature: {temp}')

            if temp < TARGET_TEMPERATURE:
                current = MAX_WT / TARGET_VOLTAGE
                print(f'Setting wattage to {current*TARGET_VOLTAGE}')
                psu.set_current(current)

            if temp > TARGET_TEMPERATURE:
                print(f'Setting wattage to 0')
                psu.set_current(0.0)

            

            yield time.time() - start_time, temp

ani = None

def main():
    def data_gen():
        with open('data.csv', 'w') as f:
            loop = run_loop()
            while True:
                values =  next(loop)
                f.write(f'{values[0]},{values[1]}\n')
                f.flush()
                canvas.draw()
                yield values
    global ani
    # list(data_gen())
    ani = animation.FuncAnimation(fig, update_plot, data_gen, interval=1000)
    print('done')
    

    # # set
    # # bound rate: 9600
    # # parity: none
    # # data bit: 8
    # # stop bit: 1
    # # data flow control: none

    # # Create a serial object
    # ser = serial.Serial(port=serial_port_name)

    # # Set the parameters
    # ser.baudrate = baud_rate
    # ser.parity = serial.PARITY_NONE
    # ser.bytesize = serial.EIGHTBITS
    # ser.stopbits = serial.STOPBITS_ONE
    # ser.xonxoff = False  # Disable software flow control

    # # Open the serial port
    # ser.close()
    # ser.open()

    
    # try:
    #     if ser.is_open:
    #         print(f"Connected to {serial_port_name} at {baud_rate} baud.")
            
    #         # Set the voltage
    #         set_voltage(ser, target_voltage)
    #         vol = read_voltage(ser)
    #         print(vol)
            
    #         print(f"Voltage set to {target_voltage} volts.")
    #     else:
    #         print(f"Failed to open {serial_port_name}.")
    # except Exception as e:
    #     print(f"Error: {str(e)}")
    # finally:
    #     # Close the serial port connection
    #     ser.close()
    #     print("Serial port closed.")

if __name__ == "__main__":
    main()
