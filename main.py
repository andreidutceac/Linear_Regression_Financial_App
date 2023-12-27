import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import matplotlib.pyplot as plt
import numpy as np
from kivy.uix.image import Image
from sklearn.linear_model import LinearRegression
import numpy as np
period_type = 'days'

def init_db():
    conn = sqlite3.connect('financial_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS financial_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value INTEGER
        )
    ''')

    # Check if the table is empty
    c.execute('SELECT COUNT(*) FROM financial_data')
    count = c.fetchone()[0]
    if count == 0:
        # Table is empty, initialize the values
        x_money, y_time = get_setting()
#        init_db_rows(y_time)

    conn.commit()
    conn.close()

def init_db_rows(time_input_value):
    conn = sqlite3.connect('financial_data.db')
    c = conn.cursor()

    # Convert the time_input text to integer
    try:
        time_input_int = int(time_input_value)
    except ValueError:
        # Handle invalid input, maybe set a default or raise an error
        time_input_int = 0


    conn.commit()
    conn.close()


def update_db(period_index, value):
    conn = sqlite3.connect('financial_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO financial_data (id, value) VALUES (?, ?)
        ON CONFLICT(id) DO UPDATE SET value = excluded.value
    ''', (period_index, value))
    conn.commit()
    conn.close()



def fetch_from_db():
    conn = sqlite3.connect('financial_data.db')
    c = conn.cursor()
    c.execute('SELECT id, value FROM financial_data ORDER BY id')
    data = c.fetchall()
    conn.close()
    return data


def reset_db():
    conn = sqlite3.connect('financial_data.db')
    c = conn.cursor()

    # Drop the existing table
    c.execute('DROP TABLE IF EXISTS financial_data')

    # Recreate the table
    c.execute('''
        CREATE TABLE financial_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def init_settings_db():
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings_data (
            id INTEGER PRIMARY KEY,
            value INTEGER,
            period INTEGER
        )
    ''')
    # Insert initial values with id = 1
    c.execute('''
           INSERT OR IGNORE INTO settings_data (id, value, period) VALUES (1, 0, 0)
       ''')
    conn.commit()
    conn.close()

def get_setting():
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    c.execute('SELECT value, period FROM settings_data WHERE id = 1')
    result = c.fetchone()
    conn.close()
    return result if result else (0, 0)

def save_setting(value, period):
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    # Update the first row with id = 1
    c.execute('''
        INSERT INTO settings_data (id, value, period) VALUES (1, ?, ?)
        ON CONFLICT(id) DO UPDATE SET value = excluded.value, period = excluded.period
    ''', (value, period))
    conn.commit()
    conn.close()



# Page 1: Welcome Screen
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        greeting = Label(text="Hi! Welcome to the Financial Planner!")
        next_button = Button(text="Go to Planner", size=(200, 100))
        next_button.bind(on_press=self.go_to_planner)
        layout.add_widget(greeting)
        layout.add_widget(next_button)
        self.add_widget(layout)

    def go_to_planner(self, instance):
        self.manager.current = 'form_screen'

# Page 2: Form Screen
class FormScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text="How much money do you want to save?"))
        self.money_input = TextInput(multiline=False)
        layout.add_widget(self.money_input)
        layout.add_widget(Label(text="Period of time:"))
        self.period_spinner = Spinner(text='Days', values=('Days', 'Weeks'))
        layout.add_widget(self.period_spinner)
        self.period_spinner.bind(text=self.on_spinner_select)
        self.time_input = TextInput(multiline=False, input_filter='int')
        layout.add_widget(self.time_input)
        save_button = Button(text="Save and Next")
        save_button.bind(on_press=self.save_data)
        layout.add_widget(save_button)
        self.add_widget(layout)
        print(self.time_input.text)
        self.period_type = 'days'

        x_money, y_time = get_setting()
        init_db_rows(y_time)

    def on_spinner_select(self, spinner, text):
        # Save the selected value or perform an action
        print(f"Selected value: {text}")  # Example action
        period_type = text

    def save_data(self, instance):
        x_money = int(self.money_input.text)
        y_time = int(self.time_input.text)
        save_setting(x_money, y_time)  # Save settings to the database
        self.manager.current = 'table_screen'

class TableScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.temp_values = {}
        self.val = 0
        main_layout = BoxLayout(orientation='vertical', spacing=10)

        self.save_input = TextInput(hint_text='How much saving?', input_filter='int')
        main_layout.add_widget(self.save_input)

        submit_button = Button(text='Submit', on_press=self.submit_form, height=50)
        main_layout.add_widget(submit_button)

        button_layout = BoxLayout(size_hint_y=None, height=50)
        reset_button = Button(text="Reset Values")
        reset_button.bind(on_press=self.reset_values)
        next_button = Button(text="Next Page")
        next_button.bind(on_press=self.go_to_additional_screen)
        button_layout.add_widget(reset_button)
        button_layout.add_widget(next_button)
        main_layout.add_widget(button_layout)

        self.add_widget(main_layout)

    def submit_form(self, instance):
        save = int(self.save_input.text)

        conn = sqlite3.connect('financial_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO financial_data (value) VALUES (?)", (save,))
        conn.commit()
        conn.close()

        print("Data submitted")





    def on_enter(self, *args):

        data = fetch_from_db()  # Fetch existing data from the database

        for period_index in range(30):
            label = Label(text=f"{period_index} Days")  # Label showing the day
            input_field = TextInput(text=str(0), multiline=False)  # TextInput with the current value
           # input_field.bind(on_text_validate=self.on_text_input)
            input_field.period_index = period_index  # Store the period index in the TextInput for later reference




    def reset_values(self, instance):
        reset_db()  # Reset values in the financial data database
        save_setting(0, 0)  # Reset values in the settings database
        self.on_enter()  # Refresh the table
        self.manager.current = 'welcome_screen'  # Navigate to the welcome screen


    def go_to_additional_screen(self, instance):
        for period_index, value in self.temp_values.items():
            update_db(period_index, value)
            print(self.value)
        self.manager.current = 'additional_screen'
        data = fetch_from_db()
        index = []

        for id, value in data:
            index.append(id)

        cum_sum = np.cumsum([value for _, value in data])
        print(cum_sum)

        # Reshaping data - scikit-learn expects a 2D array for the features
        X = np.array(index).reshape(-1, 1)
        y = np.array(cum_sum)





def create_and_save_plot(data, file_name='plot.png'):
    x = range(1, len(data) + 1)
    y = data  # Use the data directly passed to the function
    fig, ax = plt.subplots()
    ax.bar(x, y, color='orange')
    ax.set_title('Financial Data Plot')
    ax.set_xlabel('ID')
    ax.set_ylabel('Value')
    plt.savefig(file_name)
    plt.close(fig)

class ChartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.chart_layout = BoxLayout(orientation='vertical')  # Layout for the chart
        self.chart_layout2 = BoxLayout(orientation='vertical')  # Layout for the chart
        self.add_back_button()
        self.layout.add_widget(self.chart_layout)
        self.layout.add_widget(self.chart_layout2)
        inputs = get_setting()
        self.period = str(inputs[1])
        self.prediction = ''

        self.result_label = Label(text='Your prediction sum after' + (self.period) + 'is: ' + (self.prediction),
                                  size_hint=(None, None),
                                  size=(200, 100),
                                  padding=(20, 20),
                                  halign='center',
                                  valign='middle',
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5}
                                  )  # Padding for the label

        # Add the label to the layout
        self.layout.add_widget(self.result_label)

        self.add_widget(self.layout)
        self.display_plot()
        self.display_plot2()

    def add_back_button(self):
        back_button = Button(text="Back to Page 3", size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)  # Assuming you have a go_back method
        self.layout.add_widget(back_button)

    def display_plot(self):
        # Reopen the database and fetch data
        conn = sqlite3.connect('financial_data.db')
        c = conn.cursor()
        c.execute('SELECT id, value FROM financial_data ORDER BY id')
        data = [value for _, value in c.fetchall()]
        conn.close()

        # Create and save the plot
        create_and_save_plot(data, 'plot.png')

        # Update the chart layout
        self.chart_layout.clear_widgets()  # Clear only the chart layout
        self.chart_layout.add_widget(Image(source='plot.png'))

    def display_plot2(self):
        # Open the database and fetch data
        conn = sqlite3.connect('financial_data.db')
        c = conn.cursor()
        c.execute('SELECT id, value FROM financial_data ORDER BY id')
        data = c.fetchall()
        conn.close()

        # Calculate the cumulative sum
        cum_sum = np.cumsum([value for _, value in data])
        print(cum_sum)

        # Create and save the plot
        self.create_and_display_plot2(cum_sum)

        # apply linear regression
        index = []

        for id, value in data:
            index.append(id)

        cum_sum = np.cumsum([value for _, value in data])
        print(cum_sum)

        if len(index) > 0:
            # Reshaping data - scikit-learn expects a 2D array for the features
            X = np.array(index).reshape(-1, 1)
            y = np.array(cum_sum)

            # Create a linear regression model
            model = LinearRegression()

            # Fit the model
            model.fit(X, y)

            slope = model.coef_[0]
            intercept = model.intercept_

            period = get_setting()

            # Make predictions (optional)
            self.prediction = int(slope * period[1] + intercept)
            print(self.period)
            print(self.prediction)
            self.result_label.text = f'Your prediction sum after {self.period} {period_type} is: {self.prediction} $'
            print("Predictions:", self.prediction)

    def create_and_display_plot2(self, cum_sum_data):
        fig, ax = plt.subplots()
        ax.plot(range(1, len(cum_sum_data) + 1), cum_sum_data, color='blue', marker='o')
        ax.set_title('Cumulative Sum of Values')
        ax.set_xlabel('ID')
        ax.set_ylabel('Cumulative Sum')
        plt.savefig('cumulative_plot.png')
        plt.close(fig)

        # Update the chart layout
        self.chart_layout2.clear_widgets()
        self.chart_layout2.add_widget(Image(source='cumulative_plot.png'))


    def go_back(self, instance):
        # Implement the logic to go back to the previous screen
        self.manager.current = 'table_screen'  # Replace with your actual screen name


class FinancialApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome_screen'))
        sm.add_widget(FormScreen(name='form_screen'))
        sm.add_widget(TableScreen(name='table_screen'))
        sm.add_widget(ChartScreen(name='additional_screen'))
        x_money, y_time = get_setting()

        if x_money > 0 and y_time > 0:
            sm.add_widget(TableScreen(name='table_screen'))
            sm.current = 'table_screen'
        else:
            sm.add_widget(WelcomeScreen(name='welcome_screen'))
            sm.current = 'welcome_screen'

        # ... add other screens
        return sm

if __name__ == '__main__':
    init_settings_db()
    init_db()
    FinancialApp().run()
