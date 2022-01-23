# -*- coding: utf-8 -*-

class AssetPortfolio(object):
    
    def __init__( self, *args, **kwargs ):

        self.portfolio = list()
    
    def add( self, stock ):

        self.portfolio.append(stock)
        
    def value(self):

        value = 0        

        for item in self.portfolio:
                
            value += item.value
            
        return value
    
    def consolidate( self ):
        raise Exception("NotImplementedException")
    