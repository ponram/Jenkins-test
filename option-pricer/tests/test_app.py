import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from option_pricer.app import OptionPricer
import QuantLib as ql

class TestOptionPricer:
    
    def setup_method(self):
        """Set up test fixtures"""
        self.pricer = OptionPricer(
            spot_price=100.0,
            strike_price=105.0,
            risk_free_rate=0.05,
            volatility=0.20,
            dividend_yield=0.02
        )
        self.test_date = "2026-12-30"  # Using a future date
    
    def test_option_pricer_initialization(self):
        """Test OptionPricer initialization"""
        assert self.pricer.spot_price == 100.0
        assert self.pricer.strike_price == 105.0
        assert self.pricer.risk_free_rate == 0.05
        assert self.pricer.volatility == 0.20
        assert self.pricer.dividend_yield == 0.02
    
    def test_call_option_pricing(self):
        """Test call option pricing"""
        result = self.pricer.price_european_option(self.test_date, "call")
        
        assert "price" in result
        assert "delta" in result
        assert "gamma" in result
        assert "theta" in result
        assert "vega" in result
        assert "rho" in result
        
        # Basic sanity checks
        assert result["price"] > 0
        assert 0 <= result["delta"] <= 1  # Call delta should be positive
        assert result["gamma"] >= 0
        assert result["vega"] > 0
    
    def test_put_option_pricing(self):
        """Test put option pricing"""
        result = self.pricer.price_european_option(self.test_date, "put")
        
        assert result["price"] > 0
        assert -1 <= result["delta"] <= 0  # Put delta should be negative
        assert result["gamma"] >= 0
    
    def test_option_pricing_edge_cases(self):
        """Test edge cases"""
        # Test with zero volatility
        zero_vol_pricer = OptionPricer(100, 100, 0.05, 0.0)
        result = zero_vol_pricer.price_european_option(self.test_date, "call")
        assert result["price"] >= 0
    
    @pytest.mark.parametrize("option_type", ["call", "put", "CALL", "PUT"])
    def test_option_type_handling(self, option_type):
        """Test different option type inputs"""
        result = self.pricer.price_european_option(self.test_date, option_type)
        assert result["price"] > 0
