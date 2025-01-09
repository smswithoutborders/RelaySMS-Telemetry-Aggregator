# RelaySMS Telemetry Aggregator

Collects, analyzes, and exposes RelaySMS usage data via a unified API for transparent telemetry insights.

## Prerequisites

### Development Environment

1. **Python 3.8+**: Ensure Python is installed.
2. **Virtual Environment**: Install `virtualenv` for managing dependencies.

## Getting Started

### Development Setup

1. **Clone the Repository**:

   ```bash
    git clone https://github.com/smswithoutborders/RelaySMS-Telemetry-Aggregator.git
    cd RelaySMS-Telemetry-Aggregator
   ```

2. **Create a Virtual Environment**:

   ```bash
    python3 -m venv venv
    source venv/bin/activate
   ```

3. **Install Dependencies**:

   ```bash
    pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Copy `.env.example` to `.env` and update the values as needed.

   ```bash
    cp .env.example .env
   ```

5. **Start the Development Server**:

   ```bash
    fastapi dev main.py
   ```

   Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## References

1. [REST API V1 Resources](https://api.telemetry.smswithoutborders.com/docs)

## Contributing

To contribute:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-branch`.
3. Commit your changes: `git commit -m 'Add a new feature'`.
4. Push to the branch: `git push origin feature-branch`.
5. Open a Pull Request.

## License

This project is licensed under the GNU General Public License (GPL). See the [LICENSE](LICENSE) file for details.
