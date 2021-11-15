import logo from './logo.svg';
import './App.css';
import { useState, useRef } from 'react';
import { BrowserRouter as Router, Routes as Switch, Route, Link, Redirect } from 'react-router-dom'
import GroceryList from './components/GroceryList'
import RecipeList from './components/RecipeList'

function App() {
  const args = JSON.parse(document.getElementById("data").text);

  return (
    <h1>Placeholder</h1>
  );
}

export default App;