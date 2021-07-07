# Skeeter
The skeeter.py code searches through a given file and returns the amount of times 3 events occur, as well as the times of the events.
The program looks for the string "sendOrder' and saves the values associated with that line. the program then looks for ticks within a given timeframe.
If there is a tick, then it compares the sendOrder price with the tick price. Depending on if the sendOrder is a buy or sell, the program checks to see if the tick price is higher or lower by a given amount.
If it is lower for a buy or higher for a sell within the timeframe, then a counter for a favorable event goes up by one, and the time of that event is saved.
If there is a sendOrder and there is not a favorable event within the timeframe, then the counter for a non favorable event goes up.
If there is another sendOrder within the timeframe, then the program updates its values for the new sendOrder
The .idea contains PyCharm files for the Skeeter repository
