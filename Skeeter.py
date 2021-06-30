import sys
from datetime import datetime, timedelta
TIME_COL = 0


class Counter:
    m_have_order = False
    isBuy = False
    price = 0.000
    order_time = datetime.datetime
    order_pos = -1

    def _init_(self, filename, seconds_for_favorable, price_for_favorable):
        self.filename = filename
        self.seconds_for_favorable = seconds_for_favorable
        self.price_for_favorable = price_for_favorable
        m_have_order = False
        #09:54:14.893877 | 1357428480 | IN | AMOrderMgr::sendOrder() - sell 7 NG1Q @ 3.79300000, prem = 3.79375000, thd = 0.00000000, uly = 3.79375000(PREPARED=725)
        #09:54:14.894421|1357428480|IN|ETToolSkeeter::process_tick: Ticker=3.793000000 NG Toes=0.00
        def start():
            try:
                filer = open(filename, "r")
            except OSError as err:
                print("Unable to open File. OS error: {0}".format(err))
                return -1
            except:
                print("Unable to open File")
                return -1
            for line in filer:
                if m_have_order:
                    search_for_favorable(line)
                    continue

                order_pos = line.find("sendOrder()")
                if order_pos > -1:
                    get_order_details(line, order_pos)
                    continue

        def search_for_favorable(line):
            tick_pos = line.find("process_tick:")
            if tick_pos > -1:
                ticker_pos = line.find("Ticker=", tick_pos)
        # Is this another send order? If so then call get_send_order_details()
            #Has enough time passed?

        def get_order_details(line, order_pos):
            splitter = line.split('|')
            order_time = datetime.datetime.strptime(splitter[TIME_COL][0:8], '%H:%M:%S')
            order_type_pos = line.find("buy", order_pos)
            if order_type_pos != -1:
                isBuy = True
            else:
                isBuy = False
            amp_pos = line.find("@")
            price = float(line[amp_pos + 2:amp_pos + 7])

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
    counterClass = Counter(filename, seconds_for_favorable, price_for_favorable)
    counterClass.start()
    num_favorable = counterClass.getFavorable()
    num_not_favorable = counterClass.getNotFavorable()
    time_list = counterClass.getFavorableTimeList()
if __name__ == "__main__":
    main()

