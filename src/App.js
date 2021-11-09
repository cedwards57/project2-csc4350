import logo from './logo.svg';
import './App.css';
import { useState, useRef } from 'react';

 function getMealData() {
    const [mealData, setMealData] = useState(null)
    fetch('/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(mealData),
    })
      .then(response => response.json())
      .then(data => {
        setMealData(data)
      })
      .catch(() => {
        console.log("error")
      })
  }

function App() {
  // fetches JSON data passed in by flask.render_template and loaded
  // in public/index.html in the script with id "data"
  const args = JSON.parse(document.getElementById("data").text);

  return (
    <>
    <h1>Your Grocery List</h1>
    <div class="theTable">
      <table className="table">
      </table>
    </div>
    </>
  );
}

export default App;