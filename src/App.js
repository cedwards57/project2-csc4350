import logo from './logo.svg';
import './App.css';
import { useState, useRef } from 'react';
import { ResultRecipe } from './components/ResultRecipe'
import { UserRecipe } from './components/UserRecipe'

function App() {
  const args = JSON.parse(document.getElementById("data").text);
  const [recipeList, updateRecipeList] = useState(args.recipes);
  const [searchRecipes, updateSearchRecipes] = useState([]);
  
  function searchRecipe() {
    let query = document.getElementById("searchQuery").value
    fetch("/searchrecipes", {
      method:"POST",
      cache: "no-cache",
      headers:{
          "content_type":"application/json",
      },
      body:JSON.stringify({"query": query})
    }
    ).then(response => {
      return response.json();
    }).then(data => {
      updateSearchRecipes(data.results);
    })
  }

  function saveChanges() {
    fetch("/saverecipes", {
      method:"POST",
      cache: "no-cache",
      headers:{
          "content_type":"application/json",
      },
      body:JSON.stringify({"recipeList": recipeList})
    }
    ).then(response => {
      return response.json();
    }).then(data => {
      updateRecipeList(data.newRecipeList);
    })
  }

  function addRecipe(add_recipe) {
    let newRecipeList = [...recipeList, add_recipe];
    updateRecipeList(newRecipeList);
  }

  function delRecipe(del_recipe) {
    let remove_index = recipeList.indexOf(del_recipe);
    let newRecipeList = [...recipeList];
    newRecipeList.splice(remove_index,1);
    updateRecipeList(newRecipeList);
  }

  return (
    <>
    <ul>
      <li class="pageTitle"><a class="pageTitle1" href="/recipelist">Recipe List</a></li>
      <li class="theItem"><a class="theLink" href="/grocerylist">Grocery List</a></li>
      <li class="theItem"><a class="theLink" href="/logout">logout</a></li>
    </ul>
    
    <h1 class="greeting">Hello, {args.name}</h1>
    <input type="text" id="searchQuery" placeholder="Search by ingredient..." /><button class="button1" onClick={searchRecipe}>Search</button>
    {searchRecipes.map((item, k) => <p class="listofR"><ResultRecipe id={item.id} title={item.title}/><button class="button2" onClick={() => addRecipe(item)}>Add Recipe</button></p>)}
    <h2 class="yourRecipe">Your Recipes</h2>
    {recipeList.map((item, j) => <p class="listofR"><UserRecipe id={item.id} title={item.title}/><button class="button2" onClick={() => delRecipe(item)}>Delete</button></p>)}
    <button class="button12" onClick={saveChanges}>Save Changes</button>
    </>
  );
}


export default App;
