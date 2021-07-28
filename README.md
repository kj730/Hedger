# Hedger
The hedger.py code searches through a given file and returns the amount of times 3 events occur, as well as the times of the events.
The program looks for a hedge order and saves the values associated with that line. The program then looks for spots, or average futures prices, within a given timeframe.
If there is a spot, then it compares the hedge order price with the spot price. Depending on if the hedge order is a buy or sell, the program checks to see if the spot price is higher or lower by a given amount.
If it is lower for a buy or higher for a sell within the timeframe, then a counter for a favorable event goes up by one, and the time of that event is saved.
If there is a hedge order and there is not a favorable event within the timeframe, then the counter for a non favorable event goes up.
If there is another hedge order within the timeframe, then the program updates its values for the new hedge order
The .idea contains PyCharm files for the Hedger repository
