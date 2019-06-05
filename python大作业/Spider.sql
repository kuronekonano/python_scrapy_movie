create table movies(
	movie_id int primary key auto_increment,
	movie_year text,
	movie_name text,
	movie_director text,
	movie_writer text,
	movie_actor text,
	movie_type text,
	movie_country text,
	movie_language text,
	movie_anotherName text,
	movie_date text,
	movie_time text,
	movie_IMDB text,
	movie_grade text,
	movie_commentsNum text,
	movie_pageUrl text
);
TRUNCATE TABLE movies;
create table users(
	username varchar(64) primary key,
	password varchar(64) not null
);