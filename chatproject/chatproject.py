import pandas as pd
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, ttk


class WhatsAppAnalysisGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("WhatsApp Chat Analysis")
        self.geometry("800x600")
        self.file_path_var = tk.StringVar()
        ttk.Label(self, text="WhatsApp Chat File:").pack(pady=5)
        ttk.Entry(self, textvariable=self.file_path_var,
                  width=50).pack(pady=10)
        ttk.Button(self, text="Browse", command=self.load_file).pack(pady=5)

        ttk.Label(self, text="Conversation Initiation Threshold (minutes):").pack(
            pady=5)
        self.initiation_threshold = tk.IntVar(value=120)
        ttk.Entry(self, textvariable=self.initiation_threshold,
                  width=5).pack(pady=5)

        ttk.Label(self, text="Consecutive Messages Threshold:").pack(pady=5)
        self.consecutive_messages_threshold = tk.IntVar(value=4)
        ttk.Entry(self, textvariable=self.consecutive_messages_threshold,
                  width=5).pack(pady=5)

        ttk.Label(
            self, text="Time Threshold for Back-and-Forth (minutes):").pack(pady=5)
        self.time_threshold_minutes = tk.IntVar(value=5)
        ttk.Entry(self, textvariable=self.time_threshold_minutes,
                  width=10).pack(pady=5)

        ttk.Button(self, text="Analyze", command=self.analyze).pack(pady=5)

        self.results_text = tk.Text(self, width=60, height=10)
        self.results_text.pack(pady=5)
        self.results_text.insert(
            tk.END, "Analysis results will appear here...")

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select WhatsApp Chat File", filetypes=[("Text files", "*.txt")])
        self.file_path_var.set(file_path)

    def analyze(self):
        file_path = self.file_path_var.get()
        chat = import_chat(file_path)

        parsed_data = [parse_line(line) for line in chat if parse_line(line)]
        df = pd.DataFrame(parsed_data, columns=[
                          'Date', 'Time', 'Sender', 'Message'])

        self.results_text.delete("1.0", tk.END)

        message_counts = analyze_frequency(df)
        self.results_text.insert(
            tk.END, "Nachrichtenzählung:\n" + str(message_counts) + "\n\n")

        response_times = analyze_response_time(df)
        self.results_text.insert(
            tk.END, "Durchschnittliche Antwortzeit (in Minuten):\n" + str(response_times) + "\n\n")

        initiators = analyze_conversation_initiators(
            df, self.initiation_threshold.get())
        self.results_text.insert(
            tk.END, "Gesprächsinitiatoren:\n" + str(initiators) + "\n\n")

        response_times_adjusted = analyze_response_time_outside_back_and_forth(
            df, self.consecutive_messages_threshold.get(), self.time_threshold_minutes.get())
        self.results_text.insert(
            tk.END, "Durchschnittliche Antwortzeit (außerhalb des Hin-und-Her-Schreibens, in Minuten):\n" + str(response_times_adjusted) + "\n\n")
        
        plot_frame = tk.Frame(self)
        plot_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        plots = plot_results(message_counts, response_times, initiators, response_times_adjusted, plot_frame)


def import_chat(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        chat = file.readlines()
    return chat


def parse_line(line):
    pattern = r"\[(\d{2}\.\d{2}\.\d{2}), (\d{2}:\d{2}:\d{2})\] ([^:]+): (.+)"
    match = re.match(pattern, line)
    if match:
        date, time, sender, message = match.groups()
        return date, time, sender, message
    return None


def analyze_conversation_initiators(df, threshold_minutes=120):
    df['Datetime'] = pd.to_datetime(
        df['Date'] + ' ' + df['Time'], format='%d.%m.%y %H:%M:%S')
    df['Time_Diff'] = df['Datetime'].diff().dt.total_seconds() / \
        60  # in Minuten

    initiators = df[(df['Time_Diff'] > threshold_minutes) &
                    (df['Sender'] != df['Sender'].shift())]['Sender'].value_counts()
    return initiators


def analyze_frequency(df):
    return df['Sender'].value_counts()


def analyze_response_time(df):
    df['Datetime'] = pd.to_datetime(
        df['Date'] + ' ' + df['Time'], format='%d.%m.%y %H:%M:%S')
    df['Time_Diff'] = df['Datetime'].diff().where(
        df['Sender'] == df['Sender'].shift(-1))
    response_times = df.groupby('Sender')['Time_Diff'].mean(
    ).dt.total_seconds() / 60  # in Minuten
    return response_times


def analyze_response_time_outside_back_and_forth(df, consecutive_messages_threshold=4, time_threshold_minutes=5):
    df['Datetime'] = pd.to_datetime(
        df['Date'] + ' ' + df['Time'], format='%d.%m.%y %H:%M:%S')
    df['Time_Diff'] = df['Datetime'].diff().dt.total_seconds() / \
        60
    df['Back_and_Forth'] = (df['Time_Diff'] <= time_threshold_minutes)
    df['BnF_Sum'] = df['Back_and_Forth'][::-
                                         1].groupby(df['Sender']).cumsum()[::-1]

    mask = df['BnF_Sum'] < consecutive_messages_threshold
    filtered_df = df[mask].copy()

    response_times_adjusted = filtered_df.groupby('Sender')['Time_Diff'].mean()
    return response_times_adjusted

def plot_results(message_counts, response_times, initiators, response_times_adjusted, plot_frame):
    # create the plots
    fig, axs = plt.subplots(2,2, figsize=(4,4))
    axs[0, 0].bar(message_counts.index, message_counts.values)
    axs[0, 0].set_title('Nachrichten')
    axs[0, 1].bar(response_times.index, response_times.values)
    axs[0, 1].set_title('Antwortzeit')
    axs[1, 0].bar(initiators.index, initiators.values)
    axs[1, 0].set_title('Initiatoren')
    axs[1, 1].bar(response_times_adjusted.index, response_times_adjusted.values)
    axs[1, 1].set_title('Antwortzeit angepasst')

    # create a canvas for each plot and add it to the frame
    canvas1 = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # return the plots
    return fig

if __name__ == "__main__":
    app = WhatsAppAnalysisGUI()
    app.mainloop()
