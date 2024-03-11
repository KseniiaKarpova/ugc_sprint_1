from fastapi import HTTPException, status

genres_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genres Not Found")
genre_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre Not Found")

films_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Films Not Found")
film_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Films Not Found")

person_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person Not Found")
persons_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persons Not Found")

file_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File Not Found")
forbidden_error = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have been denied access")
server_error = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="ooops")

success = HTTPException(status_code=status.HTTP_201_CREATED)

unauthorized = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
