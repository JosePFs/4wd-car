# 4WD Smart Car - IoT Control System

A distributed IoT system for controlling the [Freenove 4WD Smart Car Kit for Raspberry Pi](https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi) using Domain-Driven Design principles.

## Project Structure

This project is organized into four independent modules:

```
4wd-car/
├── config_common/     # Shared configuration and constants
├── client/            # Keyboard controller
├── server/            # UDP server relay
└── device/            # Raspberry Pi car control logic
```

### Modules

#### 1. `config_common/`

Shared configuration package used by `client` and `server`.

**Purpose:**

- Define common commands (FORWARD, BACKWARD, LEFT, RIGHT, etc.)
- Share environment variables (UDP host, port, etc.)
- Maintain consistent protocol across modules

**Installation:**
Each module includes this as a local dependency via `requirements.txt`:

```txt
-e ../config_common
```

#### 2. `client/`

Keyboard controller application that runs on your laptop or desktop.

**Features:**

- Captures keyboard input (arrow keys, WASD, Space, Shift)
- Sends UDP commands to the server or directly to the device
- Clean terminal handling with proper restoration on exit

**Controls:**

- Arrow Keys / WASD: Movement (Forward/Backward/Left/Right)
- Space: Toggle car ON/OFF
- Shift left: Toggle obstacle detection ON/OFF
- Shift right: Toggle car ON/OFF
- ESC: Exit application

#### 3. `server/`

UDP server relay (middleware component).

**Purpose:**

- Receives UDP commands from client
- Relays commands to the Raspberry Pi device
- Can add logging, filtering, or additional processing

#### 4. `device/`

Raspberry Pi application that controls the physical 4WD car.

**Features:**

- Receives UDP commands over the network
- Controls motors, LEDs, buzzer via GPIO
- Obstacle detection with ultrasonic sensor
- Implements Domain-Driven Design with Hexagonal Architecture

**Architecture:**

- **Domain Layer:** Entities (Car, ObstacleDetector), Value Objects (Speed, Distance), Events
- **Application Layer:** Command handlers, use cases
- **Infrastructure Layer:** GPIO adapters, UDP server, event bus

**Standalon Usage for testing purposes:**

```bash
cd device
python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Setup

### Prerequisites

- Python 3.11+
- Raspberry Pi with Freenove 4WD Smart Car Kit (for device module)
- Network connectivity between client and device

### Installation

1. **Clone the repository and install system dependencies:**

```bash
git clone https://github.com/JosePFs/4wd-car.git
cd 4wd-car

# On Raspberry Pi OS
sudo apt-get update
sudo apt-get install -y python3-libcamera python3-smbus libcap-dev
```

2. **Setup config_common:**

```bash
cd config_common
# Edit .env or environment variables as needed
export UDP_HOST="x.x.x.x"  # Raspberry Pi IP
export UDP_PORT="5000"
```

3. **Setup client:**

```bash
cd client
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Setup device (on Raspberry Pi):**

```bash
cd device
python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements.txt
```

5. **Setup server (on Raspberry Pi):**

```bash
cd server
python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements.txt
```

### Running the System

1. **Start the device for testing (Raspberry Pi):**

```bash
cd device
python main.py
```

2. **Start the server (Raspberry Pi):**

```bash
cd server
python main.py
```

3. **Start the client (laptop/desktop):**

```bash
cd client
python main.py
```

3. **Control the car using keyboard!**

## Configuration

### Shared Configuration (`config_common/`)

The `config_common` module provides:

**Commands:**

```python
class Command(Enum):
    [...]
```

**Environment Variables:**

- `UDP_HOST`: Target device IP address
- `UDP_PORT`: UDP port for communication (default: 5000)

## Architecture Highlights

The `device` module implements clean software architecture patterns:

- **Domain-Driven Design:** Clear separation between business logic and infrastructure
- **Hexagonal Architecture:** Domain independent of delivery mechanisms (UDP, GPIO, etc.)
- **Event-Driven Design:** Components communicate via domain events
- **Clean Code:** Type hints, proper abstractions, single responsibility principle

For detailed implementation, see the [device module](./device/).

The `client` and `server` modules are simpler applications designed to interact with the device.

## Educational Context

This project was developed as part of the [Hands-on Internet of Things Specialization](https://www.coursera.org/learn/iot-devices-il) specialization on Coursera.

## Hardware Reference

[Freenove 4WD Smart Car Kit for Raspberry Pi](https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi)

## License

MIT
