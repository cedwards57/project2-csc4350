import React from 'react';

export function UserRecipe(props) {
    return (
        <p><form action="/recipe" method="get"><input type="hidden" name={props.name} value={props.id} />{props.name} <input type="submit" value="More Details"/></form></p>
    )
}