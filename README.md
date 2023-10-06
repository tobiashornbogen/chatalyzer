# WhatsApp Chat Analysis

A GUI-based Python application to analyze WhatsApp chat history. It provides insights into the frequency of messages, response times, conversation initiators, and an adjusted analysis of response times outside back-and-forth rapid exchanges. The analysis results are presented both in text and graphically.

## Features

- Load a WhatsApp chat file.
- Analyze message counts per sender.
- Compute average response times.
- Determine conversation initiators based on a user-defined threshold.
- Analyze response times outside rapid back-and-forth exchanges.
- Visual representation of analysis results.

## Requirements

- Python 3.x
- pandas
- re
- matplotlib
- tkinter

## Installation

1. Clone the repository:
git clone https://github.com/your_github_username/WhatsAppChatAnalysis.git
2. Navigate to the project directory:
cd WhatsAppChatAnalysis
3. Install the required packages using pip:
pip install pandas matplotlib


## Usage

1. Run the script:
python chatproject.py
2. Use the GUI to load a WhatsApp chat `.txt` file.
3. Adjust the various thresholds if necessary.
4. Click on the "Analyze" button to see the results.

## Note

The WhatsApp chat `.txt` file can be exported from within a WhatsApp conversation by choosing "More" > "Export chat". Make sure you export the chat without media to get a `.txt` file.

## Contribution

Contributions are welcome! Feel free to create issues or submit pull requests.

## License

This project is licensed under the GNU General Public License. See the [LICENSE.md](LICENSE.md) file for details.
