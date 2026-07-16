# LLM Mobility Control

LLM(Google Gemini)을 활용하여 사용자의 자연어 명령을 ROS2 기반 TurtleBot3의 이동 명령으로 변환하는 프로젝트입니다.

---

## Overview

사용자가 자연어로 이동 명령을 입력하면 LLM이 이를 이해하여 정형화된 명령(JSON)으로 변환하고, ROS2 Node가 이를 파싱하여 `/cmd_vel` 토픽으로 이동 명령을 발행합니다.

### System Flow

```
User
  │
  ▼
Natural Language Command
  │
  ▼
Google Gemini API
  │
  ▼
JSON Command
  │
  ▼
Command Parser
  │
  ▼
ROS2 Twist (/cmd_vel)
  │
  ▼
TurtleBot3
```

---

## Features

- Natural language command understanding using LLM
- JSON-based motion command generation
- ROS2 integration
- Sequential command execution
- Easy extension for LiDAR and Navigation2

---

## Project Structure

```
src/
└── llm_controller/
    ├── llm_node.py          # Main ROS2 Node
    ├── llm_api.py           # Gemini API communication
    ├── command_parser.py    # JSON command parser
    ├── prompt.py            # LLM Prompt
    ├── config.py            # API configuration (API key excluded)
    ├── package.xml
    └── setup.py
```

---

## Development Environment

- Ubuntu 24.04
- ROS2 Jazzy
- Python 3.12
- TurtleBot3 Simulation
- Google Gemini API

---

## Example

### User Input

```
앞으로 1m 갔다가 왼쪽으로 90도 돌아
```

### LLM Output

```json
{
  "commands": [
    {
      "action": "forward",
      "distance": 1.0
    },
    {
      "action": "left",
      "angle": 90
    }
  ]
}
```

### ROS2 Execution

```
Forward 1.0 m
↓

Rotate Left 90°

↓

Mission Complete
```

---

## Running

Build the workspace.

```bash
colcon build
source install/setup.bash
```

Run the node.

```bash
ros2 run llm_controller llm_node
```

---

## API Key

For security reasons, API keys are **not included** in this repository.

Set your own API key before running.

Example:

```bash
export GEMINI_API_KEY=YOUR_API_KEY
```

or use a `.env` file.

---

## Future Work

- LiDAR-aware obstacle avoidance
- Odometry-based distance control
- Navigation2 integration
- Multi-step autonomous navigation
- Vision-Language Model (VLM) integration

---

## Author

Song Minjun

KAIST Mechanical Engineering

Physical AI Project
