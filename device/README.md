# Raspberry Pi Smart Car - DDD Architecture Demo

A demonstration project implementing Domain-Driven Design (DDD) with Hexagonal Architecture for the [Freenove 4WD Smart Car Kit for Raspberry Pi](https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi).

## Project Overview

This project showcases an approach to IoT device programming by applying software architecture patterns typically used in enterprise applications. While the hardware is relatively simple, the codebase demonstrates how clean architecture principles can be applied to embedded systems and IoT development.

The implementation separates business logic from infrastructure concerns, making the code testable, maintainable, and extensible - key considerations for any IoT project.

## Architecture

The project follows **Domain-Driven Design (DDD)** principles with **Hexagonal Architecture** (Ports and Adapters pattern):

- **Domain Layer**: Core business entities (Car, ObstacleDetector), value objects (Distance, Speed), and domain events
- **Application Layer**: Use cases and command handlers that orchestrate domain logic
- **Infrastructure Layer**: Hardware adapters for GPIO, motors, sensors, and LEDs

**Note**: As this is a small-scale demonstration, some architectural components have been simplified or omitted. A production IoT system would include additional patterns such as repositories, aggregates, and more sophisticated event handling mechanisms.

## Educational Context

This project was developed as part of the [An Introduction to Programming the Internet of Things (IoT)](https://www.coursera.org/learn/iot-devices-il) specialization on Coursera, demonstrating the application of software engineering best practices to IoT device programming.

## Setup

### Prerequisites

- Raspberry Pi with Freenove 4WD Smart Car Kit assembled
- Python 3.11+
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/JosePFs/4wd-car.git
cd 4wd-car
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Key Features

- **Clean Architecture**: Clear separation between domain logic and hardware implementation
- **Event-Driven Design**: Domain events for state changes and inter-component communication
- **Thread-Safe Operations**: Concurrent handling of car control and obstacle detection
- **Type Safety**: Full type hints for better IDE support and code reliability
- **Testability**: Domain logic isolated from hardware dependencies

## Technology Stack

- Python 3.11+
- RPi.GPIO for Raspberry Pi hardware control
- Threading for concurrent operations
- Dataclasses for immutable value objects

## Project Structure
```
car_demo/
├── domain/          # Business logic and domain models
├── application/     # Use cases and command handlers
└── infrastructure/  # Hardware adapters and external interfaces
```

## Purpose

- Software architecture in IoT contexts
- Clean code principles applied to embedded systems
- DDD and Hexagonal Architecture
- Raspberry Pi and hardware integration

---

**Hardware Reference**: [Freenove 4WD Smart Car Kit](https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi)

**Course**: [IoT Devices Specialization - Coursera](https://www.coursera.org/learn/iot-devices-il)