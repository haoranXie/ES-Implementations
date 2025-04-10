## Project Overview
This project implements various Evolutionary Strategy algorithms. It includes implementations for:

- Simple ES optimization  
- MNIST classification 
- MuJoCo environment control
## Installation
1. Create a virtual environment:
  ```sh
  python -m venv venv
  ```
2. Activate the virtual environment:
  - On Windows:
    ```sh
    venv\Scripts\activate
    ```
  - On macOS/Linux:
    ```sh
    source venv/bin/activate
    ```
3. Install the required dependencies:
  ```sh
  pip install -r requirements.txt
  ```

## Usage
Run simple ES optimization:
  ```sh
  python src/es_simple.py
  ```
Train on MNIST:
  ```sh
  python src/es_mnist.py
  ```
Run MuJoCo on HalfCheetah-v2:
  ```sh
  python src/es_mujoco.py
  ```
