import sys
from datetime import datetime, timedelta

TIME_COL = 0

#counter class that is given a file, seconds, and price as parameters
class Counter:
    def __init__(self, filename, seconds_for_favorable, price_for_favorable):
        self.filename = filename
        self.seconds_for_favorable = seconds_for_favorable
        self.price_for_favorable = price_for_favorable
        self.have_order = False
        self.isBuy = False
        self.price = 0.000
        self.order_time = datetime.now()
        self.order_pos = -1
        self.favorable = 0
        self.not_favorable = 0
        self.time_list = []
        self.order_restart = 0
        # 09:54:14.893877 | 1357428480 | IN | AMOrderMgr::sendOrder() - sell 7 NG1Q @ 3.79300000, prem = 3.79375000, thd = 0.00000000, uly = 3.79375000(PREPARED=725)
        # 09:54:14.894421|1357428480|IN|ETToolSkeeter::process_tick: Ticker=3.793000000 NG Toes=0.00
    # start method runs the search_for_favorable and get_order_details method to count the number of favorable and
    # non favorable events, as well as how many times there was a new sendOrder in a given time

    def start(self):
        try:
            filer = open(self.filename, "r")
        except OSError as err:
            print("Unable to open File '", self.filename, "'. OS error: {0}".format(err))
            return -1
        except:
            print("Unable to open File '", self.filename, "'")
            return -1
        for line in filer:
            if self.have_order:
                self.search_for_favorable(line)
                continue

            self.order_pos = line.find("sendOrder()")
            if self.order_pos > -1:
                self.get_order_details(line, self.order_pos)
                self.have_order = True
                continue
    # search_for_favorable method finds if a sendOrder price has become favorable or not favorable within a given time,
    # or if there was a new sendOrder in a given time. If the tick is within the timeframe, if the price is lower than
    # the sendOrder price for a buy or higher for a sell, then the counter adds a favorable event happening. If this
    # does not happen in the timeframe, then the counter for a not favorable event goes up

    def search_for_favorable(self, line):
        splitter = line.split('|')
        temp_time = datetime.strptime(splitter[TIME_COL][0:8], '%H:%M:%S')
        tick_pos = line.find("process_tick:")
        temp_order_pos = line.find("sendOrder()")
        if temp_time >= self.order_time + timedelta(seconds=self.seconds_for_favorable):
            self.not_favorable += 1
            self.have_order = False
            return
        elif tick_pos > -1:
            ticker_pos = line.find("Ticker=", tick_pos)
            tick_price = float(line[ticker_pos + 7:ticker_pos + 12])
            if self.isBuy:
                if tick_price <= self.price - self.price_for_favorable:
                    self.favorable += 1
                    self.time_list.append(temp_time)
                    self.have_order = False
            elif not self.isBuy:
                if tick_price >= self.price + self.price_for_favorable:
                    self.favorable += 1
                    self.time_list.append(temp_time)
                    self.have_order = False
        elif temp_order_pos > -1:
            self.get_order_details(line, temp_order_pos)
            self.order_restart += 1
            return
    # the get_order_details method is given a line and a position in the line as a parameter and searches and saves
    # values from the line for the Counter class variables.

    def get_order_details(self, line, order_pos):
        splitter = line.split('|')
        self.order_time = datetime.strptime(splitter[TIME_COL][0:8], '%H:%M:%S')
        order_type_pos = line.find("buy", order_pos)
        if order_type_pos > -1:
            self.isBuy = True
        else:
            self.isBuy = False
        amp_pos = line.find("@")
        self.price = float(line[amp_pos + 2:amp_pos + 7])
        print("order time = ", self.order_time, ". price = ", self.price)

    def getFavorable(self):
        return self.favorable

    def getNotFavorable(self):
        return self.not_favorable

    def getFavorableTimeList(self):
        return self.time_list

    def getRestartCounter(self):
        return self.order_restart

def format_output(time_list):
    for x in time_list:
        print(x)


def main():
    # get variables
    # seconds_for_favorable = how many can seconds pass
    # price_for_favorable = price movement threshold
    if len(sys.argv) < 3:
        print("Usage: ", sys.argv[0], " Filename, seconds for favorable, price for favorable")
        exit(-1)
    filename = sys.argv[1]
    seconds_for_favorable = sys.argv[2]
    price_for_favorable = sys.argv[3]
    counterClass = Counter(filename, int(seconds_for_favorable), float(price_for_favorable))
    counterClass.start()
    num_favorable = counterClass.getFavorable()
    num_not_favorable = counterClass.getNotFavorable()
    time_list = counterClass.getFavorableTimeList()
    restart = counterClass.getRestartCounter()
    print(num_favorable, "/", num_not_favorable, "/", restart)
    # format_output(time_list)


if __name__ == "__main__":
    main()
