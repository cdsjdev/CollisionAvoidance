
# Collision Avoidance with AirSim

<a href="https://www.youtube.com/watch?v=9bEPKMctNpI"><img src="airsim.png"></a>

Reference: https://github.com/simondlevy/AirSimTensorFlow

This repository demonstrates how to use [Microsoft AirSim](https://github.com/Microsoft/AirSim) to collect image data from a simulated vehicle, train a neural network using TensorFlow, and perform real-time collision detection and multi-car simulations.

---

## 🧰 Prerequisites

- **Hardware:** [Recommended hardware](https://wiki.unrealengine.com/Recommended_Hardware) for Unreal Engine 4 is required for running AirSim. We recommend using the precompiled [AirSimNH Windows binary](https://github.com/Microsoft/AirSim/releases/download/v1.1.7/Neighbourhood.zip).
- **Python:** Use Python **3.9 (64-bit)** to ensure compatibility with TensorFlow and other dependencies.
- **Simulator:** [AirSim](https://github.com/Microsoft/AirSim), launched via `run.bat` in the AirSimNH folder.

---

## ⚙️ Setting Up the Conda Environment

Create and activate a Conda environment named `games` on Python 3.9:

```bash
conda create -n games python=3.9
conda activate games
```

---

## 🧪 Installing Dependencies

AirSim 1.8.1 is source-only and imports `numpy`/`msgpack` during its build. Install everything with build isolation off so it can see the prereqs:

```bash
pip install --no-build-isolation -r requirements.txt
```

If you prefer to avoid passing the flag each time, set once: `pip config set global.build-isolation false`.

Key pins include:

- `tensorflow==2.13.0` (uses `tensorflow.compat.v1`)
- `numpy==1.24.3`
- `airsim==1.8.1` (source build; needs numpy/msgpack present)
- `opencv-contrib-python==4.11.0.86`
- plus supporting packages in `requirements.txt`

Note: `numpy`/`msgpack` stay in `requirements.txt` to document exact versions; with isolation disabled, pip installs them before building AirSim.

---

## 🚀 Instructions for Running the Project

### 1. `image_collection.py`

- Launch AirSimNH using `run.bat`
- Run this script to start collecting first-person-view images
- The car drives forward and saves images to the `carpix` directory
- Stops when a collision is detected

### 2. `collision_training.py`

- Converts images to grayscale
- Labels them as “safe” or “collision”
- Trains a softmax neural network with TensorFlow
- Saves the model parameters as `params.pkl`

### 3. `collision_testing.py`

- Loads `params.pkl`
- Reconstructs the trained network
- Feeds live images from AirSim
- Stops the vehicle before collision is predicted

### 4. `CollisionAvoidance.py`

- Creates a second car that backs out of a parking space
- Runs in parallel with the main car using threads
- Includes potential for further autonomous behaviors

---

## 🧠 How It Works

- Images collected before a crash are labeled "safe", and the final image is labeled "collision"
- A softmax neural net is trained using TensorFlow 1.x API via `tensorflow.compat.v1`
- The trained model is saved using `pickle`
- During testing, live images are passed through the model to predict collisions and apply brakes
- `CollisionAvoidance.py` demonstrates multi-car behavior using AirSim APIs

---

## 🧊 Freezing Your Environment (Optional)

After setup, you can freeze your environment to recreate it later:

```bash
pip freeze > requirements_exact.txt
```

Then restore with:

```bash
pip install -r requirements_exact.txt
```

---

Happy simulating! 🏎️
```
