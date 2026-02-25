# mock-clock

Control time in your tests by intercepting system time calls for testing time-dependent code

## Features

- Freeze time at a specific datetime or timestamp
- Advance time forward by seconds, minutes, hours, or days
- Rewind time backward for testing past scenarios
- Context manager for isolated time control within test scope
- Automatic restoration of real time after context exit
- Intercepts datetime.datetime.now() and datetime.datetime.utcnow()
- Intercepts time.time() and time.monotonic()
- Works with asyncio event loop time for async code
- Thread-safe time manipulation for concurrent tests
- No external dependencies - pure Python implementation
- Chainable API for fluent time manipulation
- Support for timezone-aware datetime objects
- Preserves microsecond precision in time values

## How to Use

Use this project when you need to:

- Quickly solve problems related to mock-clock
- Integrate python functionality into your workflow
- Learn how python handles common patterns

## Installation

```bash
# Clone the repository
git clone https://github.com/KurtWeston/mock-clock.git
cd mock-clock

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Built With

- python

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
