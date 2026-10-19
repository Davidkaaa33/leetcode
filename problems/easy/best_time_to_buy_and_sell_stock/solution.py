class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        max_profit = 0
        min_price = prices[0]
        n = len(prices)
        for i in range(n):
            min_price = min(min_price, prices[i])
            max_profit = max(max_profit, prices[i] - min_price)
        return max_profit