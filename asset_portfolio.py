# -*- coding: utf-8 -*-

class AssetPortfolio(object):
    
    def __init__( self, *args, **kwargs ):
        
        self.portfolio = list()
    
    def add( self, stock ):
        
        self.portfolio.append(stock)
        
    def value( self ):
        
        v = 0        

        for s in self.portfolio:
                
            v += s.value
            
        return v
    
    def consolidate( self ):
        raise Exception("NotImplementedException")
    