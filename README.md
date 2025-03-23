# Speech Demonstration for Baxter Robot

This project achieves how to demonstrate/control a Baxter robot using speech commands. It integrates speech recognition with ROS to translate voice inputs into robot actions.

## Environment

- **Operating System**: Ubuntu 18.04
- **ROS Version**: Melodic
- **Baxter SDK**: Installed and configured

## Speech Recognition

The speech recognition module processes voice inputs and publishes commands to the `voice_msg` ROS topic. 

### Key Components

1. **Libraries**:
   - `libais-lite-Ual.so`: Core library for the speech recognition engine. It must be placed in a system-accessible directory, such as:
     - `/home/znfs/anaconda3/lib/libais-lite-Ual.so` (for Anaconda environments)
     - `/usr/lib/libais-lite-Ual.so` (for system Python)
   - `libunikws.so`: Dynamically loaded by Python scripts. No additional setup is required.

2. **Grammar Files**:
   - Located in the `data/` folder. These files define the recognition rules and can be customized for specific projects.

3. **Example Scripts**:
   - `demo.py`: Basic example of speech recognition.
   - `demo_multi_thread.py`: Demonstrates multi-threaded speech recognition.

### Usage

Run the speech recognition script to publish commands to the `voice_msg` topic:
```
python baxter/src/speech/src/demo.py  # or demo_multi_thread.py
```

## Speech to Baxter Actions
The speech_baxter.py script subscribes to the voice_msg topic and translates speech commands into actions for the Baxter robot.

### Features
Joint Movements:
Move forward, backward, left, and right.
Rotate the wrist.
Gripper Control:
Open and close the gripper.
Command Bindings
The following commands are mapped to specific actions:

### Command	Action
1	Move forward
2	Move backward
3	Move right
4	Move left
5	Open gripper
6	Close gripper
7	Rotate wrist
....

### Running the Script
Ensure the Baxter robot is connected and enabled.
Start the ROS master:
Run the speech_baxter.py script

```
roscore
baxter/src/baxter_project/scripts/speech_baxter.py
```



## Custom Message Format
The voicemsg.msg file defines the custom message format for speech commands:

## Notes
Ensure the Baxter robot is properly initialized and enabled before running the scripts.
The paths for libraries and grammar files can be configured in the scripts as needed.
Extend the bindings dictionary in speech_baxter.py to add new commands.
