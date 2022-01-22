# -*- coding: utf-8 -*-

class Stock(object):
    
    def __init__( self, symbol:str, shares:float, price:float ):
        
        self.symbol = symbol
        self.shares = shares
        self.price = price
                
    @property
    def value( self ):
        return self.shares * self.price