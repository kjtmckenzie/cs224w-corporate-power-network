--RICHEST MEN IN THE DATA SET--
select id, name_first, name_last, net_worth
from person
where net_worth > 10000000000
order by net_worth DESC;


-- Top 896 companies and their boards --
select distinct(p.id) as 'Person ID', p.name_first, p.name_last, e.name as 'Company Name' 
from entity e, person p, relationship r, position po
where r.entity2_id = e.id 
      AND r.entity1_id = p.entity_id
      AND r.is_current = 1
      AND r.is_deleted <> 1
      AND po.is_board = true
      AND po.relationship_id = r.id
      AND e.id < 1000;
      


