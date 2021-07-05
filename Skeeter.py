import sys
from datetime import datetime, timedelta

TIME_COL = 0


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
        self.temp_favorable = 0
        # 09:54:14.893877 | 1357428480 | IN | AMOrderMgr::sendOrder() - sell 7 NG1Q @ 3.79300000, prem = 3.79375000, thd = 0.00000000, uly = 3.79375000(PREPARED=725)
        # 09:54:14.894421|1357428480|IN|ETToolSkeeter::process_tick: Ticker=3.793000000 NG Toes=0.00

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
                self.temp_favorable = 0
                self.have_order = True
                continue

    def search_for_favorable(self, line):
        splitter = line.split('|')
        temp_time = datetime.strptime(splitter[TIME_COL][0:8], '%H:%M:%S')
        tick_pos = line.find("process_tick:")
        temp_order_pos = line.find("sendOrder()")
        if temp_time >= self.order_time + timedelta(seconds=self.seconds_for_favorable):
            if self.temp_favorable == 0:
                self.not_favorable += 1
                return
        elif tick_pos > -1:
            ticker_pos = line.find("Ticker=", tick_pos)
            tick_price = float(line[ticker_pos + 7:ticker_pos + 12])
            if self.isBuy:
                if tick_price <= self.price - self.price_for_favorable:
                    self.favorable += 1
                    self.temp_favorable += 1
                    self.time_list.append(temp_time)
            elif self.isBuy == False:
                if tick_price >= self.price + self.price_for_favorable:
                    self.favorable += 1
                    self.temp_favorable += 1
                    self.time_list.append(temp_time)
        elif temp_order_pos > -1:
            self.get_order_details(line, temp_order_pos)
            self.temp_favorable = 0
            self.have_order = True
            return

    def get_order_details(self, line, order_pos):
        splitter = line.split('|')
        self.order_time = datetime.strptime(splitter[TIME_COL][0:8], '%H:%M:%S')
        order_type_pos = line.find("buy", order_pos)
        if order_type_pos > -1:
            self.isBuy = True
        else:
            self.isBuy = False
        amp_pos = line.find("@")
        price = float(line[amp_pos + 2:amp_pos + 7])

    def getFavorable(self):
        return self.favorable

    def getNotFavorable(self):
        return self.not_favorable

    def getFavorableTimeList(self):
        return self.time_list


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
    print(num_favorable, "/", num_not_favorable)
    # format_output(time_list)


if __name__ == "__main__":
    main()
