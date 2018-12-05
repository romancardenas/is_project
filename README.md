Wind Turbine Anomaly Detection
-
Description to be done.

System Requirements
- 
1. The system has been tested on UNIX environments. A bash terminal is required
2. `Python 3`. `Python 3.6.X` is recommended, as the project uses `TensorFlow`, which is not officially supported in `Python 3.7` yet
3. The following `Python 3` packages: `pyknow`, `numpy`, `pandas`, `keras`, `tensorflow`, `seaborn`
- Make sure that your Python 3 virtual environment has these packages installed. They can be easily installed by running the bash script `bash_scripts/install_dependencies.sh`


Instructions
-
For running the code related to this project, the following steps must be done:
1. open a bash for each process to be executed
2. change the working directory of the bash to `<project folder>/`
3. Call the bash script linked to the process of interest

For running the processes, the following order is recommended:
- `bash bash_scripts/broker.sh`: Starts the MQTT Broker
- `bash bash_scripts/server.sh`: Starts the central server
- `bash bash_scripts/wind_turbine_1.sh`: Starts wind turbine client
- [optional] - `bash bash_scripts/client.sh`: Starts the RPC client (emulates the energy provider, who wants to know the status of the wind turbines)
- `bash bash_scripts/wind_turbine_2.sh`: Starts a second wind turbine client. The system server is able to support multiple wind turbines at the same time, and it creates dynamically all the required resources for granting service to completely new wind turbines

For changing the simulation parameters:
1. Open wind_turbine/new_wind_turbine.py.
2. Navigate to __init__ in WindTurbine class.
3. Find the line self.faulty = faulty_turbine.fu_data().
4. You can change the following parameters:
	-fum = (0,1,2,3). Defines the fault to be used. 0 - picks at random from the three, 1 - random P, 2 - P*reduced, 3 - P - offset.
	-test = (0,1). 1 initiates test mode - one fault only which starts at line 100.
	-reduced. Used in fault number 2.
	-offset. Used in fault number 3.
Issues
-
This repository is not granted to be under constant development. If you experience any trouble, or want to ask something about the project, send an email to `rcardenas.rod@gmail.com`. However, no response is ensured.