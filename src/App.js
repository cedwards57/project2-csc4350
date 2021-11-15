import logo from './logo.svg';
import './App.css';
import { useState, useRef } from 'react';
import GroceryList from './components/GroceryList'
import RecipeList from './components/RecipeList'

function App() {
  const args = JSON.parse(document.getElementById("data").text);
  
  return (
    <h1>{args["name"]} {args["recipes"]}</h1>
  );
}

export default App;