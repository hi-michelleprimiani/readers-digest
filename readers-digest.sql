UPDATE auth_user
SET first_name = 'Michelle', last_name = 'Primiani'
WHERE id = 2;

DELETE FROM auth_user WHERE id = 3;
DELETE FROM auth_user WHERE id = 4;
DELETE FROM auth_user WHERE id = 1;
DELETE FROM auth_user WHERE id = 2;
DELETE FROM auth_user WHERE id = 5;
DELETE FROM auth_user WHERE id = 6;

DELETE FROM digestapi_review;

DELETE FROM digestapi_book WHERE id = 13;
DELETE FROM digestapi_book WHERE id = 14;


DELETE FROM digestapi_review WHERE book_id = 14;
DELETE FROM digestapi_review WHERE book_id = 13;