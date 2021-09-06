## InvestApp
Investment app for better understanding your success in this sphere

# Main window
![image](https://user-images.githubusercontent.com/55857711/132236762-13621dac-d2fd-4506-818d-b736690aece5.png)

# Main features
Via this app you can get information about your income from buyed shares in rubles. 
This app uses Tinkoff API to connect to your investment portfolio. [Get Tinkoff API token - official website](https://www.tinkoff.ru/invest/settings/)

After that app collects info about any existing in your portfolio stock. 
It grabs the following info:
1. Stock name (you need to type it manually)
2. Real share cost - the last price from Tinkoff
3. Amount of shares that you bought
4. Average cost of share

So the whole information is collected via API.
And you can calculate the total income from any available stock in rubles. 
Also you can measure a possible income from shares by changing real stock cost parameter. 

# Main features
1. Uses Tinkoff API Token
2. Capable of importing / exporting API Token
3. Capable of encrypting / decrypting the API Token file for secure using

# How to build this app?

- Convert design file from QT Designer (.ui file) to python .py file:
```
  pyuic5 InvestApp.ui -o InvestApp.py
```
- Build executable (.exe) file from main.py:
```
  pip install auto-py-to-exe
  auto-py-to-exe
```
  In this app you will need to specify main.py script location, some icons and images if you have them and after that you can convert your application to .exe file
  
# Thanks for time!



