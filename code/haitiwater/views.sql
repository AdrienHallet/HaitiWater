CREATE OR REPLACE VIEW public.water_network_virtualelementtotal AS
 SELECT e.id AS relevant_model,
    ( SELECT COALESCE(sum(c.household_size + 1), 0::bigint) AS "coalesce"
           FROM consumers_consumer c
          WHERE c.water_outlet_id = e.id) AS total_consumers,
    ( SELECT COALESCE(sum(r.quantity_distributed), 0::double precision) AS "coalesce"
           FROM report_report r
          WHERE r.water_outlet_id = e.id AND r.was_active) AS total_distributed
   FROM water_network_element e
  GROUP BY e.id;

CREATE OR REPLACE VIEW public.water_network_virtualzonetotal AS
  SELECT
    z.id AS "relevant_model",
    z.name AS "zone_name",
    ( SELECT COALESCE(count(c.id), 0)
      FROM consumers_consumer c, water_network_element e, water_network_zone sub
      WHERE c.water_outlet_id = e.id AND e.zone_id = sub.id AND sub.name = ANY(z.subzones)) AS "indiv_consumers",
    ( SELECT COALESCE(sum(c.household_size + 1), 0)
      FROM consumers_consumer c, water_network_element e, water_network_zone sub
      WHERE c.water_outlet_id = e.id AND e.zone_id = sub.id AND sub.name = ANY(z.subzones)) AS "total_consumers",
    ( SELECT COALESCE(count(e.id), 0)
      FROM water_network_element e, water_network_zone sub
      WHERE e.zone_id = sub.id AND sub.name = ANY(z.subzones) AND e.type = 'FOUNTAIN') AS "fountains",
    ( SELECT COALESCE(count(e.id), 0)
      FROM water_network_element e, water_network_zone sub
      WHERE e.zone_id = sub.id AND sub.name = ANY(z.subzones) AND e.type = 'KIOSK') AS "kiosks",
    ( SELECT COALESCE(count(e.id), 0)
      FROM water_network_element e, water_network_zone sub
      WHERE e.zone_id = sub.id AND sub.name = ANY(z.subzones) AND e.type = 'INDIVIDUAL') AS "indiv_outputs",
    ( SELECT COALESCE(count(e.id), 0)
      FROM water_network_element e, water_network_zone sub
      WHERE e.zone_id = sub.id AND sub.name = ANY(z.subzones) AND e.type = 'SOURCE') AS "water_points",
    ( SELECT COALESCE(count(e.id), 0)
      FROM water_network_element e, water_network_zone sub
      WHERE e.zone_id = sub.id AND sub.name = ANY(z.subzones) AND e.type = 'PIPE') AS "pipes",
    ( SELECT COALESCE(count(e.id), 0)
      FROM water_network_element e, water_network_zone sub
      WHERE e.zone_id = sub.id AND sub.name = ANY(z.subzones) AND e.type = 'TANK') AS "tanks"

FROM water_network_zone z;

CREATE OR REPLACE VIEW public.consumer_virtualtotalbalance AS
  SELECT
    c.id AS "relevant_model",
    ( SELECT COALESCE(SUM(p.amount), 0)
      FROM financial_payment p
      WHERE p.consumer_id = c.id) AS "payed",
    ( SELECT COALESCE(SUM(i.amount), 0)
      FROM financial_invoice i
      WHERE i.consumer_id = c.id) AS "due"
  FROM consumers_consumer c;