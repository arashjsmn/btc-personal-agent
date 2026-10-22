# Personalized Bitcoin Analysis Agent

## Overview

A personalized Bitcoin analysis agent built with Python. The project retrieves Bitcoin market data, calculates technical indicators, generates explanations using an LLM, and uses multiple memory systems to personalize responses.

This project is for educational and research purposes. It does not guarantee market predictions or provide reliable financial advice.

## Features

- Retrieves BTC/USDT daily market data from Binance's public market-data API.
- Calculates 7-day and 25-day Simple Moving Averages (SMA) and 14-day Relative Strength Index (RSI).
- Uses Groq's API to generate natural-language explanations.
- Supports tool calling for saving user preferences.
- Implements short-term, long-term, and episodic memory.
- Records explicit user feedback and adapts explanation style.
- Includes automated unit tests for memory and feedback detection.

## Architecture

- `agent.py`: Coordinates the LLM, tools, memory systems, and response generation.
- `tools/market_data.py`: Retrieves Bitcoin market data.
- `tools/indicators.py`: Calculates technical indicators.
- `tools/btc_analysis.py`: Combines market data and indicators.
- `memory/short_term.py`: Stores conversation messages in memory during execution.
- `memory/long_term.py`: Stores persistent user preferences in JSON.
- `memory/episodic.py`: Stores dated events and feedback in JSON.
- `tests/`: Contains automated tests.
- `data/`: Stores persistent memory files.
- `.env.example`: Shows the required environment configuration.

## Memory Design

### Short-term memory

Stores recent user and assistant messages in the current Python process. It is not persistent across program restarts.

### Long-term memory

Stores user preferences, such as knowledge level, risk tolerance, investment horizon, and explanation style, in a JSON file.

### Episodic memory

Stores dated events, such as user feedback and previous analysis requests. Recent feedback can be included in the agent's prompt to improve future responses.

## Technical Indicators

- **SMA 7:** Average closing price over the latest seven daily candles.
- **SMA 25:** Average closing price over the latest twenty-five daily candles.
- **RSI 14:** A momentum indicator calculated from fourteen periods of price changes.

The current RSI implementation uses simple rolling averages. It does not implement Wilder's standard smoothing method.

The SMA comparison describes the relationship between two averages; it does not establish a long-term market trend by itself.

## Requirements

- Python 3.11 or another compatible Python version.
- A Groq API key.
- Internet access for market-data retrieval and LLM requests.

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root.
2. Add your Groq API key:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
```

3. Keep `.env` private and never commit it to version control.

## Running the Project

Run the agent's entry point according to the available interface. For example, if the project is invoked through `main.py`:

```bash
python main.py
```

Run an individual market-analysis test if its test script is available:

```bash
python test_btc_analysis.py
```

## Running Automated Tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

The current unit tests cover memory persistence and basic feedback detection. They do not, by themselves, verify every external API interaction or every LLM tool-calling scenario.

## Data Source and Limitations

Market data is retrieved from Binance's public BTC/USDT candlestick endpoint.

The latest daily candle may still be incomplete during the current trading day. Its closing price and volume may therefore change.

LLM-generated explanations may contain errors. Technical indicators are historical measurements, not guarantees of future price movements.

The feedback detector currently relies on predefined English phrases and may miss other wording or languages.

## Security

- Do not include `.env` or real API keys in a public repository or project archive.
- Use `.env.example` as the configuration template.
- Review generated data files before sharing the project.

## Research Direction

Potential improvements include more robust feedback classification, automated tool-calling tests, bounded conversation history, improved RSI calculation, and clearer separation between market-analysis requests and preference-management requests.
