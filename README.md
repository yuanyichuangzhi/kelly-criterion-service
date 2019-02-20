Kelly Criterion Service
=======================
Money management strategy based on Kelly J. L.'s formula described in "A New Interpretation of Information Rate" [1]. 
The formula was adopted to gambling and stock market by Ed Thorp, et al., see:
"The Kelly Criterion in Blackjack Sports Betting, and the Stock Market" [2].

This service calculates the optimal capital allocation for the provided portfolio of securities with the formula:

![f_i = m_i / s_i^2](https://latex.codecogs.com/gif.latex?f_i%3Dm_i/s_i%5E2)

where
  * `f_i` is the calculated leverage of the i-th security from the portfolio
  * `m_i` is the mean of the return of the i-th security from the portfolio
  * `s_i` is the standard deviation of the return of the i-th security from the portfolio

assuming that the strategies for the securities are all statistically independent.

The stock quotes are downloaded from IEX Exchange.

Reference (Matlab) implementation was taken from Ernie Chan's Quantitative Trading book [3].

Usage
-----
Hosted version of this service can be found at http://kelly.direct webpage.

Running locally
---------------
Start the application via docker and open the webpage at http://localhost:8080 :
```
 docker run -p 8080:80 --name kelly-criterion-service --rm kellydirect/kelly-criterion-service:latest
```

Dependencies
------------
The leverage calculation of this REST API is provided through kelly_criterion python package. 

References
----------
  * [1]: [A New Interpretation of Information Rate](http://ieeexplore.ieee.org/stamp/stamp.jsp?reload=true&tp=&arnumber=6771227)
  * [2]: [The Kelly Criterion in Blackjack Sports Betting, and the Stock Market](http://www.edwardothorp.com/sitebuildercontent/sitebuilderfiles/beatthemarket.pdf)
  * [3]: [Ernest P. Chan: Quantitative Trading (ISBN 978-0470284889)](http://www.amazon.com/Quantitative-Trading-Build-Algorithmic-Business/dp/0470284889)
