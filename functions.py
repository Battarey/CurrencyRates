import requests as rq # For site requests
import os # To clean console
import time as t # To sleep function
from config import API_KEY # Import API key

def clearConsole():
    os.system('cls')

def mainMenu():
    print('Select the operation you want to perform:')
    print('1 - convert one currency to another')
    print('2 - convert all rates to one')
    choise = input('Your choise: ')
    if choise == '1':
        currencyName = setAndGetNameOneCurrency()
        AllCurrenciesRelativeTo(currencyName)
    elif choise == '2':
        currencyName = setAndGetNameOneCurrency()
        AllCurrenciesRelativeTo(currencyName)
    else:
        print('Incorrect input! Try again!'), t.sleep(4), clearConsole(), mainMenu() 

def setAndGetNameOneCurrency():
    nameOfCurrency = input('Enter name of currency: ')
    nameOfCurrency = nameOfCurrency.upper() # We convert the name to uppercase to avoid making a mistake
    nameOfCurrency = nameOfCurrency.replace(" ", "") # Remove all spaces so that the error doesn't pop up again
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
    
def EnterNameTwoCurrencies():
    currencyOne = input('Enter the currency by which we will determine the rate: ')
    currencyTwo = input('Enter the currency whose rate you want to check: ')
    currencyOne = currencyOne.upper() # We convert the name to uppercase to avoid making a mistake
    currencyTwo = currencyTwo.upper() # We convert the name to uppercase to avoid making a mistake
    currencyOne = currencyOne.replace(" ", "") # Remove all spaces so that the error doesn't pop up again
    currencyTwo = currencyTwo.replace(" ", "") # Remove all spaces so that the error doesn't pop up again
    CompareCourseToCourse(currencyOne, currencyTwo)
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
