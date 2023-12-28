# Linear_Regression_Financial_App
Financial app using kivy and linear regression to predict future savings

This financial software application, crafted using the Python programming language and the Kivy framework, serves as a sophisticated tool aimed at enhancing personal savings and forecasting future financial accumulation. This application is distinctive for its integration of a linear regression machine learning algorithm. Linear regression is employed for its efficiency in analyzing current saving trends and projecting future savings, based on the data entered.


## Key Features
### 1.Machine Learning with Linear Regression:
- Utilized to forecast future savings.
- Analyzes patterns in historical saving data to make predictions.
### 2.Database Integration (SQLite3):
- First Database: Captures the user's financial goal (e.g., saving $1000 over 10 weeks) and the designated time span.
- Second Database: Records the amount saved in each specified period (e.g., weekly savings like $90, $120, $130, $90).

![7](https://github.com/andreidutceac/Linear_Regression_Financial_App/assets/117718437/8cd41817-e506-4628-9bf3-32b35e62cda5) 
![6](https://github.com/andreidutceac/Linear_Regression_Financial_App/assets/117718437/c5a5d1ec-c2df-48c7-9343-b41999a0d5b2)

## Structure of the App
### 1.Initial Welcome Page: 

The first screen that welcomes users.

![1](https://github.com/andreidutceac/Linear_Regression_Financial_App/assets/117718437/aeaabf5f-d957-476f-95ec-a21be7555870)

### 2.Goal Setting Page:

Here, users input their savings objective and the desired timeframe.
For instance, setting a goal to save $1000 in 10 weeks.

![2](https://github.com/andreidutceac/Linear_Regression_Financial_App/assets/117718437/f3f73b95-e579-4ae7-9953-b3887c502d39)

### 3.Saving Input Page:

Users update their savings for each period, which is then stored in the app.
The third page of the app includes a reset feature, allowing users to clear the database content if they decide to begin anew with different values.

![3](https://github.com/andreidutceac/Linear_Regression_Financial_App/assets/117718437/26040cec-797b-4a94-82ff-15129c6cbc32)

### 4.Visualization and Forecasting Page:
- Bar Chart: Shows the savings for each specified period.
- Accumulative Chart: Illustrates the overall savings progression.
- Savings Forecast: Based on linear regression, this feature predicts the total savings at the end of the set period, taking into account current saving habits.

![5](https://github.com/andreidutceac/Linear_Regression_Financial_App/assets/117718437/2e329d96-5f41-4d43-8839-d1cb9d86be72)

### Example Usage

Savings Goal: Accumulate $1000 in 10 weeks, equating to $100 weekly.
Recorded Savings: $90, $120, $130, $90 over the past four weeks.
Predicted Outcome: The app estimates a total saving of $1130 at the end of 10 weeks.
- Example: Predicts saving $1130 in 10 weeks for a $1000 goal.

## Technical Framework
- Development Language: Python.
- User Interface Framework: Kivy.
- Database Management: Using SQLite3.
- Predictive Analysis: Employing linear regression for financial forecasting.

## Advantages for Users
- Financial Management Aid: Helps users in planning and achieving their savings objectives.
- Progress Tracking: Provides graphical representations of savings.
- Future Savings Estimation: Offers predictions on total savings, aiding in financial planning.

This application is an exemplary blend of user-friendly design, efficient data handling, and advanced predictive analysis, making it an indispensable tool for anyone aiming to optimize their savings and financial planning.
