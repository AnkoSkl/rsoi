from movie import app
from movie.repository.movie_repository import Movies

@app.route('/')
def test():
    new_movie = Movies()
    new_movie.description = 'a'
    new_movie.length = 0
    new_movie.name = 'ababa'
    new_movie.save()
    return new_movie.name

if __name__ == '__main__':
    app.run()