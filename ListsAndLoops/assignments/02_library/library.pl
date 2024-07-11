query_1(Authors) :-  setof(Author, (A, B, C, D, E)^book(A, B, author(Author, C), edition(D,E)), Authors).

query_2(Titles) :-     findall(BookTitle, (
        book(_, BookTitle, author(_, AuthorLife), edition(_, PublicationYear)),
        term_string(AuthorLife, AuthorLifeStr),
        split_string(AuthorLifeStr, '-', '', [_, AuthorDeathYearStr]),
        atom_number(AuthorDeathYearStr, AuthorDeathYear),
        PublicationYear > AuthorDeathYear
    ), Titles).

query_3(AuthorsTitles) :- 
    setof(Author-BookList, Author^BookList^(setof(Book, book(_, Book, author(Author, _), _), BookList)), AuthorsTitles).

query_4(AuthorsPairs) :- 
    setof(FirstAuthor-SecondAuthor, (
        book(_, _, author(FirstAuthor, FirstAuthorLife), _),
        book(_, _, author(SecondAuthor, SecondAuthorLife), _),
        FirstAuthor \= SecondAuthor,
        term_string(FirstAuthorLife, FirstAuthorLifeStr),
        term_string(SecondAuthorLife, SecondAuthorLifeStr),
        split_string(FirstAuthorLifeStr, '-', '', [FirstAuthorBirth, FirstAuthorDeath]),
        split_string(SecondAuthorLifeStr, '-', '', [SecondAuthorBirth, SecondAuthorDeath]),
        atom_number(FirstAuthorBirth, FirstAuthorBirthYear),
        atom_number(FirstAuthorDeath, FirstAuthorDeathYear),
        atom_number(SecondAuthorBirth, SecondAuthorBirthYear),
        atom_number(SecondAuthorDeath, SecondAuthorDeathYear),
        FirstAuthorBirthYear =< SecondAuthorDeathYear,
        SecondAuthorBirthYear =< FirstAuthorDeathYear
    ), AuthorsPairs).

query_5(LongLived) :- fail.

query_1(Authors).
query_2(Titles).
query_3(AuthorsTitles).
query_4(AuthorsPairs).

