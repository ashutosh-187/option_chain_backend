# Option Chain Backend

This project is a backend service for handling real-time option chain data. It is built using Python with Flask for REST APIs, Socket.IO for real-time socket connections, and the Mibian library for calculating implied volatility and option Greeks. Additionally, it leverages Pandas and NumPy for data manipulation and Redis for caching and faster retrieval of real-time data.

## Features
- Real-time market data updates using the XTS Market Data API.
- RESTful APIs for accessing option chain data.
- Real-time socket connections for live updates.
- Calculation of implied volatility and option Greeks using the Mibian library.
- Efficient data handling with Pandas and NumPy.
- Redis caching for faster data retrieval.

## Prerequisites
- Python 3.7 or higher
- Redis server installed and running
- XTS Market Data API credentials

## Installation and Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/ashutosh-187/option_chain_backend.git
    cd option_chain_backend
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Start the Redis server:
    - Open WSL and execute the following command:
      ```bash
      redis-server
      ```

4. Start the project:
    - Run the `master.py` script:
      ```bash
      python master.py
      ```
    - Run the `web_socket.py` script:
      ```bash
      python web_socket.py
      ```
    - Finally, start the server:
      ```bash
      python server.py
      ```

## Usage
- The backend fetches real-time market data using the XTS Market Data API and updates it in real time.
- Redis is used for caching the data, ensuring faster retrieval and improved performance.
- REST APIs and socket connections can be used to access and subscribe to the data.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- [Flask](https://flask.palletsprojects.com/)
- [Socket.IO](https://socket.io/)
- [Mibian](https://pypi.org/project/mibian/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [Redis](https://redis.io/)
- [XTS Market Data API](https://symphonyfintech.com/xts-market-data-front-end-api-v2/)

Feel free to contribute to this project by submitting issues or pull requests.