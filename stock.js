// frontend/src/App.js

import React, { useState, useEffect } from 'react';

function App() {
  const [stocks, setStocks] = useState([]);
  const [n, setN] = useState(5);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(`/api/stocks?n=${n}`);
      const data = await response.json();
      setStocks(data);
    };

    const interval = setInterval(fetchData, 1000);

    return () => clearInterval(interval);
  }, [n]);

  return (
    <div>
      <label htmlFor="stockCount">Enter the number of stocks (max 20): </label>
      <input
        type="number"
        id="stockCount"
        value={n}
        onChange={(e) => setN(Math.min(20, Math.max(1, parseInt(e.target.value, 10))))}
      />

      <ul>
        {stocks.map((stock) => (
          <li key={stock.symbol}>{`${stock.symbol}: $${stock.price.toFixed(2)}`}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
