
import openpyxl
import pprint as pp

# https://www.youtube.com/watch?v=ibXT3SbfkOc&list=WL&index=59
# from 35:00 onwards

class DataLayer():

    def __init__(self):
        self.filename = "BDEAllocationSheet.xlsx"
        self.is_loaded = False
        self.load_data()

    def load_data(self):
        if not self.is_loaded: # just bascially load it once
            self.book = openpyxl.load_workbook(self.filename)
            self.shFSP = self.book["FSPAlloc"]
            self.shIFA = self.book["IFAlloc"]
            self.is_loaded = True

    def get_data(self):
        self.load_data()
        data = []
        for row in self.shFSP.iter_rows(min_row=2, values_only=True):
            data.append(row)
        return data

data = DataLayer()
pp.pprint(data.get_data())