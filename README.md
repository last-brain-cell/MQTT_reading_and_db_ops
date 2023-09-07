# MQTT Subscriber

This repository contains code for an inventory management system that utilizes MQTT for data communication and MongoDB for data storage. The system manages product information and updates it based on incoming data from RFID scans. Below are instructions on how to set up and use the system.

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Code Structure](#code-structure)

## Requirements

Before getting started, make sure you have the following requirements installed:

- Git
- Python 3.11
- MongoDB
- Required Python packages (see individual code README files for details)

## Installation

1. Clone the repository to your local machine:

   [Download Git](https://git-scm.com/downloads)

   ```bash
   git clone https://github.com/last-brain-cell/MQTT_reading_and_db_ops.git
   ```

2. Install Python 3.11:

[Download Python](https://www.python.org/downloads/)

3. Install required Python packages using pip. Navigate to the root directory of each code file and run:

   ```bash
   pip install -r requirements.txt
   ```

4. Install MongoDB:

[Download MongoDB](https://www.mongodb.com/try/download/community)

## Usage

To set up and use the Inventory Management System, follow these steps:

### 1. Install Requirements

Before running the code, make sure you have the following requirements installed on your system:

- **Python 3.11**: If you don't have Python 3.11 installed, you can download it from [Python's official website](https://www.python.org/downloads/).

- **MongoDB**: You need to have MongoDB installed. You can download it from the [MongoDB Download Center](https://www.mongodb.com/try/download/community).

- **Required Python Packages**: Each code file has its own set of required packages listed in their respective README files. Navigate to the code directory and follow the installation instructions in the README file to install the required packages.

![mqtt_broker](https://github.com/last-brain-cell/MQTT_reading_and_db_ops/blob/master/Help/requirements.png)

### 2. Configuration

#### MQTT Broker

- By default, the code is configured to use the public MQTT broker provided by Eclipse (broker address: `mqtt.eclipseprojects.io`). If you have your own MQTT broker, you can modify the `mqttBroker` variable in the code to use your broker's address.

![mqtt_broker](https://github.com/last-brain-cell/MQTT_reading_and_db_ops/blob/master/Help/mqtt_broker.png)

#### MongoDB Configuration

- Ensure that your MongoDB server is running and accessible. The code is configured to connect to a local MongoDB server by default. If your MongoDB server is hosted remotely or has custom authentication, you can modify the MongoDB connection URL in the code. Example:

![mongodb_compass_connect](https://github.com/last-brain-cell/MQTT_reading_and_db_ops/blob/master/Help/mongodb_compass_connect.png)

   
    db_client = MongoClient("mongodb://your-mongodb-server-address:27017/")
   

![mongodb_connect](https://github.com/last-brain-cell/MQTT_reading_and_db_ops/blob/master/Help/mongodb_connect.png)

### 3. Running the Code

#### Subscriber (rfid_data_subscriber.py)

- Navigate to the `rfid_data_subscriber` directory.

- Install the required Python packages by running:

    ```bash
    pip install -r requirements.txt
    ```

- Run the subscriber code:

    ```bash
    python rfid_data_subscriber.py
    ```

The subscriber will connect to the MQTT broker, listen for incoming RFID data, process it, and update the database as necessary.

#### Publisher (test_publisher.py)

- If you want to simulate RFID scans, you can use the `test_publisher.py` code.

- Run the publisher code:

    ```bash
    python test_publisher.py
    ```

- Press Enter to simulate a test scan. The code will generate random RFID data and publish it to MQTT topics.

### 4. Checking Data

You can check the data in the MongoDB database to verify updates and new entries. The database is named "Product_Management," and you can explore the collections and documents to view the stored product information and RFID data.

That's it! You have set up and used the Inventory Management System.


## Code Structure

- [rfid_data_subscriber.py](./rfid_data_subscriber/README.md) - Subscriber code for processing RFID data and updating the database.
- [test_publisher.py](./test_publisher/README.md) - Publisher code for simulating RFID scans and sending data to the subscriber.
- [HHDG - SpareInventory - excel.xlsx](./HHDG%20-%20SpareInventory%20-%20excel.xlsx) - Excel sheet containing product data.


