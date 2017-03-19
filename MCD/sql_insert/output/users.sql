INSERT INTO public.users(id, lastname, firstname, email, picture, categories_id, accounts_id)VALUES (1, 'Tom', 'Trucani','user1@mymail.org', '', 3, 1);

SELECT setval('users_id_seq',(SELECT max(id) FROM public.users));

