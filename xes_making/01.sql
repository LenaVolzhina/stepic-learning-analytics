select actor_id, count(*) c from events_event group by actor_id order by c desc;
# top actors: 724310 727752 719459 722729 725516 722482
# just some actors: 719339 (2438), 727860 (2437), 719565 (2437), 728452 (2436), 719606 (2433), 723283 (2431)
# where actor_id in (719339, 727860, 719565, 728452, 719606, 723283)
select * from events_event where actor_id in (719339, 727860, 719565, 728452, 719606, 723283) order by time;


set @inc := 0;
set @inc1 := 0;
set @num := 0;
# NB: data in csv file must be in format "user_id,step_id,step_type,action,timestamp"
# ORDERED BY user_id, timestamp
# timestamp example: "2014-10-25T17:00:27.000+03:00"
SELECT  actor_id user_id, steps.ordered_num step_id, 
		if((select title like('%T%') from stepic_test.lessons_step where id = target_id), 'video', 'quiz') step_type, 
        (select name from activity_type_constants where id = action) action, 
        date_format(time, '%Y-%m-%dT%H:%i:%s.000+00:00') timestamp						# забиваем на часовые пояса, возможно, зря :(
FROM (select * from events_event where actor_id in (719339, 727860, 719565, 728452, 719606, 723283)) events
		join 
		(	select @num := @num + 1 ordered_num, step_id 
			from ( 
				select steps.id step_id
				from stepic_test.lessons_step steps
						join
						(	select @inc1 := @inc1 + 1 ord, unit_id, lesson_id
							from (select units.id unit_id, units.lesson_id lesson_id, units.position position, sections.ord ord, sections.section_id section_id
								from 	stepic_test.courses_unit units
									join
										(SELECT @inc := @inc + 1 ord, section_id 
										from (select id section_id FROM stepic_test.courses_section 
											  where course_id = 70		# только курс с биологией
											  order by course_id, position) qq
										where section_id = 150			# только первый модуль
										) sections
									on units.section_id = sections.section_id
								order by sections.ord, position) t) lessons
						on steps.lesson_id = lessons.lesson_id
				order by lessons.ord, steps.position) ww
			order by ordered_num) steps
		on events.target_id = steps.step_id
order by actor_id, timestamp					# обязательно !!!
into outfile "D:\\stepic\\python\\xes_making\\xes_01.csv"
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

select @num from dual;		# должно быть 83
