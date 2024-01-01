import logo from './logo.svg';
import './App.css';
import React, { useEffect } from 'react';

function App() {

  useEffect(() => {

    console.log('process.env.REACT_APP_API_URL', process.env.REACT_APP_API_URL);
    
    fetch(process.env.REACT_APP_API_URL + '/cors-test', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: 'Hello from React' }),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });

  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
