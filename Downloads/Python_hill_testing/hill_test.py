## -*- coding: utf-8 -*-
#4 success
#5
#code
'''import serial
import time

# Initialize the serial connection (adjust parameters as needed)
ser = serial.Serial(
    port='COM13',       # Replace with your UART port (e.g., /dev/ttyUSB0 on Linux)
    baudrate=115200,     # Set the baudrate to match your Simulink configuration
    timeout=1          # Timeout in seconds
)

# Function to send integer data to the UART
def send_integer_data(data):
    if isinstance(data, int):
        ser.write(data.to_bytes(4, byteorder='little', signed=True))  # Convert integer to bytes and write to UART
    else:
        raise ValueError("Data must be an integer")

try:
    integer_data = 101 # Example integer data to be sent

    if integer_data < 0:
        send_integer_data(integer_data)
        print(f"Sent negative integer: {integer_data}")
    elif integer_data ==0:
        send_integer_data(integer_data)
        print(f"Sent zero: {integer_data}")
    elif integer_data > 0:
        send_integer_data(integer_data)
        print(f"Sent positive integer: {integer_data}")
    else:
        print("No valid integer data to send.")

except KeyboardInterrupt:
    print("Terminating the program...")

finally:
    ser.close()  # Close the serial connection
'''


	
	
	
	
	





'''
import serial
import time

# Initialize the serial connection (adjust parameters as needed)
ser = serial.Serial(
    port='COM13',       # Replace with your UART port (e.g., /dev/ttyUSB0 on Linux)
    baudrate=115200,     # Set the baudrate to match your Simulink configuration
    timeout=1          # Timeout in seconds
)

# Function to send integer data to the UART
def send_integer_data(data):
    if isinstance(data, int):
        ser.write(data.to_bytes(4, byteorder='little', signed=True))  # Convert integer to bytes and write to UART
    else:
        raise ValueError("Data must be an integer")

try:
    integer_data = 101  # Example integer data to be sent

    if integer_data == 1:
        send_integer_data(integer_data)
        print("Sent positive response.")
   
    else:
        send_integer_data(integer_data)
        print("Sent other response.")

except KeyboardInterrupt:
    print("Terminating the program...")

finally:
    ser.close()  # Close the serial connection
	
	'''
	
	
	



'''
import time
import serial  # For COM port communication
import chardet

class HILSimulator:
    def __init__(self, com_port, baudrate=115200, timeout=1):
        """
        Initialize the HIL simulator communication over the specified COM port.
        :param com_port: COM port name (e.g., 'COM1', '/dev/ttyUSB0')
        :param baudrate: Communication baud rate (default: 115200)
        :param timeout: Read timeout in seconds (default: 1)
        """
        self.com_port = com_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.input_signal_map = self._generate_input_signal_map()
        self.output_signal_map = self._generate_output_signal_map()

    def connect(self):
        """
        Establish a connection to the HIL simulator via the COM port.
        """
        try:
            self.serial_conn = serial.Serial(
                self.com_port, baudrate=self.baudrate, timeout=self.timeout
            )
            print(f"Connected to HIL simulator on {self.com_port}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.com_port}: {e}")

    def disconnect(self):
        """
        Disconnect from the HIL simulator.
        """
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Disconnected from HIL simulator.")

    def send_command(self, command):
        """
        Send a command to the HIL simulator.
        :param command: Command string to send
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(command.encode('ISO-8859-1') + b'\n')
        time.sleep(0.1)

    def read_response(self):
        """
        Read a response from the HIL simulator.
        :return: Response string
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        response = self.serial_conn.readline()
        detected_encoding = chardet.detect(response)['encoding']
        if not detected_encoding:
            detected_encoding = 'utf-8'  # Default to UTF-8 if detection fails
        print(f"Detected encoding: {detected_encoding}")
        return response.decode(detected_encoding).strip()

    def set_input_signal(self, signal_name, value):
        """
        Set an input signal value in the HIL simulator.
        :param signal_name: Name of the input signal to set
        :param value: Value to set for the input signal
        """
        if signal_name not in self.input_signal_map:
            raise ValueError(f"Unknown input signal name: {signal_name}")
        signal_id = self.input_signal_map[signal_name]
        self.send_integer_data(signal_id)
        self.send_integer_data(value)
        print(f"Set input signal '{signal_name}' (ID: {signal_id}) to value: {value}")

    def get_output_signal(self, signal_name):
        """
        Get an output signal value from the HIL simulator.
        :param signal_name: Name of the output signal to retrieve
        :return: Signal value
        """
        if signal_name not in self.output_signal_map:
            raise ValueError(f"Unknown output signal name: {signal_name}")
        signal_id = self.output_signal_map[signal_name]
        self.send_integer_data(signal_id)
        response = self.read_response()
        print(f"Retrieved output signal '{signal_name}' (ID: {signal_id}): {response}")
        return response

    def send_integer_data(self, data):
        """
        Send integer data to the HIL simulator.
        :param data: Integer data to send
        """
        if not isinstance(data, int):
            raise ValueError("Data must be an integer")
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(data.to_bytes(4, byteorder='little', signed=True))
        print(f"Sent integer data: {data}")

    def _generate_input_signal_map(self):
        """
        Generate a mapping of input signal names to signal IDs from the HIL model.
        Replace or expand this dictionary with actual input signal names and IDs.
        """
        return {
            "Set_Low_Beam": 101,
        }

    def _generate_output_signal_map(self):
        """
        Generate a mapping of output signal names to signal IDs from the HIL model.
        Replace or expand this dictionary with actual output signal names and IDs.
        """
        return {
            "Low_Beam_Status": 201,
        }

# Example usage
if __name__ == "__main__":
    hil = HILSimulator(com_port="COM13")
    try:
        hil.connect()

        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_Low_Beam", 1)  # Turn on Low Beam
        response = hil.get_output_signal("Low_Beam_Status")
        print(f"Low Beam Status: {response}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        hil.disconnect()

'''
'''
import time
import serial  # For COM port communication
import chardet

class HILSimulator:
    def __init__(self, com_port, baudrate=115200, timeout=1):
        """
        Initialize the HIL simulator communication over the specified COM port.
        :param com_port: COM port name (e.g., 'COM1', '/dev/ttyUSB0')
        :param baudrate: Communication baud rate (default: 115200)
        :param timeout: Read timeout in seconds (default: 1)
        """
        self.com_port = com_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.input_signal_map = self._generate_input_signal_map()
        self.output_signal_map = self._generate_output_signal_map()

    def connect(self):
        """
        Establish a connection to the HIL simulator via the COM port.
        """
        try:
            self.serial_conn = serial.Serial(
                self.com_port, baudrate=self.baudrate, timeout=self.timeout
            )
            print(f"Connected to HIL simulator on {self.com_port}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.com_port}: {e}")

    def disconnect(self):
        """
        Disconnect from the HIL simulator.
        """
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Disconnected from HIL simulator.")

    def send_command(self, command):
        """
        Send a command to the HIL simulator.
        :param command: Command string to send
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(command.encode('ISO-8859-1') + b'\n')
        time.sleep(0.1)

    def read_response(self):
        """
        Read a response from the HIL simulator.
        :return: Response string
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        response = self.serial_conn.readline()
        detected_encoding = chardet.detect(response)['encoding']
        if not detected_encoding:
            detected_encoding = 'utf-8'  # Default to UTF-8 if detection fails
        print(f"Detected encoding: {detected_encoding}")
        return response.decode(detected_encoding).strip()

    def set_input_signal(self, signal_name, value):
        """
        Set an input signal value in the HIL simulator.
        :param signal_name: Name of the input signal to set
        :param value: Value to set for the input signal
        """
        if signal_name not in self.input_signal_map:
            raise ValueError(f"Unknown input signal name: {signal_name}")
        if value == 1:
            signal_id = self.input_signal_map[signal_name]
            self.send_integer_data(signal_id)
            self.send_integer_data(value)
            print(f"Set input signal '{signal_name}' (ID: {signal_id}) to value: {value}")
        else:
            print(f"Input signal '{signal_name}' is set to 0, no command sent.")

    def get_output_signal(self, signal_name):
        """
        Get an output signal value from the HIL simulator.
        :param signal_name: Name of the output signal to retrieve
        :return: Signal value
        """
        if signal_name not in self.output_signal_map:
            raise ValueError(f"Unknown output signal name: {signal_name}")
        signal_id = self.output_signal_map[signal_name]
        self.send_integer_data(signal_id)
        response = self.read_response()
        print(f"Retrieved output signal '{signal_name}' (ID: {signal_id}): {response}")
        return response

    def send_integer_data(self, data):
        """
        Send integer data to the HIL simulator.
        :param data: Integer data to send
        """
        if not isinstance(data, int):
            raise ValueError("Data must be an integer")
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(data.to_bytes(4, byteorder='little', signed=True))
        print(f"Sent integer data: {data}")

    def _generate_input_signal_map(self):
        """
        Generate a mapping of input signal names to signal IDs from the HIL model.
        Replace or expand this dictionary with actual input signal names and IDs.
        """
        return {
            "Set_Low_Beam": 101,
        }

    def _generate_output_signal_map(self):
        """
        Generate a mapping of output signal names to signal IDs from the HIL model.
        Replace or expand this dictionary with actual output signal names and IDs.
        """
        return {
            "Low_Beam_Status": 
			111,
        }

# Example usage
if __name__ == "__main__":
    hil = HILSimulator(com_port="COM13")
    try:
        hil.connect()

        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_Low_Beam", 0)  # Turn on Low Beam
        response = hil.get_output_signal("Low_Beam_Status")
        print(f"Low Beam Status: {response}")

        # Example: Attempt to set Low Beam to 0 (no command should be sent)
         #hil.set_input_signal("Set_Low_Beam", 1)  # Turn off Low Beam (no command should be sent)

    except Exception as e:
        print(f"Error: {e}")
    finally:
       hil.disconnect()
'''







'''
import time
import serial  # For COM port communication
import chardet

class HILSimulator:
    def __init__(self, com_port, baudrate=115200, timeout=1):
        """
        Initialize the HIL simulator communication over the specified COM port.
        :param com_port: COM port name (e.g., 'COM1', '/dev/ttyUSB0')
        :param baudrate: Communication baud rate (default: 115200)
        :param timeout: Read timeout in seconds (default: 1)
        """
        self.com_port = com_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.input_signal_map = self._generate_input_signal_map()
        self.output_signal_map = self._generate_output_signal_map()

    def connect(self):
        """
        Establish a connection to the HIL simulator via the COM port.
        """
        try:
            self.serial_conn = serial.Serial(
                self.com_port, baudrate=self.baudrate, timeout=self.timeout
            )
            print(f"Connected to HIL simulator on {self.com_port}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.com_port}: {e}")

    def disconnect(self):
        """
        Disconnect from the HIL simulator.
        """
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Disconnected from HIL simulator.")

    def send_command(self, command):
        """
        Send a command to the HIL simulator.
        :param command: Command string to send
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(command.encode('ISO-8859-1') + b'\n')
        time.sleep(0.1)

    def read_response(self):
        """
        Read a response from the HIL simulator.
        :return: Response string
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        response = self.serial_conn.readline()
        detected_encoding = chardet.detect(response)['encoding']
        if not detected_encoding:
            detected_encoding = 'utf-8'  # Default to UTF-8 if detection fails
		#if detected_encoding == "ascii":
		#	detected_encoding = 'utf-8'  # Default to UTF-8 if detection fails
        print(f"Detected encoding: {detected_encoding}")
        return response.decode(detected_encoding).strip()

    def receive_data(self, num_bytes):
        """
        Receive raw data from the HIL simulator.
        :param num_bytes: Number of bytes to read
        :return: Raw data bytes
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        data = self.serial_conn.read(num_bytes)
        return data

    def set_input_signal(self, signal_name, value):
        """
        Set an input signal value in the HIL simulator.
        :param signal_name: Name of the input signal to set
        :param value: Value to set for the input signal
        """
        if signal_name not in self.input_signal_map:
            raise ValueError(f"Unknown input signal name: {signal_name}")
        if value == 1:
            signal_id = self.input_signal_map[signal_name]
            self.send_integer_data(signal_id)
            self.send_integer_data(value)
            print(f"Set input signal '{signal_name}' (ID: {signal_id}) to value: {value}")
        else:
            print(f"Input signal '{signal_name}' is set to 0, no command sent.")

    def get_output_signal(self, signal_name):
        """
        Get an output signal value from the HIL simulator.
        :param signal_name: Name of the output signal to retrieve
        :return: Signal value
        """
        if signal_name not in self.output_signal_map:
            raise ValueError(f"Unknown output signal name: {signal_name}")
        signal_id = self.output_signal_map[signal_name]
        self.send_integer_data(signal_id)
        response = self.read_response()
        print(f"Retrieved output signal '{signal_name}' (ID: {signal_id}): {response}")
        return response

    def send_integer_data(self, data):
        """
        Send integer data to the HIL simulator.
        :param data: Integer data to send
        """
        if not isinstance(data, int):
            raise ValueError("Data must be an integer")
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(data.to_bytes(4, byteorder='little', signed=True))
        print(f"Sent integer data: {data}")

    def _generate_input_signal_map(self):
        """
        Generate a mapping of input signal names to signal IDs from the HIL model.
        Replace or expand this dictionary with actual input signal names and IDs.
        """
        return {
            "Set_Low_Beam": 101,
        }

    def _generate_output_signal_map(self):
        """
        Generate a mapping of output signal names to signal IDs from the HIL model.
        Replace or expand this dictionary with actual output signal names and IDs.
        """
        return {
            "Dir_Ind_Li_inp": 
            111,
			#"Hz_Li_Inp": 
          # 111,
        }

# Example usage
if __name__ == "__main__":
    hil = HILSimulator(com_port="COM13")
    try:
        hil.connect()

        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_Low_Beam", 1)  # Turn on Low Beam
        response = hil.get_output_signal("Dir_Ind_Li_inp")
        print(f"Dir_Ind_Li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received diretion inp sts: {raw_data}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
       hil.disconnect()
'''
		
		
	


'''import time
import serial  # For COM port communication
import chardet

class HILSimulator:
    def __init__(self, com_port, baudrate=115200, timeout=1):
        """
        Initialize the HIL simulator communication over the specified COM port.
        :param com_port: COM port name (e.g., 'COM1', '/dev/ttyUSB0')
        :param baudrate: Communication baud rate (default: 115200)
        :param timeout: Read timeout in seconds (default: 1)
        """
        self.com_port = com_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.input_signal_map = self._generate_input_signal_map()
        self.output_signal_map = self._generate_output_signal_map()

    def connect(self):
        """
        Establish a connection to the HIL simulator via the COM port.
        """
        try:
            self.serial_conn = serial.Serial(
                self.com_port, baudrate=self.baudrate, timeout=self.timeout
            )
            print(f"Connected to HIL simulator on {self.com_port}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.com_port}: {e}")

    def disconnect(self):
        """
        Disconnect from the HIL simulator.
        """
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Disconnected from HIL simulator.")

    def send_command(self, command):
        """
        Send a command to the HIL simulator.
        :param command: Command string to send
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(command.encode('ISO-8859-1') + b'\n')
        time.sleep(0.1)

    def read_response(self):
        """
        Read a response from the HIL simulator.
        :return: Response string
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        response = self.serial_conn.readline()
        detected_encoding = chardet.detect(response)['encoding']
        if not detected_encoding or detected_encoding.lower() == 'ascii':
            detected_encoding = 'utf-8'  # Force to UTF-8 if detection fails or is ASCII
        print(f"Detected encoding: {detected_encoding}")
        return response.decode(detected_encoding).strip()

    def receive_data(self, num_bytes):
        """
        Receive raw data from the HIL simulator.
        :param num_bytes: Number of bytes to read
        :return: Raw data bytes
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        data = self.serial_conn.read(num_bytes)
        return data

    def set_input_signal(self, signal_name, value):
        """
        Set an input signal value in the HIL simulator.
        :param signal_name: Name of the input signal to set
        :param value: Value to set for the input signal
        """
        if signal_name not in self.input_signal_map:
            raise ValueError(f"Unknown input signal name: {signal_name}")
        if value == 1:
            signal_id = self.input_signal_map[signal_name]
            self.send_integer_data(signal_id)
            self.send_integer_data(value)
            print(f"Set input signal '{signal_name}' (ID: {signal_id}) to value: {value}")
        else:
            print(f"Input signal '{signal_name}' is set to 0, no command sent.")

    def get_output_signal(self, signal_name):
        """
        Get an output signal value from the HIL simulator.
        :param signal_name: Name of the output signal to retrieve
        :return: Signal value
        """
        if signal_name not in self.output_signal_map:
            raise ValueError(f"Unknown output signal name: {signal_name}")
        signal_id = self.output_signal_map[signal_name]
        self.send_integer_data(signal_id)
        response = self.read_response()
        print(f"Retrieved output signal '{signal_name}' (ID: {signal_id}): {response}")
        return response

    def send_integer_data(self, data):
        """
        Send integer data to the HIL simulator.
        :param data: Integer data to send
        """
        if not isinstance(data, int):
            raise ValueError("Data must be an integer")
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(data.to_bytes(4, byteorder='little', signed=True))
        print(f"Sent integer data: {data}")

    def _generate_input_signal_map(self):
        """
        Generate a mapping of input signal names to signal IDs from the HIL model.
        Replace or expand this dictionary with actual input signal names and IDs.
        """
        return {
            "Set_Low_Beam": 101,
        }

    def _generate_output_signal_map(self):
        """
        Generate a mapping of output signal names to signal IDs from the HIL model.
        Replace or expand this dictionary with actual output signal names and IDs.
        """
        return {
            "Dir_Ind_Li_inp": 
            111,
        }

# Example usage
if __name__ == "__main__":
    hil = HILSimulator(com_port="COM13")
    try:
        hil.connect()

        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_Low_Beam", 1)  # Turn on Low Beam
        response = hil.get_output_signal("Dir_Ind_Li_inp")
        print(f"Dir_Ind_Li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received diretion inp sts: {raw_data}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
       hil.disconnect()'''





'''
import time
import serial  # For COM port communication
import chardet

class HILSimulator:
    def __init__(self, com_port, baudrate=115200, timeout=1):
        """
        Initialize the HIL simulator communication over the specified COM port.
        :param com_port: COM port name (e.g., 'COM1', '/dev/ttyUSB0')
        :param baudrate: Communication baud rate (default: 115200)
        :param timeout: Read timeout in seconds (default: 1)
        """
        self.com_port = com_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.input_signal_map = self._generate_input_signal_map()
        self.output_signal_map = self._generate_output_signal_map()

    def connect(self):
        """
        Establish a connection to the HIL simulator via the COM port.
        """
        try:
            self.serial_conn = serial.Serial(
                self.com_port, baudrate=self.baudrate, timeout=self.timeout
            )
            print(f"Connected to HIL simulator on {self.com_port}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.com_port}: {e}")

    def disconnect(self):
        """
        Disconnect from the HIL simulator.
        """
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Disconnected from HIL simulator.")

    def send_command(self, command):
        """
        Send a command to the HIL simulator.
        :param command: Command string to send
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(command.encode('ISO-8859-1') + b'\n')
        time.sleep(0.1)

    def read_response(self):
        """
        Read a response from the HIL simulator.
        :return: Response string in hexadecimal format
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        response = self.serial_conn.readline()
        detected_encoding = chardet.detect(response)['encoding']
        if not detected_encoding or detected_encoding.lower() == 'ascii':
            detected_encoding = 'utf-8'  # Force to UTF-8 if detection fails or is ASCII
        print(f"Detected encoding: {detected_encoding}")
        hex_response = response.hex()  # Convert to hexadecimal
        return hex_response

    def receive_data(self, num_bytes):
        """
        Receive raw data from the HIL simulator.
        :param num_bytes: Number of bytes to read
        :return: Raw data bytes in hexadecimal format
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        data = self.serial_conn.read(num_bytes)
        hex_data = data.hex()  # Convert to hexadecimal
        return hex_data

    def set_input_signal(self, signal_name, value):
        """
        Set an input signal value in the HIL simulator.
        :param signal_name: Name of the input signal to set
        :param value: Value to set for the input signal
        """
        if signal_name not in self.input_signal_map:
            raise ValueError(f"Unknown input signal name: {signal_name}")
        if value == 1:
            signal_id = self.input_signal_map[signal_name]
            self.send_integer_data(signal_id)
            self.send_integer_data(value)
            print(f"Set input signal '{signal_name}' (ID: {signal_id}) to value: {value}")
        else:
            print(f"Input signal '{signal_name}' is set to 0, no command sent.")

    def get_output_signal(self, signal_name):
        """
        Get an output signal value from the HIL simulator.
        :param signal_name: Name of the output signal to retrieve
        :return: Signal value in hexadecimal format
        """
        if signal_name not in self.output_signal_map:
            raise ValueError(f"Unknown output signal name: {signal_name}")
        signal_id = self.output_signal_map[signal_name]
        self.send_integer_data(signal_id)
        response = self.read_response()
        print(f"Retrieved output signal '{signal_name}' (ID: {signal_id}): {response}")
        return response

    def send_integer_data(self, data):
        """
        Send integer data to the HIL simulator.
        :param data: Integer data to send
        """
        if not isinstance(data, int):
            raise ValueError("Data must be an integer")
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(data.to_bytes(4, byteorder='little', signed=True))
        print(f"Sent integer data: {data}")

    def _generate_input_signal_map(self):
        """
        Generate a mapping of input signal names to signal IDs from the HIL model.
        Replace or expand this dictionary with actual input signal names and IDs.
        """
        return {
            "Set_left_direction": 101,
			"Set_right_direction": 102,
			"Set_Hazard_indicator": 103,
			"Set_Position_light": 105,
			"Set_Low_beam_light": 106,
			"Set_High_beam_light": 107,
			"Set_Position+left_turn": 108,
			"Set_Position+right_turn": 109,
        }

    def _generate_output_signal_map(self):
        """
        Generate a mapping of output signal names to signal IDs from the HIL model.
        Replace or expand this dictionary with actual output signal names and IDs.
        """
        return {
            "Dir_Ind_Li_inp": 111,
			"Hz_Li_Inp": 111,
			"Head_li_inp":111,
        }

# Example usage
if __name__ == "__main__":
    hil = HILSimulator(com_port="COM13")
    try:
        hil.connect()

        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_left_direction",1)  # Turn on Low Beam
        response = hil.get_output_signal("Dir_Ind_Li_inp")
        print(f"Dir_Ind_Li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received direction inp sts: {raw_data}")
		# Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_right_direction", 0)  # Turn on Low Beam
        response = hil.get_output_signal("Dir_Ind_Li_inp")
        print(f"Dir_Ind_Li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received direction inp sts: {raw_data}")
		# Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_Hazard_indicator", 0)  # Turn on hazard Beam
        response = hil.get_output_signal("Hz_Li_Inp")
        print(f"Hz_Li_Inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received Hazard inp sts: {raw_data}")
		# Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_Position_light", 0)  # Turn on position Beam
        response = hil.get_output_signal("Head_li_inp")
        print(f"Head_li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received position light inp sts: {raw_data}")
		# Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_Low_beam_light", 1)  # Turn on Low Beam
        response = hil.get_output_signal("Head_li_inp")
        print(f"Head_li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received low beam inp sts: {raw_data}")
		# Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_High_beam_light", 0)  # Turn on high Beam
        response = hil.get_output_signal("Head_li_inp")
        print(f"Head_li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received high beam inp sts: {raw_data}")
		

    except Exception as e:
        print(f"Error: {e}")
    finally:
       hil.disconnect() '''
	   
	   
	   
	



'''import time
import serial  # For COM port communication
import chardet

class HILSimulator:
    def __init__(self, com_port, baudrate=115200, timeout=1):
        self.com_port = com_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.input_signal_map = self._generate_input_signal_map()
        self.output_signal_map = self._generate_output_signal_map()
        self.active_signals = {}
        self.blink_flags = {}

    def connect(self):
        try:
            self.serial_conn = serial.Serial(self.com_port, baudrate=self.baudrate, timeout=self.timeout)
            print(f"Connected to HIL simulator on {self.com_port}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.com_port}: {e}")

    def disconnect(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Disconnected from HIL simulator.")

    def send_command(self, command):
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(command.encode('ISO-8859-1') + b'\n')
        time.sleep(0.1)

    def read_response(self):
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        response = self.serial_conn.readline()
        detected_encoding = chardet.detect(response)['encoding']
        if not detected_encoding or detected_encoding.lower() == 'ascii':
            detected_encoding = 'utf-8'
        print(f"Detected encoding: {detected_encoding}")
        hex_response = response.hex()
        return hex_response

    def receive_data(self, num_bytes):
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        data = self.serial_conn.read(num_bytes)
		hex_data = data.hex()
		hex_data=data.int()
        return hex_data

    def set_input_signal(self, signal_name, value, duration=1):
        if signal_name not in self.input_signal_map:
            raise ValueError(f"Unknown input signal name: {signal_name}")
        signal_id = self.input_signal_map[signal_name]
        self.active_signals[signal_name] = value

        if value == 1:
            self.send_integer_data(signal_id)
            self.send_integer_data(value)
            self.blink_flags[signal_name] = True
            print(f"Set input signal '{signal_name}' (ID: {signal_id}) to value: {value}")
            
            # Send the signal for the specified duration
            end_time = time.time() + duration
            while time.time() < end_time:
                self.send_integer_data(signal_id)
                self.send_integer_data(value)
                time.sleep(1)  # Adjust this sleep time if needed

            # Reset the signal after the duration
            self.send_integer_data(signal_id)
            self.send_integer_data(0)
            self.blink_flags[signal_name] = False
            print(f"Reset input signal '{signal_name}' (ID: {signal_id}) after {duration} seconds")
        else:
            print(f"Input signal '{signal_name}' is set to 0, no command sent.")

    def maintain_signals(self):
        while True:
            for signal_name, value in self.active_signals.items():
                if value == 1 and self.blink_flags.get(signal_name, False):
                    signal_id = self.input_signal_map[signal_name]
                    self.send_integer_data(signal_id)
                    self.send_integer_data(1)
                    print(f"Blinking input signal '{signal_name}' (ID: {signal_id}) - ON")
                    time.sleep(0.5)
                    self.send_integer_data(signal_id)
                    self.send_integer_data(0)
                    print(f"Blinking input signal '{signal_name}' (ID: {signal_id}) - OFF")
                    time.sleep(0.5)
            time.sleep(1)

    def get_output_signal(self, signal_name):
        if signal_name not in self.output_signal_map:
            raise ValueError(f"Unknown output signal name: {signal_name}")
        signal_id = self.output_signal_map[signal_name]
        self.send_integer_data(signal_id)
        response = self.read_response()
        print(f"Retrieved output signal '{signal_name}' (ID: {signal_id}): {response}")
        return response

    def send_integer_data(self, data):
        if not isinstance(data, int):
            raise ValueError("Data must be an integer")
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(data.to_bytes(4, byteorder='little', signed=True))
        print(f"Sent integer data: {data}")

    def _generate_input_signal_map(self):
        return {
            "Set_left_direction": 101,
            "Set_right_direction": 102,
            "Set_Hazard_indicator": 103,
            "Set_Position_light": 105,
            "Set_Low_beam_light": 106,
            "Set_High_beam_light": 107,
            "Set_Position_left_turn": 108,
            "Set_Position+right_turn": 109,
        }

    def _generate_output_signal_map(self):
        return {
            "Dir_Ind_Li_inp": 111,
            "Hz_Li_Inp": 111,
            "Head_li_inp": 111,
        }

# Example usage
if __name__ == "__main__":
    hil = HILSimulator(com_port="COM13")
    try:
        hil.connect()

        # Example: Set right direction for 10 seconds
        hil.set_input_signal("Set_left_direction", 1, duration=1)
        response = hil.get_output_signal("Dir_Ind_Li_inp")
        print(f"Dir_Ind_Li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(8)  # Receive 10 bytes of data
        print(f"Received direction inp sts: {raw_data}")
		# Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_right_direction", 0, duration=4)  # Turn on Low Beam
        response = hil.get_output_signal("Dir_Ind_Li_inp")
        print(f"Dir_Ind_Li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received direction inp sts: {raw_data}")
        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_Hazard_indicator", 0, duration=1)  # Turn on hazard Beam
        response = hil.get_output_signal("Hz_Li_Inp")
        print(f"Hz_Li_Inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received Hazard inp sts: {raw_data}")
        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_Position_light", 0, duration=1)  # Turn on position Beam
        response = hil.get_output_signal("Head_li_inp")
        print(f"Head_li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received position light inp sts: {raw_data}")
        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_Low_beam_light", 0, duration=5)  # Turn on Low Beam
        response = hil.get_output_signal("Head_li_inp")
        print(f"Head_li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received low beam inp sts: {raw_data}")
        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_High_beam_light", 0, duration=3)  # Turn on high Beam
        response = hil.get_output_signal("Head_li_inp")
        print(f"Head_li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received high beam inp sts: {raw_data}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        hil.disconnect()'''


#testing

import time
import serial  # For COM port communication
import chardet

class HILSimulator:
    def __init__(self, com_port, baudrate=115200, timeout=1):
        self.com_port = com_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.input_signal_map = self._generate_input_signal_map()
        self.output_signal_map = self._generate_output_signal_map()
        self.active_signals = {}
        self.blink_flags = {}

    def connect(self):
        try:
            self.serial_conn = serial.Serial(self.com_port, baudrate=self.baudrate, timeout=self.timeout)
            print(f"Connected to HIL simulator on {self.com_port}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.com_port}: {e}")

    def disconnect(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Disconnected from HIL simulator.")

    def send_command(self, command):
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(command.encode('ISO-8859-1') + b'\n')
        time.sleep(0.1)

    def read_response(self):
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        response = self.serial_conn.readline()
        detected_encoding = chardet.detect(response)['encoding']
        if not detected_encoding or detected_encoding.lower() == 'ascii':
            detected_encoding = 'utf-8'
        print(f"Detected encoding: {detected_encoding}")
        hex_response = response.hex()
        return hex_response

    def receive_data(self, num_bytes):
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        data = self.serial_conn.read(num_bytes)
        hex_data = data.hex()
        return hex_data

    def set_input_signal(self, signal_name, value, duration=1):
        if signal_name not in self.input_signal_map:
            raise ValueError(f"Unknown input signal name: {signal_name}")
        signal_id = self.input_signal_map[signal_name]
        self.active_signals[signal_name] = value

        if value == 1:
            self.send_integer_data(signal_id)
            self.send_integer_data(value)
            self.blink_flags[signal_name] = True
            print(f"Set input signal '{signal_name}' (ID: {signal_id}) to value: {value}")
            
            # Send the signal for the specified duration
            end_time = time.time() + duration
            while time.time() < end_time:
                self.send_integer_data(signal_id)
                self.send_integer_data(value)
                time.sleep(1)  # Adjust this sleep time if needed

            # Reset the signal after the duration
            self.send_integer_data(signal_id)
            self.send_integer_data(0)
            self.blink_flags[signal_name] = False
            print(f"Reset input signal '{signal_name}' (ID: {signal_id}) after {duration} seconds")
        else:
            print(f"Input signal '{signal_name}' is set to 0, no command sent.")

    def maintain_signals(self):
        while True:
            for signal_name, value in self.active_signals.items():
                if value == 1 and self.blink_flags.get(signal_name, False):
                    signal_id = self.input_signal_map[signal_name]
                    self.send_integer_data(signal_id)
                    self.send_integer_data(1)
                    print(f"Blinking input signal '{signal_name}' (ID: {signal_id}) - ON")
                    time.sleep(0.5)
                    self.send_integer_data(signal_id)
                    self.send_integer_data(0)
                    print(f"Blinking input signal '{signal_name}' (ID: {signal_id}) - OFF")
                    time.sleep(0.5)
            time.sleep(1)

    def get_output_signal(self, signal_name):
        if signal_name not in self.output_signal_map:
            raise ValueError(f"Unknown output signal name: {signal_name}")
        signal_id = self.output_signal_map[signal_name]
        self.send_integer_data(signal_id)
        response = self.read_response()
        print(f"Retrieved output signal '{signal_name}' (ID: {signal_id}): {response}")
        return response

    def send_integer_data(self, data):
        if not isinstance(data, int):
            raise ValueError("Data must be an integer")
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(data.to_bytes(4, byteorder='little', signed=True))
        print(f"Sent integer data: {data}")

    def _generate_input_signal_map(self):
        return {
            "Set_left_direction": 101,
            "Set_right_direction": 102,
            "Set_Hazard_indicator": 103,
            "Set_Position_light": 105,
            "Set_Low_beam_light": 106,
            "Set_High_beam_light": 107,
            "Set_Position_left_turn": 108,
            "Set_Position+right_turn": 109,
        }

    def _generate_output_signal_map(self):
        return {
            "Dir_Ind_Li_inp": 111,
            "Hz_Li_Inp": 111,
            "Head_li_inp": 111,
        }

# Example usage
if __name__ == "__main__":
    hil = HILSimulator(com_port="COM10")
    try:
        hil.connect()

        # Example: Set right direction for 10 seconds
        hil.set_input_signal("Set_left_direction", 1, duration=3)
        response = hil.get_output_signal("Dir_Ind_Li_inp")
        print(f"Dir_Ind_Li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(8)  # Receive 10 bytes of data
        print(f"Received direction inp sts: {raw_data}")

        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_right_direction", 0, duration=4)  # Turn on Low Beam
        response = hil.get_output_signal("Dir_Ind_Li_inp")
        print(f"Dir_Ind_Li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received direction inp sts: {raw_data}")

        # Example: Set Hazard Indicator and validate its status
        hil.set_input_signal("Set_Hazard_indicator", 0, duration=1)  # Turn on hazard Beam
        response = hil.get_output_signal("Hz_Li_Inp")
        print(f"Hz_Li_Inp: {response}")

        # Example: Set Position Light and validate its status
        hil.set_input_signal("Set_Position_light", 0, duration=1)  # Turn on position Beam
        response = hil.get_output_signal("Head_li_inp")
        print(f"Head_li_inp: {response}")

        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_Low_beam_light", 0, duration=5)  # Turn on Low Beam
        response = hil.get_output_signal("Head_li_inp")
        print(f"Head_li_inp: {response}")

        # Example: Set High Beam and validate its status
        hil.set_input_signal("Set_High_beam_light", 0, duration=3)  # Turn on high Beam
        response = hil.get_output_signal("Head_li_inp")
        print(f"Head_li_inp: {response}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        hil.disconnect()
		
	   
	   
	   
 
'''import time
import serial  # For COM port communication
import chardet

class HILSimulator:
    def __init__(self, com_port, baudrate=115200, timeout=1):
        """
        Initialize the HIL simulator communication over the specified COM port.
        :param com_port: COM port name (e.g., 'COM1', '/dev/ttyUSB0')
        :param baudrate: Communication baud rate (default: 115200)
        :param timeout: Read timeout in seconds (default: 1)
        """
        self.com_port = com_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.input_signal_map = self._generate_input_signal_map()
        self.output_signal_map = self._generate_output_signal_map()
        self.active_signals = {}

    def connect(self):
        """
        Establish a connection to the HIL simulator via the COM port.
        """
        try:
            self.serial_conn = serial.Serial(
                self.com_port, baudrate=self.baudrate, timeout=self.timeout
            )
            print(f"Connected to HIL simulator on {self.com_port}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.com_port}: {e}")

    def disconnect(self):
        """
        Disconnect from the HIL simulator.
        """
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Disconnected from HIL simulator.")

    def send_command(self, command):
        """
        Send a command to the HIL simulator.
        :param command: Command string to send
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(command.encode('ISO-8859-1') + b'\n')
        time.sleep(0.1)

    def read_response(self):
        """
        Read a response from the HIL simulator.
        :return: Response string in hexadecimal format
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        response = self.serial_conn.readline()
        detected_encoding = chardet.detect(response)['encoding']
        if not detected_encoding or detected_encoding.lower() == 'ascii':
            detected_encoding = 'utf-8'  # Force to UTF-8 if detection fails or is ASCII
        print(f"Detected encoding: {detected_encoding}")
        hex_response = response.hex()  # Convert to hexadecimal
        return hex_response

    def receive_data(self, num_bytes):
        """
        Receive raw data from the HIL simulator.
        :param num_bytes: Number of bytes to read
        :return: Raw data bytes in hexadecimal format
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        data = self.serial_conn.read(num_bytes)
        hex_data = data.hex()  # Convert to hexadecimal
        return hex_data

    def set_input_signal(self, signal_name, value):
        """
        Set an input signal value in the HIL simulator.
        :param signal_name: Name of the input signal to set
        :param value: Value to set for the input signal
        """
        if signal_name not in self.input_signal_map:
            raise ValueError(f"Unknown input signal name: {signal_name}")
        signal_id = self.input_signal_map[signal_name]
        self.active_signals[signal_name] = value

        if value == 1:
            self.send_integer_data(signal_id)
            self.send_integer_data(value)
            print(f"Set input signal '{signal_name}' (ID: {signal_id}) to value: {value}")
        else:
            print(f"Input signal '{signal_name}' is set to 0, no command sent.")

    def maintain_signals(self):
        """
        Maintain active signals by continuously sending the command for active signals.
        """
        while True:
            for signal_name, value in self.active_signals.items():
                if value == 1:
                    signal_id = self.input_signal_map[signal_name]
                    self.send_integer_data(signal_id)
                    self.send_integer_data(value)
                    print(f"Maintaining input signal '{signal_name}' (ID: {signal_id}) with value: {value}")
            time.sleep(1)  # Adjust the frequency as needed

    def get_output_signal(self, signal_name):
        """
        Get an output signal value from the HIL simulator.
        :param signal_name: Name of the output signal to retrieve
        :return: Signal value in hexadecimal format
        """
        if signal_name not in self.output_signal_map:
            raise ValueError(f"Unknown output signal name: {signal_name}")
        signal_id = self.output_signal_map[signal_name]
        self.send_integer_data(signal_id)
        response = self.read_response()
        print(f"Retrieved output signal '{signal_name}' (ID: {signal_id}): {response}")
        return response

    def send_integer_data(self, data):
        """
        Send integer data to the HIL simulator.
        :param data: Integer data to send
        """
        if not isinstance(data, int):
            raise ValueError("Data must be an integer")
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(data.to_bytes(4, byteorder='little', signed=True))
        print(f"Sent integer data: {data}")

    def _generate_input_signal_map(self):
        """
        Generate a mapping of input signal names to signal IDs from the HIL model.
        Replace or expand this dictionary with actual input signal names and IDs.
        """
        return {
            "Set_left_direction": 101,
            "Set_right_direction": 102,
            "Set_Hazard_indicator": 103,
            "Set_Position_light": 105,
            "Set_Low_beam_light": 106,
            "Set_High_beam_light": 107,
            "Set_Position+left_turn": 108,
            "Set_Position+right_turn": 109,
        }

    def _generate_output_signal_map(self):
        """
        Generate a mapping of output signal names to signal IDs from the HIL model.
        Replace or expand this dictionary with actual output signal names and IDs.
        """
        return {
            "Dir_Ind_Li_inp": 111,
            "Hz_Li_Inp": 111,
            "Head_li_inp":111,
        }

# Example usage
if __name__ == "__main__":
    hil = HILSimulator(com_port="COM13")
    try:
        hil.connect()

        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_left_direction",0)  # Turn on Low Beam
        response = hil.get_output_signal("Dir_Ind_Li_inp")
        print(f"Dir_Ind_Li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received direction inp sts: {raw_data}")
        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_right_direction", 1)  # Turn on Low Beam
        response = hil.get_output_signal("Dir_Ind_Li_inp")
        print(f"Dir_Ind_Li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received direction inp sts: {raw_data}")
        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_Hazard_indicator", 0)  # Turn on hazard Beam
        response = hil.get_output_signal("Hz_Li_Inp")
        print(f"Hz_Li_Inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received Hazard inp sts: {raw_data}")
        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_Position_light", 0)  # Turn on position Beam
        response = hil.get_output_signal("Head_li_inp")
        print(f"Head_li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received position light inp sts: {raw_data}")
        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_Low_beam_light", 0)  # Turn on Low Beam
        response = hil.get_output_signal("Head_li_inp")
        print(f"Head_li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received low beam inp sts: {raw_data}")
        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_High_beam_light", 0)  # Turn on high Beam
        response = hil.get_output_signal("Head_li_inp")
        print(f"Head_li_inp: {response}")

        # Example: Receive raw data from the HIL simulator
        raw_data = hil.receive_data(10)  # Receive 10 bytes of data
        print(f"Received high beam inp sts: {raw_data}")
		

    except Exception as e:
        print(f"Error: {e}")
    finally:
     hil.disconnect()'''






	   
'''	   
import time
import serial  # For COM port communication
import chardet

class HILSimulator:
    def __init__(self, com_port, baudrate=115200, timeout=1):
        """
        Initialize the HIL simulator communication over the specified COM port.
        :param com_port: COM port name (e.g., 'COM1', '/dev/ttyUSB0')
        :param baudrate: Communication baud rate (default: 115200)
        :param timeout: Read timeout in seconds (default: 1)
        """
        self.com_port = com_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.input_signal_map = self._generate_input_signal_map()
        self.output_signal_map = self._generate_output_signal_map()
        self.active_signals = {}
        self.blink_flags = {}

    def connect(self):
        """
        Establish a connection to the HIL simulator via the COM port.
        """
        try:
            self.serial_conn = serial.Serial(
                self.com_port, baudrate=self.baudrate, timeout=self.timeout
            )
            print(f"Connected to HIL simulator on {self.com_port}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.com_port}: {e}")

    def disconnect(self):
        """
        Disconnect from the HIL simulator.
        """
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Disconnected from HIL simulator.")

    def send_command(self, command):
        """
        Send a command to the HIL simulator.
        :param command: Command string to send
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(command.encode('ISO-8859-1') + b'\n')
        time.sleep(0.1)

    def read_response(self):
        """
        Read a response from the HIL simulator.
        :return: Response string in hexadecimal format
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        response = self.serial_conn.readline()
        detected_encoding = chardet.detect(response)['encoding']
        if not detected_encoding or detected_encoding.lower() == 'ascii':
            detected_encoding = 'utf-8'  # Force to UTF-8 if detection fails or is ASCII
        print(f"Detected encoding: {detected_encoding}")
        hex_response = response.hex()  # Convert to hexadecimal
        return hex_response

    def receive_data(self, num_bytes):
        """
        Receive raw data from the HIL simulator.
        :param num_bytes: Number of bytes to read
        :return: Raw data bytes in hexadecimal format
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        data = self.serial_conn.read(num_bytes)
        hex_data = data.hex()  # Convert to hexadecimal
        return hex_data

    def set_input_signal(self, signal_name, value):
        """
        Set an input signal value in the HIL simulator.
        :param signal_name: Name of the input signal to set
        :param value: Value to set for the input signal
        """
        if signal_name not in self.input_signal_map:
            raise ValueError(f"Unknown input signal name: {signal_name}")
        signal_id = self.input_signal_map[signal_name]
        self.active_signals[signal_name] = value

        if value == 1:
            self.send_integer_data(signal_id)
            self.send_integer_data(value)
            self.blink_flags[signal_name] = True  # Set blink flag
            print(f"Set input signal '{signal_name}' (ID: {signal_id}) to value: {value}")
        else:
            self.blink_flags[signal_name] = False  # Clear blink flag
            print(f"Input signal '{signal_name}' is set to 0, no command sent.")

    def maintain_signals(self):
        """
        Maintain active signals by continuously sending the command for active signals.
        """
        while True:
            for signal_name, value in self.active_signals.items():
                if value == 1 and self.blink_flags.get(signal_name, False):
                    signal_id = self.input_signal_map[signal_name]
                    self.send_integer_data(signal_id)
                    self.send_integer_data(1)
                    time.sleep(0.5)  # Adjust blink interval as needed
                    self.send_integer_data(signal_id)
                    self.send_integer_data(0)
                    time.sleep(0.5)  # Adjust blink interval as needed
                    print(f"Blinking input signal '{signal_name}' (ID: {signal_id})")
            time.sleep(1)  # Adjust the frequency as needed

    def get_output_signal(self, signal_name):
        """
        Get an output signal value from the HIL simulator.
        :param signal_name: Name of the output signal to retrieve
        :return: Signal value in hexadecimal format
        """
        if signal_name not in self.output_signal_map:
            raise ValueError(f"Unknown output signal name: {signal_name}")
        signal_id = self.output_signal_map[signal_name]
        self.send_integer_data(signal_id)
        response = self.read_response()
        print(f"Retrieved output signal '{signal_name}' (ID: {signal_id}): {response}")
        return response

    def send_integer_data(self, data):
        """
        Send integer data to the HIL simulator.
        :param data: Integer data to send
        """
        if not isinstance(data, int):
            raise ValueError("Data must be an integer")
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("No active connection to the HIL simulator.")
        self.serial_conn.write(data.to_bytes(4, byteorder='little', signed=True))
        print(f"Sent integer data: {data}")

    def _generate_input_signal_map(self):
        """
        Generate a mapping of input signal names to signal IDs from the HIL model.
        Replace or expand this dictionary with actual input signal names and IDs.
        """
        return {
            "Set_left_direction": 101,
            "Set_right_direction": 102,
            "Set_Hazard_indicator": 103,
            "Set_Position_light": 105,
            "Set_Low_beam_light": 106,
            "Set_High_beam_light": 107,
            "Set_Position+left_turn": 108,
            "Set_Position+right_turn": 109,
        }

    def _generate_output_signal_map(self):
        """
        Generate a mapping of output signal names to signal IDs from the HIL model.
        Replace or expand this dictionary with actual output signal names and IDs.
        """
        return {
            "Dir_Ind_Li_inp": 111,
            "Hz_Li_Inp": 111,
            "Head_li_inp":111,
        }

# Example usage
if __name__ == "__main__":
    hil = HILSimulator(com_port="COM13")
    try:
        hil.connect()

        # Example: Set Low Beam and validate its status
        hil.set_input_signal("Set_left_direction", 1)  # Turn on Low Beam
        response = hil.get_output_signal("Dir_Ind_Li_inp")
        print(f"Dir_Ind_Li_inp: {response}")

        # Start blinking LED
        hil.maintain_signals()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        hil.disconnect()
'''

	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

		
