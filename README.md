## InvestApp
Investment app for better understanding your success in this sphere

# Main window
![image](https://user-images.githubusercontent.com/55857711/132039805-6e02c718-be08-47a7-9594-f98d2d5ee5a4.png)

# Main features
Via this app you can get information about your income from buyed shares in rubles. 
This app uses Tinkoff API to connect to your investment portfolio. [Get Tinkoff API token - official website](https://www.tinkoff.ru/invest/settings/)

After that app collects info about any existing in your portfolio stock. 
It grabs the following info:
1. Stock name (you need to type it manually)
2. Real share cost - the last price from Tinkoff
3. Amount of shares that you bought
4. Average cost of share

So the whole information is collected with API.
And you can calculate the total income from any available stock in rubles. 
Also you can measure a possible income from shares by changing real stock cost parameter. 

# How to build this app?

- If you want to convert .ui file from QT Designer to .py file:
```
  pyuic5 InvestApp.ui -o InvestApp.py
```
- If you want to convert .py file to standalone executable (.exe):
```
  pip install auto-py-to-exe
  auto-py-to-exe
```
  In this app you will need to specify script location, some icons and images if you have them and after that you can convert your application to .exe file
  
# Thanks for time!



