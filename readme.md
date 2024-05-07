# Movie Rating API

## To retrieve a list of movies
`http://localhost:8000/api/movies/`

## To see a spesific movie
`http://localhost:8000/api/movies/${movie.id}/`

## To rate a movie
`http://localhost:8000/api/movies/${movie.id}/rate_movie/`

```
fetch(`http://localhost:8000/api/movies/${movie.id}/rate_movie/`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token xxx'
    },
    body: JSON.stringify(
        { stars: `${userRating + 1}` }
    )
})
```