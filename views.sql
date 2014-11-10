CREATE OR REPLACE VIEW public_company_detail AS
  SELECT
    entity.id             AS entity_id,
    entity.name           AS name,
    public_company.ticker AS ticker,
    public_company.sec_cik
  FROM entity
    JOIN extension_record ON entity.id = extension_record.entity_id
    JOIN public_company ON entity.id = public_company.entity_id
  WHERE extension_record.definition_id = 13

CREATE OR REPLACE VIEW people_detail AS
  SELECT
    entity.id,
    entity.name,
    person.name_last,
    person.name_first,
    person.name_middle,
    person.gender_id
  FROM entity
    JOIN extension_record ON entity.id = extension_record.entity_id
    JOIN person ON person.entity_id = entity.id
  WHERE extension_record.definition_id = 1

CREATE OR REPLACE VIEW relationship_detail AS
  SELECT
    relationship.id,
    relationship.entity1_id,
    relationship.entity2_id,
    relationship.start_date,
    relationship.end_date
  FROM relationship
    JOIN position ON relationship.id = position.relationship_id
  WHERE position.is_board = 1