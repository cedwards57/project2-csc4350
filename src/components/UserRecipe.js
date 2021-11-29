import React from 'react';

export function UserRecipe(props) {
    return (
        <p><form action="/recipe" method="get"><input type="hidden" name="recipeid" value={props.id} />{props.title} <input type="submit" value="More Details"/></form></p>
    )
}