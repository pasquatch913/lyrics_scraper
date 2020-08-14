 delete from clean_songs where lyrics ilike 'We do not have the lyrics for%';
update clean_songs set lyrics = regexp_replace(lyrics,'^Guided By Voices\nMiscellaneous\n[^\n]+\n','');
update clean_songs set lyrics = replace(lyrics, '{chorus}', '');
update clean_songs set lyrics = replace(lyrics, 'repeat chorus', '');
update clean_songs set lyrics = replace(lyrics, 'Chorus x2', '');
update clean_songs set lyrics = replace(lyrics, 'Chorus x3', '');
update clean_songs set lyrics = replace(lyrics, 'Chorus:', '');
update clean_songs set lyrics = replace(lyrics, '(R. Pollard)', '');
update clean_songs set lyrics = replace(lyrics, 'Pollards mumbling here', '');
update clean_songs set lyrics =  regexp_replace(lyrics,'Chorus\n','', 'g');
update clean_songs set lyrics =  regexp_replace(lyrics,'Chorus$','', 'g');

update clean_songs set lyrics =  regexp_replace(lyrics,'repeat verse[^\n]+\n','', 'gi');

update clean_songs set lyrics = replace(lyrics, 'Chorus, repeat', '');
update clean_songs set lyrics = replace(lyrics, 'repeat all', '');
update clean_songs set lyrics = replace(lyrics, 'Repeat first verse', '');
update clean_songs set lyrics = replace(lyrics, 'Chorus (replace "get" with "like")', '');

update clean_songs set lyrics = replace(lyrics, '???', '');
update clean_songs set lyrics = replace(lyrics, '??', '');
update clean_songs set lyrics = replace(lyrics, ' ? ', '');
update clean_songs set lyrics = replace(lyrics, '(?)', '');

delete from clean_songs where id = 2;

 select title, replace(lyrics, '{chorus}', '') from clean_songs where lyrics like '%{chorus}%';


-- strings to remove
-- {chorus} - done
-- repeat chorus - done
-- Chorus: - done
-- Chorus (newline) - done
-- Chorus x3 - done
-- Chorus x2 - done
-- Chorus (replace "get" with "like") - done
-- Repeat (then something?) - done

-- ???
-- ??
--  ? 
-- (?)
-- (R. Pollard) - done