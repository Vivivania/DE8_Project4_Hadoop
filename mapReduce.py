#!python3

from optparse import Values
from mrjob.job import MRJob
from mrjob.step import MRStep

import csv
import json

cols = 'order_id,order_date,user_id,payment_name,shipper_name,order_price,order_discount,voucher_name,voucher_price,order_total,rating_status'.split(',')

def csv_readline(line):
    """Given a sting CSV line, return a list of strings."""
    for row in csv.reader([line]):
        return row

class OrderDateCount(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.sort)
        ]

    def mapper(self, _, line):
        # Convert each line into a dictionary
        row = dict(zip(cols, csv_readline(line)))

        #skip first row as header
        if row['order_id'] != 'order_id':
            # Yield the order_date
            yield row['order_date'][0:7], 1

    def reducer(self, key, values):
        #for 'order_date' compute
        yield None, (key,sum(values))
    
    def sort(self, key, values):
        data = []
        for order_date, order_count in values:
            data.append((order_date, order_count))
            data.sort()

        for order_date, order_count in data:
           yield order_date, order_count


#Order Total Per Month
    def mapper_order_total(self, order_date, order_total):
        yield int(order_total), order_date

    def reducer_OrderTotal_per_Month(self, order_total, order_date):
        for order_date in order_date:
            yield order_date, order_total


if __name__ == '__main__':
    OrderDateCount.run()