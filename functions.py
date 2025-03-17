import requests as rq # For site requests
import os # To clean console
import time as t # To sleep function
from config import API_KEY # Import API key

def clearConsole():
    os.system('cls')

def mainMenu():
    print('Select the operation you want to perform:')
    print('1 - compare exchange rates 1 to 1') 
    print('2 - convert all rates to one')
    print('3 - convert all main rates to one')
    print('4 - Convert an amount from one currency to another')
    choise = input('Your choise: ')
    if choise == '1':
        currencyName = EnterNameTwoCurrencies()
        CompareCourseToCourse(currencyName)
    elif choise == '2':
        currencyName = setAndGetNameOneCurrency()
        AllCurrenciesRelativeTo(currencyName)
    elif choise == '3':
        currencyName = setAndGetNameOneCurrency()
        getExchangeRatesMajorCurrencies(currencyName)
    elif choise == '4':
        currencyCalculator()
    else:
        print('Incorrect input! Try again!'), t.sleep(4), clearConsole(), mainMenu() 

def setAndGetNameOneCurrency():
    nameOfCurrency = input('Enter name of currency: ')
    nameOfCurrency = nameOfCurrency.upper().strip() # Convert the name to capital letters to avoid errors and remove spaces
    return nameOfCurrency

def AllCurrenciesRelativeTo(currency):
    BASE_URL = 'https://v6.exchangerate-api.com/v6/'
    url = f'{BASE_URL}{API_KEY}/latest/{currency}'
    response = rq.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['conversion_rates']
    else:
        print("Error:", response.status_code, response.json())
        return None

def getExchangeRatesMajorCurrencies(currency):
    url = f"https://open.er-api.com/v6/latest/{currency}"
    response = rq.get(url)

    if response.status_code != 200:
        print(f"Error while receiving data: {response.status_code}")
        return

    data = response.json()
    main_currencies = ['USD', 'EUR', 'JPY', 'GBP', 'CHF', 'AUD', 'CAD', 'SGD']

    print(f'Exchange rates relative to {currency}:')
    for currencyName in main_currencies:
        if currencyName in data['rates']:
            rate = data['rates'][currencyName]
            print(f'1 {currency} = {rate:.4f} {currencyName}')
        else:
            print(f'Rate {currencyName} is not available.')
    
    pressEnter = input('\nPress Enter to go to the main menu '), clearConsole, mainMenu() 

def currencyCalculator():
    currencyOne = input('Enter the currency you will be transferring from: ')
    currencyTwo = input('Enter the currency you will be converting to: ')
    currencyOne = currencyOne.upper().strip() # Convert the name to capital letters to avoid errors and remove spaces
    currencyTwo = currencyTwo.upper().strip() # Convert the name to capital letters to avoid errors and remove spaces

    successfulCompletion = False
    difference = 0

    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currencyOne}'
    response = rq.get(url)
    data = response.json()
    if data['result'] == 'success':
        if currencyOne in data['conversion_rates'] and currencyTwo in data['conversion_rates']:
            rate = data['conversion_rates'][currencyTwo]
            successfulCompletion = True
            difference = rate
        else:
            print(f"Incorrect currency name, please check if you have made a typo. Your input: '{currencyOne}'/'{currencyTwo}'."), t.sleep(5), currencyCalculator()
    else:
        print(f"Error! Perhaps you entered the currency name incorrectly. Your input: '{currencyOne}'/'{currencyTwo}'"), t.sleep(5), currencyCalculator()

    if successfulCompletion == True:
        try:
            ammount = int(input(f'Enter the amount of {currencyOne}: '))
            ammount = ammount * difference
            ammount = str(ammount)[:4]
            print(f'Summ in {currencyTwo}: {ammount}')
            successfulCompletion = False
            pressEnter = input('\nPress Enter to go to the main menu '), clearConsole, mainMenu() 
        except ValueError:
            print('Incorrect input! Try again!'), t.sleep(4), clearConsole(), currencyCalculator()
    else:
        pass

def EnterNameTwoCurrencies():
    currencyOne = input('Enter the currency by which we will determine the rate: ')
    currencyTwo = input('Enter the currency whose rate you want to check: ')
    currencyOne = currencyOne.upper().strip() # Convert the name to capital letters to avoid errors and remove spaces
    currencyTwo = currencyTwo.upper().strip() # Convert the name to capital letters to avoid errors and remove spaces

    difference = CompareCourseToCourse(currencyOne, currencyTwo)


    pressEnter = input('\nPress Enter to go to the main menu '), clearConsole, mainMenu() 
def CompareCourseToCourse(currencyOne, currencyTwo):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currencyOne}'
    response = rq.get(url)
    data = response.json()
    
    if data['result'] == 'success':
        if currencyOne in data['conversion_rates'] and currencyTwo in data['conversion_rates']:
            rate = data['conversion_rates'][currencyTwo]
            print(f'{currencyTwo} to {currencyOne} exchange rate: {rate}')
        else:
            print(f"Incorrect currency name, please check if you have made a typo. Your input: '{currencyOne}'/'{currencyTwo}'."), t.sleep(5), EnterNameTwoCurrencies()
    else:
        print(f"Error! Perhaps you entered the currency name incorrectly. Your input: '{currencyOne}'/'{currencyTwo}'"), t.sleep(5), EnterNameTwoCurrencies()
