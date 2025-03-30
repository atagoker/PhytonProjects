# Pomodoro Timer (Terminal Edition)

A simple terminal-based Pomodoro Timer written in Python. Stay focused and productive with timed work and break sessions based on the Pomodoro Technique.

## What is the Pomodoro Technique?

The Pomodoro Technique is a time management method that breaks work into intervals:
- 25 minutes of focused work
- 5-minute short breaks
- 15-minute long break after 4 sessions

## Features

- Customizable session and break durations
- Automatically switches between work and break sessions
- Graceful exit with Ctrl + C
- Lightweight and runs in any terminal with Python

## Getting Started

### Prerequisites

- Python 3.x

## Configuration

To change durations, edit these values in `pomodoro.py`:

    WORK_DURATION = 25       # in minutes
    SHORT_BREAK = 5
    LONG_BREAK = 15
    SESSIONS_BEFORE_LONG_BREAK = 4

## Example Output

    Work Session 1
    ⏳ 24:59
    ⏳ 24:58
    ...
    ⏳ 00:01
    Time's up!
    Take a short break!

## License

This project is licensed under the MIT License. Feel free to fork and modify it to suit your workflow.

## Future Plans

- Add desktop notifications  
- Sound alerts at the end of sessions  
- GUI version with Tkinter
